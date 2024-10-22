from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import database, hashing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was sent.'}), 400
        
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form
    user_id = request.form.get('user_id')
    print("USER ID", user_id)

    if file.filename == '':
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if not user_id:
        return jsonify({'error': 'The user ID cannot be empty.'}), 400

    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = hashing.generate_hash(file_data)

        # Store file name and hash in database
        database.update_file_db(user_id, file.filename, file_hash)

        return jsonify({'message': 'File uploaded successfully', 'file': file.filename, 'file_hash': file_hash}), 200

@app.route("/check-file", methods=['POST'])
def handle_file_check():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was sent.'}), 400
    
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form and store as a number
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({'error': 'The filename cannot be empty.'}), 404
    
    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        new_file_hash = hashing.generate_hash(file_data)

        filename = file.filename

        filename_result = database.find_recent_file_by_name(filename, user_id)
        
        if not filename_result:
            error_message = "Error. The file: " + filename + " was not found."
            return jsonify({'error': error_message}), 404

        same_file_hash = hashing.compare_file_hashes(filename_result['file_hash'], new_file_hash)

        if same_file_hash:
            success_message = "Success! The file: " + filename + " has not changed."
            return jsonify({'message': success_message, 'file': filename_result['filename'], 'file_hash': filename_result['file_hash'], 'date': filename_result['date']}), 200
        else:
            error_message = "Error. The file: " + filename + " has changed."
            database.insert_log_db(user_id, filename, "File hashes do not match.", filename_result['file_hash'], new_file_hash)
            return jsonify({'error': error_message}), 400

@app.route("/generate-log-file", methods=['POST'])
def download_log_file():
    # user_id = "1"  # Hardcoded
    # username = "username"
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    # print("REQUEST: " + user_id1 + " " + username1)

    log_file_path = database.generate_log_file(user_id, username)

    # Return the PDF log file to download
    return send_file(log_file_path, as_attachment=True, download_name=f"{username}-logs.pdf")

@app.route("/signup", methods=['POST'])
def handle_user_signup():
    # Get the username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')

    print("USERNAME", username)
    print("PASSWORD", password)

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

    print("USERNAME", username)
    print("PASSWORD", password)

    if username == '' or password == '':
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
    if username and password:
        user_result = database.find_user_account(username, password)
        if not user_result:
            return jsonify({'error': 'No user account exists with this information.'}), 400
        else:
            print("USER", user_result)
            return jsonify({'message': 'Success: A user account was found.', 'user_id': user_result['userID'], 'username': user_result['username']}), 200

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)