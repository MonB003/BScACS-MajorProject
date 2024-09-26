from pymongo import MongoClient, DESCENDING
import os
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load .env file variables
load_dotenv()

# Connect to MongoDB database
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['files_db']

def get_date_time():
    # Get current date and time
    now = datetime.now()
    
    # Format: dd/mm/YY H:M:S
    datetime_formatted = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Date and time:", datetime_formatted)
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
def find_recent_file_by_name(filename):
    collection = db['files']
    filename_recent_date = collection.find_one({"filename": filename}, sort=[('date', DESCENDING)])
    
    if filename_recent_date:
        print("MOST RECENT FILE RESULT", filename_recent_date)
        return filename_recent_date
    return None


# Insert new log entry info into database
def insert_log_db(user_id, filename, log_message, old_file_hash, new_file_hash):
    collection = db['logs']
    current_datetime = get_date_time()
    log_info = {
        "user_id": user_id,
        "filename": filename,
        "log_message": log_message,
        "old_file_hash": old_file_hash,
        "new_file_hash": new_file_hash,
        "date": current_datetime
    }
    collection.insert_one(log_info)

# Creates a log file for the user
def generate_log_file(user_id):
    collection = db['logs']
    # Get logs for this user
    user_logs = collection.find({"user_id": user_id})  

    log_file_path = f"user{user_id}-logs.pdf"
    
    # Create a PDF object
    canvasObj = canvas.Canvas(log_file_path, pagesize=letter)
    canvasObj.setFont("Helvetica", 12)
    canvasObj.drawString(50, 750, f"Log File for User {user_id}")
    canvasObj.drawString(50, 730, f"Created on: {get_date_time()}")
    
    y_position = 700  # Start position to write logs

    # Iterate over the logs and write each line in the PDF
    for log in user_logs:
        canvasObj.drawString(50, y_position, f"Date: {log['date']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"Filename: {log['filename']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"Message: {log['log_message']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"Old Hash: {log['old_file_hash']}")
        y_position -= 20
        canvasObj.drawString(50, y_position, f"New Hash: {log['new_file_hash']}")
        y_position -= 40
    
    # Save the PDF
    canvasObj.save()
    return log_file_path