import os, pytest
from major_project_backend.files import compare_file_content, get_pdf_text, get_docx_text, get_date_time_string

TEST_DIR = "testing_files"

@pytest.fixture
def test_text_file():
    file_path = os.path.join(TEST_DIR, "test_text.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test line 1.\nTest line 2.")
    return file_path

@pytest.fixture
def test_text_file_new():
    file_path = os.path.join(TEST_DIR, "test_text_new.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("New test line 1.\nNew test line 2.")
    return file_path

@pytest.fixture
def test_text_file_add():
    file_path = os.path.join(TEST_DIR, "test_text_add.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test line 1.\nTest line 2.\nTest line 3.")
    return file_path

@pytest.fixture
def test_text_file_remove():
    file_path = os.path.join(TEST_DIR, "test_text_remove.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test line 1.")
    return file_path

def test_compare_text_file_line_change(test_text_file, test_text_file_new):
    with open(test_text_file_new, "rb") as f:
        uploaded_data = f.read()

    diff_result = compare_file_content(test_text_file, uploaded_data, "text/plain")
    diff_result_list = list(diff_result)
    print("RESULT LIST", diff_result_list)
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,2 @@"
    ]
    
    # Expected header size plus 4 lines: 2 lines in each file
    file_sizes = 2+2
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result_list) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result_list[index].strip() == expected_header[index]
    
    # Differences for different files
    # assert list(diff) is not []


def test_compare_text_file_line_add(test_text_file, test_text_file_add):
    with open(test_text_file_add, "rb") as f:
        uploaded_data = f.read()

    diff_result = compare_file_content(test_text_file, uploaded_data, "text/plain")
    diff_result_list = list(diff_result)
    print("RESULT LIST", diff_result_list)
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,3 @@"
    ]
    
    # Expected header size plus 5 lines: 2 lines for original, 3 lines for new file
    file_sizes = 2+3
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result_list) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result_list[index].strip() == expected_header[index]
    
def test_compare_text_file_line_remove(test_text_file, test_text_file_remove):
    with open(test_text_file_remove, "rb") as f:
        uploaded_data = f.read()

    diff_result = compare_file_content(test_text_file, uploaded_data, "text/plain")
    diff_result_list = list(diff_result)
    print("RESULT LIST", diff_result_list)
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1 @@"
    ]
    
    # Expected header size plus 5 lines: 2 lines for original, 1 line for new file
    file_sizes = 2+1
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result_list) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result_list[index].strip() == expected_header[index]
    
def test_compare_text_file_same(test_text_file):
    with open(test_text_file, "rb") as f:
        uploaded_data = f.read()

    diff_result = compare_file_content(test_text_file, uploaded_data, "text/plain")
    diff_result_list = list(diff_result)
    print("RESULT LIST", diff_result_list)
    expected_header = [
        "--- initial_file",
        "+++ uploaded_file",
        "@@ -1,2 +1,2 @@"
    ]
    
    # Expected header size plus 4 lines: line 1 printed twice, line 2 printed once since it's the same
    file_sizes = 2+1
    expected_size = len(expected_header) + file_sizes
    # Check size of diff result
    assert len(diff_result_list) == expected_size
    # Check that header matches expected values
    for index in range(3):
        assert diff_result_list[index].strip() == expected_header[index]
    
    
    # No differences for the same files
    # assert list(diff) == []
    # assert all(line.startswith('@@') is False for line in diff)  # No actual content differences
