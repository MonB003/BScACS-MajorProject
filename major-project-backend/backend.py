from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import database, files

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set upload folder
# UPLOAD_FOLDER = 'uploaded-files/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 400
    
    # # Check if the upload folder exists, otherwise create it
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])

    if file:
        # Create file path to save the file to
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # file.save(file_path)

        # # Hash the file
        # file_hash = files.generate_file_hash(file_path)
        # print("FILE HASH: ", file_hash)

        # Read file content from memory
        file_data = file.read()

        # Hash the file content
        file_hash = files.generate_file_hash(file_data)
        print("FILE HASH: ", file_hash)

        # Store file name and hash in database
        database.insert_file_db(file.filename, file_hash)

        return jsonify({'message': 'File uploaded successfully', 'file': file.filename, 'file_hash': file_hash}), 200

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)