from difflib import unified_diff
import docx
import PyPDF2
import os, time
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

def parse_file_by_type(file, filename, file_type):
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
