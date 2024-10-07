from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import database, hashing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
        
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 404
    
    if not user_id:
        return jsonify({'error': 'No user ID was provided'}), 400

    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = hashing.generate_file_hash(file_data)
        print("FILE HASH: ", file_hash)

        # Store file name and hash in database
        database.update_file_db(user_id, file.filename, file_hash)

        return jsonify({'message': 'File uploaded successfully', 'file': file.filename, 'file_hash': file_hash}), 200

@app.route("/check-file", methods=['POST'])
def handle_file_check():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    # Get the file data from the request form
    file = request.files['file']
    # Get the user ID from the request form and store as a number
    user_id = request.form.get('user_id')
    user_id_num = int(user_id)

    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 404
    
    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        new_file_hash = hashing.generate_file_hash(file_data)

        filename = file.filename

        filename_result = database.find_recent_file_by_name(filename)
        print("FILENAME RESULT", filename_result)

        if not filename_result:
            return jsonify({'error': 'File not found'}), 404

        same_file_hash = hashing.compare_file_hashes(filename_result['file_hash'], new_file_hash)
        print("CHECK FILE HASH RESULT", same_file_hash)

        if same_file_hash:
            return jsonify({'message': 'Success: File has not changed.', 'file': filename_result['filename'], 'file_hash': filename_result['file_hash'], 'date': filename_result['date']}), 200
        else:
            database.insert_log_db(user_id_num, filename, "File hashes do not match.", filename_result['file_hash'], new_file_hash)
            return jsonify({'error': 'Error: File has changed.'}), 400

@app.route("/generate-log-file", methods=['GET'])
def download_log_file():
    user_id = 1  # Hardcoded
    log_file_path = database.generate_log_file(1)

    # Return the PDF log file to download
    return send_file(log_file_path, as_attachment=True, download_name=f"user{user_id}-logs.pdf")

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)