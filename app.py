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
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found.'}), 404

    file_size = os.path.getsize(file_path)
    ranges = parse_range_header(request.headers.get('Range'), file_size)

    if not ranges:
        # No Range header provided, serve the entire file as before
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    content_length = sum(end - start + 1 for start, end in ranges)
    response_headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(content_length),
        'Accept-Ranges': 'bytes',
        'Content-MD5': generate_content_md5(file_path)
    }

    def generate_partial_content():
        with open(file_path, 'rb') as file:
            for start, end in ranges:
                file.seek(start)
                yield file.read(end - start + 1)

    return generate_partial_content(), 206, response_headers  # Return 206 Partial Content

def parse_range_header(range_header, file_size):
    try:
        # The Range header should look like: "bytes=start-end,start-end,..."
        if not range_header.startswith('bytes='):
            return None

        ranges = []
        byte_ranges = range_header[len('bytes='):].split(',')
        for byte_range in byte_ranges:
            start, end = map(int, byte_range.split('-'))
            if start < 0:
                start = max(file_size + start, 0)
            if end < 0:
                end = max(file_size + end, 0)
            if start >= file_size or end >= file_size or start > end:
                return None
            ranges.append((start, end))
        
        return ranges
    except (ValueError, AttributeError):
        return None

def generate_content_md5(file_path):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
