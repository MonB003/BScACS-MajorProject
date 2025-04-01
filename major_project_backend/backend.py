from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import database, hashing, files, security, testing
import datetime, jwt, os, time
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load .env file variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # Secure and unique key
ALGORITHM = "HS256"  # HMAC SHA-256

# Get env variable, default to "false", store as boolean
test_mode_env = os.getenv("TEST_MODE", "false")
TEST_MODE = True if test_mode_env.lower() == "true" else False

# Set file upload and changes folders
UPLOAD_FOLDER = 'uploaded-files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CHANGES_FOLDER = 'changed-files/'
app.config['CHANGES_FOLDER'] = CHANGES_FOLDER

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    test_method = "handle_file_upload (error)"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer

    if 'file' not in request.files:
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'No file was sent.'}), 400
        
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form
    user_id = request.form.get('user_id')

    if file.filename == '':
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if not user_id:
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'The user ID cannot be empty.'}), 400
    
    size = request.form.get('size')
    last_modified_date = request.form.get('lastModifiedDate')
    file_path_form = request.form.get('filePath').strip()
    
    # Get full file path by combining the file path and filename
    full_file_path = os.path.join(file_path_form, file.filename)
    full_file_path = os.path.normpath(full_file_path)

    if not os.path.exists(full_file_path):
        error_message = "Error. The file path: " + full_file_path + " does not exist."
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': error_message}), 404

    if file:
        # Create directory path
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    
        # Create file path to save the file to
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Temporarily change permissions to writable
        security.make_file_writable(file_path)

        # Save the new file (overwrites if exists)
        file.save(file_path)
        
        # Store encrypted version of the file
        security.encrypt_file(file_path, app.config['UPLOAD_FOLDER'], user_id)

        # Make file read-only again
        security.make_file_readable(file_path)
        
        # Reset the file pointer after saving it
        file.seek(0)
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = hashing.generate_hash(file_data)
        # Store file name and hash in database
        database.update_file_db(user_id, file.filename, file_hash, file.content_type, size, last_modified_date, file_path_form)

        message = "The file: " + file.filename + " was uploaded successfully."
        test_method = f"handle_file_upload (file: {file.filename})"
        testing.record_test_time(test_method, start_time)
        return jsonify({'message': message, 'file': file.filename}), 200

@app.route("/check-file", methods=['POST'])
def handle_file_check():
    test_method = "handle_file_check (error)"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer
        
    if 'file' not in request.files:
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'No file was sent.'}), 400
    
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form and store as a number
    user_id = request.form.get('user_id')
    size = request.form.get('size')
    last_modified_date = request.form.get('lastModifiedDate')
    file_path_form = request.form.get('filePath')

    if file.filename == '':
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        new_file_hash = hashing.generate_hash(file_data)
        
        filename = file.filename
        filename_result = database.find_recent_file_by_name(filename, file_path_form, user_id)
        new_file_result = {
            "user_id": user_id,
            "filename": filename,
            "file_path": file_path_form,
            "file_hash": new_file_hash,
            "content_type": file.content_type,
            "size": size,
            "last_modified_date": last_modified_date
        }        
        
        if not filename_result:
            error_message = "Error. The file: " + filename + " in the " + file_path_form + " directory was not found."
            testing.record_test_time(test_method, start_time)
            return jsonify({'error': error_message}), 404
        
        differences_result = database.find_file_differences(filename_result, new_file_result)
        if differences_result is None:
            success_message = "Success! The file: " + filename + " has not changed."
            test_method = f"handle_file_check (file not changed: {filename})"
            testing.record_test_time(test_method, start_time)
            return jsonify({'message': success_message, 'file': filename_result['filename'], 'file_hash': filename_result['file_hash'], 'date': filename_result['date']}), 200
        else:
            # Decrypt the encrypted initial file
            security.decrypt_file(file.filename, app.config['UPLOAD_FOLDER'], user_id)

            # Get file path of decrypted file
            name = "decrypt-" + file.filename
            decrypted_initial_file = os.path.join(app.config['UPLOAD_FOLDER'], name)
        
            # Find differences in content between the two files
            file_data_changes = files.compare_file_content(decrypted_initial_file, file_data, file.content_type)

            # Write file differences to a local file
            content_changes_log = ""
            if file_data_changes is not None:
                content_changes_log = "Log file for file content changes: "
                changes_log_file = files.save_file_changes(app.config['CHANGES_FOLDER'], user_id, file.filename, differences_result, file_data_changes)
                content_changes_log += changes_log_file

            error_message = "Error. The file: " + filename + " has changed."
            log_message = database.insert_log_db(user_id, filename, differences_result)
            
            test_method = f"handle_file_check (file changed: {filename})"
            testing.record_test_time(test_method, start_time)
            return jsonify({'error': error_message, 'log_message': log_message, 'log_file': content_changes_log}), 400

# Utility function to make MongoDB documents JSON serializable
def serialize_file(file_doc):
    file_doc['_id'] = str(file_doc['_id'])  # Convert ObjectId to a string
    return file_doc

@app.route("/get-user-files", methods=['POST'])
def get_user_files():
    test_method = "get_user_files"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer
        
    user_id = request.form.get('user_id')
    
    if not user_id:
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'The user ID cannot be empty.'}), 400
    
    user_files_result = database.get_user_files(user_id)
    if user_files_result is None:
        testing.record_test_time(test_method, start_time)
        return jsonify({'message': "The user has no files."}), 404
    else:
        # Convert cursor to a list of JSON-serializable dictionaries
        user_files = [serialize_file(file) for file in user_files_result]
        testing.record_test_time(test_method, start_time)
        return jsonify({'message': "Success! The user has files.", 'files': user_files}), 200

@app.route("/generate-log-file", methods=['POST'])
def download_log_file():
    test_method = "download_log_file"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer
        
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    log_file_path = database.generate_log_file(user_id, username)

    testing.record_test_time(test_method, start_time)
    # Return the PDF log file to download
    return send_file(log_file_path, as_attachment=True, download_name=f"{username}-logs.pdf")

@app.route("/signup", methods=['POST'])
def handle_user_signup():
    test_method = "handle_user_signup (error)"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer
        
    # Get the username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')
    print("Signup for user", username)

    if username == '' or password == '':
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
    if username:
        username_result = database.find_username(username)
        if username_result:
            testing.record_test_time(test_method, start_time)
            return jsonify({'error': 'An account with this username already exists.'}), 400
        else:
            # Store new user
            user_result = database.insert_user_db(username, password)
            # Setup access token
            access_token = create_access_token(user_result['userID'])
            response = make_response(jsonify({'message': 'Login successful'}))
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Strict', max_age=datetime.timedelta(hours=1))
            
            test_method = f"handle_user_signup (user: {user_result['username']})"
            testing.record_test_time(test_method, start_time)
            return jsonify({'message': 'Success: A user account has been created.', 'user_id': user_result['userID'], 'username': user_result['username'], "access_token": access_token}), 200

@app.route("/login", methods=['POST'])
def handle_user_login():
    test_method = "handle_user_login (error)"
    start_time = None
    if TEST_MODE:
        start_time = time.perf_counter()  # Start timer
        
    # Get the username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')
    print("Login for user", username)

    if username == '' or password == '':
        testing.record_test_time(test_method, start_time)
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
    if username and password:
        user_result = database.find_user_account(username, password)
        if not user_result:
            testing.record_test_time(test_method, start_time)
            return jsonify({'error': 'No user account exists with this information.'}), 404
        else:
            # Setup access token
            access_token = create_access_token(user_result['userID'])
            response = make_response(jsonify({'message': 'Login successful'}))
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Strict', max_age=datetime.timedelta(hours=1))

            test_method = f"handle_user_login (user: {user_result['username']})"
            testing.record_test_time(test_method, start_time)
            return jsonify({'message': 'Success: A user account was found.', 'user_id': user_result['userID'], 'username': user_result['username'], "access_token": access_token}), 200

def create_access_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),  # Token expires in 1 hour
        "iat": datetime.datetime.now(datetime.timezone.utc),  # Issued at
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded  # Returns the payload if valid
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
@app.route('/record-time', methods=['POST'])
def record_time():
    # testing_file = f"testing_times_{os.name}.txt"
    data = request.json
    method = data.get("methodName")
    total_time = data.get("totalTime")
    
    # print("TIME", total_time)
    # print(f"RECORD TIME: Received time for {method}: {total_time} ms")  # Debugging line

    testing.write_test_time(method, total_time, "Frontend")

    # with open(testing_file, "a") as file:
    #     file.write(f"{feature}: {total_time} ms\n")

    # return {"message": "Method time recorded"}, 200
    return jsonify({'message': 'Method time recorded'}), 200

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)