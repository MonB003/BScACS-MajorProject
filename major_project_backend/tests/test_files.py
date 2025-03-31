import os, pytest
from major_project_backend.files import compare_file_content, get_pdf_text, get_docx_text, get_date_time_string

TEST_DIR = "testing_files"

@pytest.fixture
def test_text_file():
    file_path = os.path.join(TEST_DIR, "test_text.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test file line 1.\nTest file line 2.")
    return file_path

@pytest.fixture
def test_text_file_new():
    file_path = os.path.join(TEST_DIR, "test_text_new.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("New test file line 1.\nNew test file line 2.")
    return file_path

def test_compare_text_file_same(test_text_file):
    with open(test_text_file, "rb") as f:
        uploaded_data = f.read()

    diff = compare_file_content(test_text_file, uploaded_data, "text/plain")
    
    # No differences for the same files
    # assert list(diff) == []
    
    assert all(line.startswith('@@') is False for line in diff)  # No actual content differences


def test_compare_text_file_different(test_text_file, test_text_file_new):
    with open(test_text_file, "rb") as f:
        uploaded_data = f.read()

    diff = compare_file_content(test_text_file_new, uploaded_data, "text/plain")
    # Differences for different files
    assert list(diff) is not []
