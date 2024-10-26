from pymongo import MongoClient, DESCENDING
import os
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
import hashing

# Load .env file variables
load_dotenv()

# Connect to MongoDB database
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['toolkit_db']

def get_date_time():
    # Get current date and time
    now = datetime.now()
    
    # Format: dd/mm/YY H:M:S
    datetime_formatted = now.strftime("%d/%m/%Y %H:%M:%S")
    return datetime_formatted

# Insert file info into database
def insert_file_db(filename, file_hash):
    collection = db['files']
    current_datetime = get_date_time()
    file_data = {
        "filename": filename,
        "file_hash": file_hash,
        "date": current_datetime
    }
    collection.insert_one(file_data)

# Find a file by hash
def find_file_by_hash(file_hash):
    collection = db['files']
    return collection.find_one({"file_hash": file_hash})

# Find the most recent file by filename
def find_recent_file_by_name(filename, user_id):
    collection = db['files']
    filename_recent_date = collection.find_one({"filename": filename, "user_id": user_id}, sort=[('date', DESCENDING)])
    
    if filename_recent_date:
        return filename_recent_date
    return None

# Insert or update a file entry in the database
def update_file_db(user_id, filename, file_hash, content_type, size, last_modified_date):
    collection = db['files']

    # Insert file data if new, otherwise update these fields
    current_datetime = get_date_time()
    file_data = {
        "user_id": user_id,
        "filename": filename,
        "file_hash": file_hash,
        "content_type": content_type,
        "size": size,
        "last_modified_date": last_modified_date,
        "date": current_datetime,
    }

    # Insert or update a file entry
    update_result = collection.update_one(
        {"filename": filename, "user_id": user_id},
        {"$set": file_data},  # Use set operator to update the fields
        upsert=True  # Upsert creates a new document if none is found
    )

    if update_result is None:
        return False
    return True

# Insert new log entry info into database
def insert_log_db(user_id, filename, file_differences):
    collection = db['logs']
    current_datetime = get_date_time()

    print("DIFFERENCES", file_differences)
    full_log_message = ""
    if len(file_differences) == 1:
        full_log_message += "Field changed: "
    else:
        full_log_message += "Fields changed: "

    for index, (key, value) in enumerate(file_differences.items()):
        # Search and remove any "_" symbol, then append key to the full_log_message string
        key_string = str(key).replace('_', ' ')
        full_log_message += key_string
        # Add commas between keys
        if index != len(file_differences)-1:
            full_log_message += ', '
    
    print("FULL MESSAGE: ", full_log_message)

    log_info = {
        "user_id": user_id,
        "filename": filename,
        "log_message": full_log_message,
        "date": current_datetime,
    }

    # Merge file_differences into log_info, so all info is stored in one dictionary
    log_info.update(file_differences)
    collection.insert_one(log_info)

# Creates a log file for the user
def generate_log_file(user_id, username):
    collection = db['logs']
    # Get logs for this user
    user_logs = collection.find({"user_id": user_id})  

    log_file_path = f"{username}-logs.pdf"
    
    # Create a PDF object
    canvasObj = canvas.Canvas(log_file_path, pagesize=letter)
    canvasObj.setFont("Helvetica", 12)
    canvasObj.drawString(50, 750, f"Log File for {username}")
    canvasObj.drawString(50, 730, f"Created on: {get_date_time()}")
    
    y_position = 700  # Start position to write logs

    # Iterate over the logs and write each line in the PDF
    for log in user_logs:
        print("LOG", log)
        canvasObj.drawString(50, y_position, f"Date: {log['date']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"Filename: {log['filename']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"Message: {log['log_message']}")
        # y_position -= 20
        # canvasObj.drawString(50, y_position, f"Old Hash: {log['old_file_hash']}")
        # y_position -= 20
        # canvasObj.drawString(50, y_position, f"New Hash: {log['new_file_hash']}")
        y_position -= 40
    
    # Save the PDF
    canvasObj.save()
    return log_file_path

# Generate a user ID
def generate_user_id():
    # Use uuid4 to generate an ID
    uuid_value = uuid.uuid4() 
    print("The id generated using uuid4() : ", uuid_value) 
    return str(uuid_value)

# Insert user into database
def insert_user_db(username, password):
    collection = db['users']
    current_datetime = get_date_time()
    hash_password = hashing.generate_hash(password.encode('utf-8'))
    user_data = {
        "userID": generate_user_id(),
        "username": username,
        "password": hash_password,
        "date": current_datetime
    }
    collection.insert_one(user_data)
    return user_data

# Find a user by username
def find_username(username):
    collection = db['users']
    return collection.find_one({"username": username})

# Find a user by username and password
def find_user_account(username, password):
    collection = db['users']
    hash_password = hashing.generate_hash(password.encode('utf-8'))
    return collection.find_one({"username": username, "password": hash_password})

def find_file_differences(original_file, new_file):
    # Ensure both are dictionaries
    if not isinstance(original_file, dict) or not isinstance(new_file, dict):
        print("Inputs must be dictionaries.")
        return

    differences = {}

    # Loop through each key in the new file, which has only the info to compare
    for key in new_file:
        if key in original_file:
            original_value = original_file[key]
            new_value = new_file[key]
            
            # Compare the initial and new values
            if original_value != new_value:
                differences[key] = {
                    "original_value": original_value,
                    "new_value": new_value
                }

    if differences:
        print("Differences found between the files:")
        for key, diff in differences.items():
            print(f"Key: {key}")
            print(f"  Original Value: {diff['original_value']}")
            print(f"  New Value: {diff['new_value']}")
        return differences
    else:
        print("There were no differences found between the files.")
        return None