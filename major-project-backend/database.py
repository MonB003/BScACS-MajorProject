from pymongo import MongoClient, DESCENDING
import os
from dotenv import load_dotenv
from datetime import datetime

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