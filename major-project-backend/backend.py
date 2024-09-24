from flask import Flask, request, jsonify
from flask_cors import CORS
import os, hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set upload folder
UPLOAD_FOLDER = 'uploaded-files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file with the specified filename'}), 400
    
    # Check if the upload folder exists, otherwise create it
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if file:
        # Create file path to save the file to
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Hash the file
        file_hash = generate_file_hash(file_path)
        print("FILE HASH: ", file_hash)

        return jsonify({'message': 'File uploaded successfully', 'file_path': file.filename, 'file_hash': file_hash}), 200

def generate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)