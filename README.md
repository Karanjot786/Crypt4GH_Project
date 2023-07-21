# HTTP(S) File Server in Flask

This is a simple HTTP(S) file server written in Flask that allows users to upload and download files securely over HTTPS. The server uses a self-signed SSL certificate for testing purposes.
Requirements

    Python 3.x
    Flask (install using pip3 install Flask)

### How to Use

Clone this repository to your local machine:

```bash
git clone https://github.com/Karanjot786/Crypt4GH_Project
cd Crypt4GH_Project
```

### Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

### Start the Flask server:

```bash
python3 app.py
```

Important Note: Since the server uses a self-signed SSL certificate, you might encounter SSL certificate errors when testing with curl. To bypass the SSL certificate verification for testing, use the -k or --insecure flag with curl.

### Uploading a File:

```bash
curl -k -X POST -F "file=@/path/to/your/file.jpg" https://127.0.0.1:5000/upload
```

Replace /path/to/your/file.jpg with the actual path to the file you want to upload. The server will respond with a JSON message indicating whether the upload was successful or if there was an error.

### Downloading a File:

```bash
curl -k -OJ https://127.0.0.1:5000/uploads/your_filename.jpg
```

Replace your_filename.jpg with the name of the file you want to download. The server will download the file and save it in your current directory.

### Security Considerations

The server is using a self-signed SSL certificate for testing purposes only. In production, you should obtain a valid SSL certificate from a trusted certificate authority.

The app.secret_key is generated randomly to secure session handling. Replace the your_secret_key in the code with a strong, random key for production use.