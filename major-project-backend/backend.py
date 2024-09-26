from flask import Flask, request, jsonify
from flask_cors import CORS
import database, files

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 404

    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = files.generate_file_hash(file_data)
        print("FILE HASH: ", file_hash)

        # Store file name and hash in database
        database.insert_file_db(file.filename, file_hash)

        return jsonify({'message': 'File uploaded successfully', 'file': file.filename, 'file_hash': file_hash}), 200

@app.route("/check-file", methods=['POST'])
def handle_file_check():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 404
    
    if file:
        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        new_file_hash = files.generate_file_hash(file_data)

        filename = file.filename

        filename_result = database.find_recent_file_by_name(filename)
        print("FILENAME RESULT", filename_result)

        if not filename_result:
            return jsonify({'error': 'File not found'}), 404

        same_file_hash = files.compare_file_hashes(filename_result['file_hash'], new_file_hash)
        print("CHECK FILE HASH RESULT", same_file_hash)

        if same_file_hash:
            return jsonify({'message': 'Success: File has not changed.', 'file': filename_result['filename'], 'file_hash': filename_result['file_hash'], 'date': filename_result['date']}), 200
        else:
            database.insert_log_db(1, filename, "File hashes do not match.", filename_result['file_hash'], new_file_hash)
            return jsonify({'error': 'Error: File has changed.'}), 400

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)