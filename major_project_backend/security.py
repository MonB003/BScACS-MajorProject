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

def encrypt_dictionary(dict_items):
    # Loop through each key value in the dictionary
    aes_key = base64.b64decode(AES_KEY)
    for key, value in dict_items.items():
        if isinstance(value, dict) and 'original_value' in value and 'new_value' in value:
            orig_value = value["original_value"]
            new_value = value["new_value"]
            # Encrypt the values
            encrypted_orig_value = encrypt_data(orig_value, aes_key)
            encrypted_new_value = encrypt_data(new_value, aes_key)
            # Update dictionary to store encrypted values
            dict_items[key]["original_value"] = encrypted_orig_value
            dict_items[key]["new_value"] = encrypted_new_value
        elif key == 'user_id' or key == '_id':
            # Do not encrypt the user ID, since it's used to find a user's logs
            print("IDs are not encrypted")
        else:
            # Encrypt the value
            encrypted_value = encrypt_data(value, aes_key)
            # Update dictionary to store encrypted value
            dict_items[key] = encrypted_value

def decrypt_dictionary(dict_items):
    # Loop through each key value in the dictionary
    aes_key = base64.b64decode(AES_KEY)
    for key, value in dict_items.items():
        if isinstance(value, dict) and 'original_value' in value and 'new_value' in value:
            orig_value = value["original_value"]
            new_value = value["new_value"]
            # Decrypt the values
            decrypted_orig_value = decrypt_data(orig_value, aes_key)
            decrypted_new_value = decrypt_data(new_value, aes_key)
            # Update dictionary to store decrypted values
            dict_items[key]["original_value"] = decrypted_orig_value
            dict_items[key]["new_value"] = decrypted_new_value
        elif key == 'user_id' or key == '_id':
            print("IDs are not decrypted")
        else:
            # Decrypt the value
            decrypted_value = decrypt_data(value, aes_key)
            # Update dictionary to store decrypted value
            dict_items[key] = decrypted_value
