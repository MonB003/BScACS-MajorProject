# Tests for the security.py methods
import base64
from Crypto.Random import get_random_bytes
from major_project_backend.security import encrypt_data, decrypt_data, encrypt_dictionary, decrypt_dictionary

# Random 256-bit AES key for tests
AES_KEY = get_random_bytes(32)

def test_encrypt_data():
    data = "This is test data"
    encrypted_data = encrypt_data(data, AES_KEY)

    # Check data type is dictionary with the AES fields
    assert isinstance(encrypted_data, dict)  
    assert 'iv' in encrypted_data
    assert 'tag' in encrypted_data
    assert 'ciphertext' in encrypted_data

    # Check encrypted values are base64 encoded strings
    for key in ['iv', 'tag', 'ciphertext']:
        assert isinstance(encrypted_data[key], str)
        # Check decoded value isn't empty
        assert len(base64.b64decode(encrypted_data[key])) > 0

def test_encrypt_and_decrypt():
    data = "Test data for encrypt and decrypt"
    encrypted_data = encrypt_data(data, AES_KEY)
    decrypted_data = decrypt_data(encrypted_data, AES_KEY)
    # Check that the original and decrypted values match
    assert decrypted_data == data

def test_encrypt_data_empty():
    data = ""
    encrypted_data = encrypt_data(data, AES_KEY)
    decrypted_data = decrypt_data(encrypted_data, AES_KEY)
    
    # Check that the original and decrypted values match
    assert decrypted_data == data

def test_encrypt_different_characters():
    data = "Abc123!@#"
    encrypted_data = encrypt_data(data, AES_KEY)
    decrypted_data = decrypt_data(encrypted_data, AES_KEY)

    # Check that the original and decrypted values match
    assert decrypted_data == data
    
def test_encrypt_decrypt_dictionary():
    user_id = "abc-123"
    orig_test_value = "abc"
    new_test_value = "abc"
    test_dict = {
        "user_id": user_id,
        "filename": "test.txt",
        "file_hash": {
            "original_value": orig_test_value,
            "new_value": new_test_value
        }
    }

    encrypted_dict = test_dict.copy()
    encrypt_dictionary(encrypted_dict)

    # Check user_id is the same
    assert encrypted_dict["user_id"] == user_id

    # Check encrypted values are dictionaries with AES fields
    assert isinstance(encrypted_dict["filename"], dict)
    assert 'iv' in encrypted_dict["filename"]
    assert 'tag' in encrypted_dict["filename"]
    assert 'ciphertext' in encrypted_dict["filename"]

    decrypted_dict = encrypted_dict.copy()
    decrypt_dictionary(decrypted_dict)

    # Check decrypted values match the original values
    assert decrypted_dict["filename"] == test_dict["filename"]
    assert decrypted_dict["file_hash"]["original_value"] == test_dict["file_hash"]["original_value"]
    assert decrypted_dict["file_hash"]["new_value"] == test_dict["file_hash"]["new_value"]
