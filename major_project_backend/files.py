import docx
# import PyPDF2
from pypdf import PdfReader
import os, stat
from datetime import datetime
from io import BytesIO
import difflib

def fix_newlines(lines):
    # Crate consistent "\n" newline characters
        return [line.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n" for line in lines]
    # return [line.replace("\r\n", "\n").replace("\\n", "\n").strip() for line in lines]

def compare_file_content(local_file_path, uploaded_file_data, file_type):
    # Read uploaded file data from memory if it's a text file
    if file_type.startswith("text/"):
        # Read local file
        with open(local_file_path, 'r', encoding='utf-8') as local_file:
            local_lines = local_file.readlines()
        uploaded_lines = uploaded_file_data.decode('utf-8').splitlines(keepends=True)
        
    elif file_type == "application/pdf":
        # Extract text from both PDF files
        with open(local_file_path, "rb") as local_file:
            local_lines = get_pdf_text(local_file)
        uploaded_lines = get_pdf_text(BytesIO(uploaded_file_data))
        print("LOCAL LINES:", [repr(line) for line in local_lines])
        print("UPLOADED LINES:", [repr(line) for line in uploaded_lines])

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Extract text from both DOCX files
        local_lines = get_docx_text(local_file_path)
        uploaded_lines = get_docx_text(BytesIO(uploaded_file_data))
        
    else:
        print("Unsupported file type for text comparison.")
        return None
    
    local_lines = fix_newlines(local_lines)
    uploaded_lines = fix_newlines(uploaded_lines)
    print("NORMALIZED LOCAL LINES:", [repr(line) for line in local_lines])
    print("NORMALIZED UPLOADED LINES:", [repr(line) for line in uploaded_lines])

    # Use difflib to compare lines
    # diff = difflib.ndiff(local_lines, uploaded_lines)

    diff = difflib.unified_diff(local_lines, uploaded_lines, 
                                fromfile='initial_file', 
                                tofile='uploaded_file', 
                                lineterm='')
    return diff

# Get text content from a PDF
# def get_pdf_text(pdf_file):
#     reader = PyPDF2.PdfReader(pdf_file)
#     text_lines = []
#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             text_lines.extend(text.splitlines(keepends=True)) # Split text into lines, keep the line break characters
#     return text_lines

def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)  # Use PdfReader from pypdf
    text_lines = []
    for page in reader.pages:
        # text = page.extract_text()
        text = page.extract_text(layout=True)
        print("TEXT", text)
        if text:
            # print("TEXT TRUE")
            # text = text.replace("\\n", "\n")  
            text_lines.extend(text.splitlines(keepends=True))  # Keep line breaks
    print("TEXT LINES", text_lines)
    return text_lines

# Get text content from a Word docx
def get_docx_text(docx_file):
    doc = docx.Document(docx_file)
    text_lines = [para.text + "\n" for para in doc.paragraphs]  # Keep them in lines
    return text_lines

def get_date_time_string():
    # Get current date and time
    now = datetime.now()
    
    # Format: YYYY-MM-DD-H-M-S
    datetime_formatted = now.strftime("%Y-%m-%d-%H-%M-%S")
    return datetime_formatted

def save_file_changes(log_dir, user_id, filename, metadata, differences):
    # Create directory path
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create path to file changes file
    name = filename.split('.')[0] # Get filename without the extension
    datetime_string = get_date_time_string() # Add date and time to make filename unique
    log_filename = os.path.join(log_dir, f"{name}-changes-{datetime_string}.txt")
    
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(f"Filename: {filename}\n")
        f.write(f"User ID: {user_id}\n")
              
        # Parse metadata
        f.write(f"File metadata: \n")
        for key, value in metadata.items():
            # Print original and new values
            if isinstance(value, dict) and 'original_value' in value and 'new_value' in value:
                key_string = str(key).replace('_', ' ')
                f.write(f"{key_string}:\n")
                f.write(f"\tOriginal: {value['original_value']}\n")
                f.write(f"\tNew: {value['new_value']}\n")
        
        f.write("-" * 35 + "\n")
        f.write(f"File content changes: \n")
        if differences is not None:
            for current_line in differences:
                f.write(f"{current_line}\n")
        else:
            f.write("None.")

    # Make file read-only
    os.chmod(log_filename, stat.S_IREAD)
    
    print(f"Saved file changes to {log_filename}")
    return log_filename