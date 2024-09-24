import hashlib

# Creates a hash for a file
def generate_file_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()
# def generate_file_hash(file_path):
#     sha256_hash = hashlib.sha256()
#     with open(file_path, "rb") as f:
#         for byte_block in iter(lambda: f.read(4096), b""):
#             sha256_hash.update(byte_block)
#     return sha256_hash.hexdigest()