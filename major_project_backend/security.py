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
            # print("ENCRYPT ORIG", encrypted_orig_value)
            # print("ENCRYPT NEW", encrypted_new_value)
            # Update dictionary to store encrypted values
            dict_items[key]["original_value"] = encrypted_orig_value
            dict_items[key]["new_value"] = encrypted_new_value
        else:
            # Encrypt the value
            encrypted_value = encrypt_data(value, aes_key)
            # print("ENCRYPT VALUE", encrypted_value)
            # Update dictionary to store encrypted value
            dict_items[key] = encrypted_value


# key = base64.b64decode(AES_KEY)
# encrypted_data = encrypt_data("testing more message", key)
# print("Encrypted:", encrypted_data)
# decrypted_data = decrypt_data(encrypted_data, key)
# print("Decrypted:", decrypted_data)

# thisdict = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }
# encrypt_dictionary(thisdict)