import os
from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Generate a random 32-byte (256-bit) secret key
secret_key = secrets.token_hex(32)
app.secret_key = secret_key

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully.', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file format. Allowed formats are: ' + ', '.join(app.config['ALLOWED_EXTENSIONS'])}), 400

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)
