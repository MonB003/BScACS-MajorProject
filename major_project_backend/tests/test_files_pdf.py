# Tests for the files.py methods related to PDF files
import os, pytest
from reportlab.pdfgen import canvas
from major_project_backend.files import compare_file_content, get_pdf_text

TEST_DIR = "testing_files"

# Create PDF and write lines to a file
def create_pdf(file_path, lines):
    # Convert string to list
    if isinstance(lines, str):  
        lines = lines.splitlines()

    c = canvas.Canvas(file_path)
    # Position to start
    text_object = c.beginText(50, 800)

    for line in lines:
        # Write each line to the file
        text_object.textLine(line)

    c.drawText(text_object)
    c.save()
    
@pytest.fixture
def test_pdf_file():
    file_path = os.path.join(TEST_DIR, "test_pdf.pdf")
    create_pdf(file_path, "Test line 1.\nTest line 2.")
    return file_path

@pytest.fixture
def test_pdf_file_new():
    file_path = os.path.join(TEST_DIR, "test_pdf_new.pdf")
    create_pdf(file_path, "New test line 1.\nNew test line 2.")
    return file_path

@pytest.fixture
def test_pdf_file_add():
    file_path = os.path.join(TEST_DIR, "test_pdf_add.pdf")
    create_pdf(file_path, "Test line 1.\nTest line 2.\nTest line 3.")
    return file_path

@pytest.fixture
def test_pdf_file_remove():
    file_path = os.path.join(TEST_DIR, "test_pdf_remove.pdf")
    create_pdf(file_path, "Test line 1.")
    return file_path

def test_compare_pdf_line_change(test_pdf_file, test_pdf_file_new):
    with open(test_pdf_file_new, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_pdf_file, uploaded_data, "application/pdf"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,2 @@"
    ]
    
    # Expected header size plus 4 lines: 2 lines in each file
    file_sizes = 2+2
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_pdf_line_add(test_pdf_file, test_pdf_file_add):
    with open(test_pdf_file_add, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_pdf_file, uploaded_data, "application/pdf"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,3 @@"
    ]
    
    # Expected header size plus 3 lines: 2 lines in original, 1 new line added
    file_sizes = 2+1
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_pdf_line_remove(test_pdf_file, test_pdf_file_remove):
    with open(test_pdf_file_remove, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_pdf_file, uploaded_data, "application/pdf"))
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1 @@"
    ]
    
    # Expected header size plus 2 lines: 1 same line from original, 1 line removed
    file_sizes = 2
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result[index].strip() == expected_header[index]

def test_compare_pdf_same(test_pdf_file):
    with open(test_pdf_file, "rb") as f:
        uploaded_data = f.read()

    diff_result = list(compare_file_content(test_pdf_file, uploaded_data, "application/pdf"))
    # Check for no differences
    assert len(diff_result) == 0

def test_get_pdf_text(test_pdf_file):
    text_result = get_pdf_text(test_pdf_file)
    # Check the file has 2 lines
    assert len(text_result) == 2

def test_get_pdf_text_add(test_pdf_file_add):
    text_result = get_pdf_text(test_pdf_file_add)
    # Check the file has 3 lines
    assert len(text_result) == 3

def test_get_pdf_text_remove(test_pdf_file_remove):
    text_result = get_pdf_text(test_pdf_file_remove)
    # Check the file has 1 line
    assert len(text_result) == 1
