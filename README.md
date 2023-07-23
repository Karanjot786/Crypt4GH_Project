# HTTP(S) File Server in Flask

This is a simple HTTP(S) file server written in Flask that allows users to upload and download files securely over HTTPS. The server uses a self-signed SSL certificate for testing purposes.

## Requirements

- Python 3.x
- Flask (install using `pip3 install Flask`)

## How to Use

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


### Uploading a File

To upload a file, use the following curl command:

```bash
curl -k -X POST -F "file=@/path/to/your/file.jpg" https://127.0.0.1:5000/upload
```

Replace /path/to/your/file.jpg with the actual path to the file you want to upload. The server will respond with a JSON message indicating whether the upload was successful or if there was an error.

### Downloading a File

```bash
curl -k -OJ https://127.0.0.1:5000/uploads/your_filename.jpg
```
Replace your_filename.jpg with the name of the file you want to download. The server will download the file and save it in your current directory.

### Byte-Range Support

The server now supports byte-range requests, allowing clients to request specific portions of a file. To fetch a specific byte range of a file, you can use the -r or --range option with curl.

`For example, to fetch the first 100 bytes of a file:`

```bash
curl -k -OJ -r 0-99 https://127.0.0.1:5000/uploads/your_filename.jpg
```

`To fetch the range of bytes from 100 to 199:`

```bash
curl -k -OJ -r 100-199 https://127.0.0.1:5000/uploads/your_filename.jpg
```

`You can also fetch multiple byte ranges by specifying them comma-separated:`

```bash
curl -k -OJ -r 0-49,100-149 https://127.0.0.1:5000/uploads/your_filename.jpg
```

`Please note that byte ranges should be valid, and the server will respond with the requested byte range using the 206 Partial Content response.`


### Security Considerations

The server is using a self-signed SSL certificate for testing purposes only. In production, you should obtain a valid SSL certificate from a trusted certificate authority.

The app.secret_key is generated randomly to secure session handling. 