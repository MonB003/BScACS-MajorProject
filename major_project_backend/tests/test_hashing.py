# Tests for the hashing.py methods
from major_project_backend.hashing import generate_hash, compare_file_hashes

def test_generate_hash():
    password = "password"
    encoded_password = password.encode('utf-8')
    hash_password = generate_hash(encoded_password)
    assert hash_password is not None
    assert len(hash_password) > 0

def test_generate_hash_empty():
    password = ""
    encoded_password = password.encode('utf-8')
    hash_password = generate_hash(encoded_password)
    # Should still generate a hash
    assert hash_password is not None
    assert len(hash_password) > 0

def test_generate_hash_numbers():
    password = "12345"
    encoded_password = password.encode('utf-8')
    hash_password = generate_hash(encoded_password)
    assert hash_password is not None
    assert len(hash_password) > 0
    
def test_generate_hash_special_characters():
    password = "!@#$%^&*()_+="
    encoded_password = password.encode('utf-8')
    hash_password = generate_hash(encoded_password)
    assert hash_password is not None
    assert len(hash_password) > 0
    
def test_generate_hash_characters():
    password = "Abc123!@#"
    encoded_password = password.encode('utf-8')
    hash_password = generate_hash(encoded_password)
    assert hash_password is not None
    assert len(hash_password) > 0

def test_compare_file_hashes_same():
    current_file_hash = "hash"
    new_file_hash = "hash"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is True

def test_compare_file_hashes_same_characters():
    current_file_hash = "Abc123!@#"
    new_file_hash = "Abc123!@#"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is True
   
def test_compare_file_hashes_same_empty():
    current_file_hash = ""
    new_file_hash = ""
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is True
     
def test_compare_file_hashes_different_end():
    current_file_hash = "hash1"
    new_file_hash = "hash2"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is False

def test_compare_file_hashes_different_start():
    current_file_hash = "hash"
    new_file_hash = "cash"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is False

def test_compare_file_hashes_different_middle():
    current_file_hash = "Ab123!"
    new_file_hash = "Abc123!"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is False

def test_compare_file_hashes_different_length():
    current_file_hash = "Abc123"
    new_file_hash = "Abcd1234"
    comparison_result = compare_file_hashes(current_file_hash, new_file_hash)
    assert comparison_result is False
