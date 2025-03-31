# Tests for the files.py methods related to DOCX files
import os
import pytest
from major_project_backend.files import compare_file_content, get_docx_text
from docx import Document

TEST_DIR = "testing_files"

# Create document and write lines to a file
def create_docx(file_path, lines):
    if isinstance(lines, str):  
        lines = lines.splitlines()

    doc = Document()
    for line in lines:
        doc.add_paragraph(line)
    doc.save(file_path)

@pytest.fixture
def test_docx_file():
    file_path = os.path.join(TEST_DIR, "test_docx.docx")
    create_docx(file_path, "Test line 1.\nTest line 2.")
    return file_path

@pytest.fixture
def test_docx_file_new():
    file_path = os.path.join(TEST_DIR, "test_docx_new.docx")
    create_docx(file_path, "New test line 1.\nNew test line 2.")
    return file_path

@pytest.fixture
def test_docx_file_add():
    file_path = os.path.join(TEST_DIR, "test_docx_add.docx")
    create_docx(file_path, "Test line 1.\nTest line 2.\nTest line 3.")
    return file_path

@pytest.fixture
def test_docx_file_remove():
    file_path = os.path.join(TEST_DIR, "test_docx_remove.docx")
    create_docx(file_path, "Test line 1.")
    return file_path

def test_compare_docx_line_change(test_docx_file, test_docx_file_new):
    with open(test_docx_file_new, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_docx_file, uploaded_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,2 @@"
    ]
    
    # Expected header size plus 4 lines: 2 lines in each file
    file_sizes = 2+2
    expected_size = len(expected_header) + file_sizes
    assert len(diff_result) == expected_size
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_docx_line_add(test_docx_file, test_docx_file_add):
    with open(test_docx_file_add, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_docx_file, uploaded_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,3 @@"
    ]
    
    # Expected header size plus 3 lines: 2 lines in original, 1 new line added
    file_sizes = 2+1
    expected_size = len(expected_header) + file_sizes
    assert len(diff_result) == expected_size
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_docx_line_remove(test_docx_file, test_docx_file_remove):
    with open(test_docx_file_remove, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_docx_file, uploaded_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1 @@"
    ]
    
    # Expected header size plus 2 lines: 1 same line from original, 1 line removed
    file_sizes = 2
    expected_size = len(expected_header) + file_sizes
    assert len(diff_result) == expected_size
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_docx_same(test_docx_file):
    with open(test_docx_file, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_docx_file, uploaded_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    # Check for no differences
    assert len(diff_result) == 0

def test_get_docx_text(test_docx_file):
    text_result = get_docx_text(test_docx_file)
    # Check the file has 2 lines
    assert len(text_result) == 2

def test_get_docx_text_add(test_docx_file_add):
    text_result = get_docx_text(test_docx_file_add)
    # Check the file has 3 lines
    assert len(text_result) == 3

def test_get_docx_text_remove(test_docx_file_remove):
    text_result = get_docx_text(test_docx_file_remove)
    # Check the file has 1 line
    assert len(text_result) == 1
