from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64, os, json
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env file variables
load_dotenv()
AES_KEY = os.getenv("AES_KEY")
key = base64.b64decode(AES_KEY)  # Decode the base64 string to bytes
# print(f"Key length: {len(key)} bytes") 

# Connect to MongoDB database
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['toolkit_db']
collection = db["initial_files"]

# ** Encrypt and Save File **
def encrypt_file(filename, file_dir, user_id):
    with open(filename, "rb") as f: # Open full file path
        data = f.read()  # Read file content

    init_vector = get_random_bytes(12)  # AES-GCM IV
    cipher = AES.new(key, AES.MODE_GCM, nonce=init_vector)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # encrypted_filename = filename + ".encrypt"  # Save encrypted file
    encrypted_filename = "encrypt-" + filename # Save encrypted file
    name = os.path.basename(filename) # Get filename without entire path
    encrypted_filename = os.path.join(file_dir, f"encrypt-{name}")
    if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    
    with open(encrypted_filename, "wb") as f:
        f.write(ciphertext)

    # Store metadata in MongoDB
    file_metadata = {
        "filename": os.path.basename(filename),
        "user_id": user_id,
        "iv": base64.b64encode(init_vector).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
    }
    # collection.insert_one(file_metadata)
    
    collection.update_one(
        {"filename": os.path.basename(filename), "user_id": user_id},  # Find by filename & user
        {"$set": file_metadata},  # Update IV and tag
        upsert=True  # Insert if not found
    )
    print(f"File {encrypted_filename} encrypted and stored securely.")

# ** Decrypt and Retrieve File **
def decrypt_file(filename, file_dir, user_id):
    print(f"File to decrypt: {filename}")
    print(f"File to decrypt: {os.path.basename(filename)}")

    file_metadata = collection.find_one({"filename": os.path.basename(filename), "user_id": user_id})
    if not file_metadata:
        print("Error: Metadata not found in database.")
        return

    # encrypted_filename = filename + ".encrypt"  # Save encrypted file
    # encrypted_filename = "encrypt-" + filename
    
    name = os.path.basename(filename) # Get filename without entire path
    encrypted_filename = os.path.join(file_dir, f"encrypt-{name}")
    if not os.path.exists(encrypted_filename):
        print("Error: Encrypted file not found.")
        return

    print(f"File to decrypt: {encrypted_filename}")

    with open(encrypted_filename, "rb") as f:
        ciphertext = f.read()

    # Decode IV and tag from database
    init_vector = base64.b64decode(file_metadata["iv"])
    tag = base64.b64decode(file_metadata["tag"])

    cipher = AES.new(key, AES.MODE_GCM, nonce=init_vector)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        print(f"DECRYPT DATA: {decrypted_data}")

        # original_filename = filename + ".decrypt"
        # original_filename = "decrypt-" + filename
        original_filename = os.path.join(file_dir, f"decrypt-{name}")
        print(f"File name: {original_filename}")

        with open(original_filename, "wb") as f:
            f.write(decrypted_data)
        print(f"File decrypted and saved as {original_filename}")
    except ValueError:
        print("Decryption failed! Data may have been tampered with.")

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
