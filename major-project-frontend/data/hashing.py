import hashlib
import base64

# Creates a hash for a file or password
def generate_hash(data):
    return hashlib.sha256(data).hexdigest()