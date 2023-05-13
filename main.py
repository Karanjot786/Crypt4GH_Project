from flask import Flask, request, jsonify
import crypt4gh.keys as c4gh_keys
import crypt4gh.lib as c4gh_lib

app = Flask(__name__)

# Specify the location of the key files

# Load the key pair
public_key_file = "karanjot.pub"
public_key = c4gh_keys.get_public_key(public_key_file)
private_key_file = "karanjot.sec"
private_key = c4gh_keys.get_public_key(private_key_file)

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    file = request.files['file']
    encrypted_file = 'encrypted.c4gh'

    # Encrypt the file
    with open(file.filename, 'rb') as file_in:
        with open(encrypted_file, 'wb') as file_out:
            c4gh_lib.encrypt(public_key,file_in, file_out)
            

    return jsonify({'message': 'File encrypted successfully!'})

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    file = request.files['file']
    decrypted_file = 'decrypted.txt'

    # Decrypt the file
    with open(file.filename, 'rb') as file_in:
        with open(decrypted_file, 'wb') as file_out:
            c4gh_lib.decrypt(private_key, file_in, file_out, public_key)
            

    return jsonify({'message': 'File decrypted successfully!'})

if __name__ == '__main__':
    app.run()
