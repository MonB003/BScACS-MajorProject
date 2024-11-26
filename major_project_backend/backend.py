from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import database, hashing, files
import os, stat

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set upload folder
UPLOAD_FOLDER = 'uploaded-files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was sent.'}), 400
        
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if not user_id:
        return jsonify({'error': 'The user ID cannot be empty.'}), 400
    
    size = request.form.get('size')
    last_modified_date = request.form.get('lastModifiedDate')

    if file:
        # Create file path to save the file to
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # Make file read-only for security
        # os.chmod(file_path, stat.S_IREAD)
        
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = hashing.generate_hash(file_data)
        # Store file name and hash in database
        database.update_file_db(user_id, file.filename, file_hash, file.content_type, size, last_modified_date)

        # Parse metadata based on file type
        files.parse_file_by_type(file, file_path, file.content_type)

        # chunk_hashes = hashing.generate_chunked_hash(file_data)
        # # Store file name and chunk hashes in database
        # database.update_file_db(
        #     user_id,
        #     file.filename,
        #     chunk_hashes,         # Store the list of chunk hashes
        #     file.content_type,
        #     size,
        #     last_modified_date
        # )

        message = "The file: " + file.filename + " was uploaded successfully."
        return jsonify({'message': message, 'file': file.filename}), 200

@app.route("/check-file", methods=['POST'])
def handle_file_check():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was sent.'}), 400
    
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form and store as a number
    user_id = request.form.get('user_id')
    size = request.form.get('size')
    last_modified_date = request.form.get('lastModifiedDate')

    if file.filename == '':
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        new_file_hash = hashing.generate_hash(file_data)
        # new_file_hash = hashing.generate_chunked_hash(file_data)

        filename = file.filename
        filename_result = database.find_recent_file_by_name(filename, user_id)
        new_file_result = {
            "user_id": user_id,
            "filename": filename,
            "file_hash": new_file_hash,
            "content_type": file.content_type,
            "size": size,
            "last_modified_date": last_modified_date
        }        
        
        if not filename_result:
            error_message = "Error. The file: " + filename + " was not found."
            return jsonify({'error': error_message}), 404

        differences_result = database.find_file_differences(filename_result, new_file_result)
        if differences_result is None:
            success_message = "Success! The file: " + filename + " has not changed."
            return jsonify({'message': success_message, 'file': filename_result['filename'], 'file_hash': filename_result['file_hash'], 'date': filename_result['date']}), 200
        else:
            error_message = "Error. The file: " + filename + " has changed."
            log_message = "" # TEMP: database.insert_log_db(user_id, filename, differences_result)
            return jsonify({'error': error_message, 'log_message': log_message}), 400

# Utility function to make MongoDB documents JSON serializable
def serialize_file(file_doc):
    file_doc['_id'] = str(file_doc['_id'])  # Convert ObjectId to a string
    return file_doc

@app.route("/get-user-files", methods=['POST'])
def get_user_files():
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'The user ID cannot be empty.'}), 400
    
    user_files_result = database.get_user_files(user_id)
    if user_files_result is None:
        return jsonify({'message': "The user has no files."}), 404
    else:
        # Convert cursor to a list of JSON-serializable dictionaries
        user_files = [serialize_file(file) for file in user_files_result]
        return jsonify({'message': "Success! The user has files.", 'files': user_files}), 200

@app.route("/generate-log-file", methods=['POST'])
def download_log_file():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    log_file_path = database.generate_log_file(user_id, username)

    # Return the PDF log file to download
    return send_file(log_file_path, as_attachment=True, download_name=f"{username}-logs.pdf")

@app.route("/signup", methods=['POST'])
def handle_user_signup():
    # Get the username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')
    print("Signup for user", username)

    if username == '' or password == '':
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
    if username:
        username_result = database.find_username(username)
        if username_result:
            return jsonify({'error': 'An account with this username already exists.'}), 400
        else:
            user_result = database.insert_user_db(username, password)
            print("USER", user_result)
            return jsonify({'message': 'Success: A user account has been created.', 'user_id': user_result['userID'], 'username': user_result['username']}), 200

@app.route("/login", methods=['POST'])
def handle_user_login():
    # Get the username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')
    print("Login for user", username)

    if username == '' or password == '':
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
    if username and password:
        user_result = database.find_user_account(username, password)
        if not user_result:
            return jsonify({'error': 'No user account exists with this information.'}), 404
        else:
            return jsonify({'message': 'Success: A user account was found.', 'user_id': user_result['userID'], 'username': user_result['username']}), 200

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)