from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64, os
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()
AES_KEY = os.getenv("AES_KEY")

# Encrypt data
def encrypt_data(data, key):
    # Generate random 12-byte initialization vector for AES-GCM
    init_vector = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=init_vector)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    
    # Store IV, tag, and ciphertext
    return {
        'iv': base64.b64encode(init_vector).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
    }

# Decrypt data
def decrypt_data(encrypted_data, key):
    # Get specific encrypted values
    init_vector = base64.b64decode(encrypted_data['iv'])
    tag = base64.b64decode(encrypted_data['tag'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=init_vector)
    # Use tag to verify integrity
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')

# key = get_random_bytes(32)  # Generates a 32-byte (256-bit) key
# key = AES_KEY
key = base64.b64decode(AES_KEY)

# print("KEY", key)
# encoded_key = base64.b64encode(key).decode('utf-8')
# print(f"Encoded Key (for storage): {encoded_key}")

encrypted_data = encrypt_data("testing more message", key)
print("Encrypted:", encrypted_data)

decrypted_data = decrypt_data(encrypted_data, key)
print("Decrypted:", decrypted_data)
