import hashlib
import base64

# Creates a hash for a file or password
def generate_hash(data):
    return hashlib.sha256(data).hexdigest()

# Returns a boolean of whether 2 hashes are the same
def compare_file_hashes(current_file_hash, new_file_hash):
    return current_file_hash == new_file_hash

def generate_chunked_hash(file_data, chunk_size=4096):
    hash_sequence = []
    hasher = hashlib.sha256()
    
    # Read the file in chunks
    for i in range(0, len(file_data), chunk_size):
        chunk = file_data[i:i+chunk_size]

        # Try decoding as UTF-8, or fallback to Base64
        try:
            chunk_formatted = chunk.decode('utf-8')
        except UnicodeDecodeError:
            # Use Base64 encoding for binary data
            chunk_formatted = base64.b64encode(chunk).decode('utf-8')
        # print("CHUNK", chunk_formatted)

        hasher.update(chunk)
        # Store hash for each chunk
        hash_sequence.append(hasher.hexdigest())
    
    # Final hash of the whole file
    file_hash = hasher.hexdigest()
    return file_hash, hash_sequence
