from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Members API Route

@app.route("/upload-file", methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        return jsonify({'message': 'File uploaded successfully', 'file_path': file.filename}), 200

# To run the app
if __name__ == "__main__":
    # Debug is true because we're in development mode
    app.run(debug=True)