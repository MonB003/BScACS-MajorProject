import os, pytest

@pytest.fixture(scope="session", autouse=True)
def create_testing_files_directory():
    """Check that testing_files directory exists before running tests, otherwise create it."""
    testing_dir = os.path.join(os.path.dirname(__file__), "testing_files")
    os.makedirs(testing_dir, exist_ok=True)
