import hashlib

# Creates a hash for a file or password
def generate_hash(data):
    return hashlib.sha256(data).hexdigest()

# Returns a boolean of whether 2 hashes are the same
def compare_file_hashes(current_file_hash, new_file_hash):
    return current_file_hash == new_file_hash