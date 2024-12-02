from difflib import unified_diff
import docx
import PyPDF2
import os, time
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from io import BytesIO
import difflib

def parse_file_info_by_type(file, filename, file_type):
    print("FILE TYPE", file_type)
    # print("FILE NAME", filename)
    # print("FILE", file)

    if file_type == "text/plain" or file_type == "text/csv":
        print("TEXT FILE")
        file_data = os.stat(filename)
        file_permissions = oct(file_data.st_mode)[-3:]
        file_created = time.ctime(file_data.st_ctime)
        file_last_modified = time.ctime(file_data.st_mtime)
        file_last_accessed = time.ctime(file_data.st_atime)
        print("Permissions", file_permissions)
        print("Creation time", file_created)
        print("Modified time", file_last_modified)
        print("Accessed time", file_last_accessed)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Parse DOCX file
        print("DOCX OR EXCEL FILE")
        doc_file = docx.Document(file)
        doc_properties = doc_file.core_properties
        print("Title", doc_properties.title)
        print("Author", doc_properties.author)
        print("Subject", doc_properties.subject)
        print("Created", doc_properties.created)
        print("Last modified", doc_properties.last_modified_by)
        print("Modified", doc_properties.modified)

    elif file_type == "application/pdf":
        print("PDF FILE")
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_data = pdf_reader.metadata
        print(f"Number of pages: {len(pdf_reader.pages)}")

        # print(pdf_data.author)
        # print(pdf_data.creator)
        # print(pdf_data.producer)
        # print(pdf_data.subject)
        # print(pdf_data.title)
        if (pdf_data):
            print("DATA")
            for key, value in pdf_data.items():
                print(f"{key[1:]}: {value}")
        else:
            print("No PDF metadata found for this file.")
    
    elif file_type == "image/jpeg" or file_type == "image/png":
        # ***NOT getting any data
        image = Image.open(filename)
        exif_data = image._getexif()
        if exif_data is not None:
            image_data = {}
            for tag, value in image_data.items():
                tag_name = TAGS.get(tag, tag)
                image_data[tag_name] = value
            for key, value in image_data.items():
                print(f"{key}: {value}")
        else:
            print("No image metadata found for this file.")
    else:
        print("File type not supported")
        # return None  # Unsupported file type

def parse_file_content(file_type, local_file, new_file):
    print("FILE TYPE:", file_type)
    
    # Generic File Metadata
    file_stats = os.stat(local_file)
    print(f"Permissions: {oct(file_stats.st_mode)[-3:]}")
    print(f"Created: {time.ctime(file_stats.st_ctime)}")
    print(f"Last Modified: {time.ctime(file_stats.st_mtime)}")
    print(f"Last Accessed: {time.ctime(file_stats.st_atime)}")

    # Read local file content
    print("--- FILE CONTENT ---")
    if file_type in ["text/plain", "text/csv"]:
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            # print("\n".join(content[:5]))  # Print first 5 lines
            print("\n".join(content))
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(local_file)
        print("Title:", doc.core_properties.title or "No title")
        for para in doc.paragraphs: # [:5]:  # First 5 paragraphs
            print(para.text)
    elif file_type == "application/pdf":
        reader = PyPDF2.PdfReader(local_file)
        for page in reader.pages: # [:5]:  # First 5 pages
            print(page.extract_text())
    else:
        print("Unsupported file type.")

def parse_uploaded_file_content(file_type, uploaded_file):
    print("UPLOADED FILE TYPE:", file_type)
    print("--- UPLOADED FILE CONTENT ---")
    if file_type in ["text/plain", "text/csv"]:
        data = uploaded_file.decode('utf-8').split('\r\n') # Separate by line
        for line in data:
            print(line)  # Print each line
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(BytesIO(uploaded_file))  # Read DOCX from memory
        print("Title:", doc.core_properties.title or "No title")
        for para in doc.paragraphs:
            print(para.text)
    elif file_type == "application/pdf":
        reader = PyPDF2.PdfReader(BytesIO(uploaded_file))  # Read PDF from memory
        for page in reader.pages:
            print(page.extract_text())
    else:
        print("Unsupported file type.")

def compare_file_metadata(local_file_path, uploaded_file_data, file_type):
    print("FILE TYPE:", file_type)
    # Read local file
    with open(local_file_path, 'r', encoding='utf-8') as local_file:
        local_lines = local_file.readlines()
    
    # Read uploaded file data from memory if it's a text file
    # if file_type in ["text/plain", "text/csv"]:
    if file_type.startswith("text/"):
        uploaded_lines = uploaded_file_data.decode('utf-8').splitlines(keepends=True)
    else:
        print("Unsupported file type for text comparison.")
        return None
    
    # Use difflib to compare lines
    diff = difflib.unified_diff(local_lines, uploaded_lines, 
                                fromfile='local_file', 
                                tofile='uploaded_file', 
                                lineterm='')
    
    # # Print the differences line by line
    # print("DIFFERENCES:")
    # for line in diff:
    #     print(line)
        
    return diff

def save_file_changes(log_dir, user_id, filename, metadata, differences):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    name = filename.split('.')[0] # Get filename without the extension
    log_filename = os.path.join(log_dir, f"{name}-changes.txt")
    # print("FILE CHANGE PATH:", log_filename)
    
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(f"Filename: {filename}\n")
        f.write(f"User ID: {user_id}\n")
        # f.write(f"Comparison Date: {datetime.utcnow()}\n")
              
        # Parse metadata
        f.write(f"File metadata: \n")
        for key, value in metadata.items():
            # Print original and new values
            if isinstance(value, dict) and 'original_value' in value and 'new_value' in value:
                key_string = str(key).replace('_', ' ')
                f.write(f"{key_string}:\n")
                f.write(f"\tOriginal: {value['original_value']}\n")
                f.write(f"\tNew: {value['new_value']}\n")
        
        f.write("-" * 40 + "\n")
        f.write(f"File content metadata changes: \n")
        f.writelines(differences)
        # for current_line in differences:
        #     f.write(f"{current_line}")

    print(f"Saved diff to {log_filename}")

# def parse_file_data(file_data, file_type):
#     print("Parsing file data...")

#     if file_type in ["text/plain", "text/csv"]:
#         content = file_data.decode('utf-8')  # Decode binary data into a string
#         lines = content.splitlines()  # Split into lines
#         print("\n".join(lines))  # Print first 5 lines for preview
#         return lines  # Return list of lines for comparison

#     elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = docx.Document(BytesIO(file_data))  # Read DOCX from memory
#         paragraphs = [para.text for para in doc.paragraphs]
#         print("\n".join(paragraphs[:5]))  # Print first 5 paragraphs
#         return paragraphs  # Return list of paragraphs for comparison

#     elif file_type == "application/pdf":
#         reader = PyPDF2.PdfReader(BytesIO(file_data))  # Read PDF from memory
#         pages = [page.extract_text() for page in reader.pages]
#         print("\n".join(pages))  # Print text from the first page
#         return pages  # Return list of page text for comparison

#     else:
#         print("Unsupported file type.")
#         return None

# def compare_files(old_file_data, new_file_data, file_type):
#     # Parse both files
#     old_content = parse_file_data(old_file_data, file_type)
#     new_content = parse_file_data(new_file_data, file_type)

#     if isinstance(old_content, list) and isinstance(new_content, list):
#         # Compare line-by-line or paragraph-by-paragraph
#         diff = unified_diff(old_content, new_content, lineterm="")
#         print("\n".join(list(diff)))
#     elif isinstance(old_content, dict) and isinstance(new_content, dict):
#         # Compare metadata for images
#         differences = {key: (old_content.get(key), new_content.get(key))
#                        for key in set(old_content) | set(new_content)
#                        if old_content.get(key) != new_content.get(key)}
#         print("Metadata differences:", differences)
#     else:
#         print("Unable to compare content.")
