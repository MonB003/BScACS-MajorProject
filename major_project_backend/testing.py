import os, time

# Get env variable, default to "false", store as boolean
test_mode_env = os.getenv("TEST_MODE", "false")
TEST_MODE = True if test_mode_env.lower() == "true" else False
TIME_PRECISION = 4

# The test-times directory in this file's location
testing_dir = os.path.join(os.path.dirname(__file__), "test-times")
# Make sure test-times directory exists
os.makedirs(testing_dir, exist_ok=True)
# Test time file's path: test-times/testing_times_{os.name}.txt
TEST_FILE = os.path.join(testing_dir, f"testing_times_{os.name}.txt")

def record_test_time(method, start_time):
    if TEST_MODE is False:
        return
    
    # If program is being tested, record time taken
    end_time = time.perf_counter()  # End timer
    total_time = round(end_time - start_time, TIME_PRECISION)  # Round results
    print(f"Writing to {TEST_FILE}: {method} took {total_time} seconds")

    # Log time to a file
    write_test_time(method, total_time)
        
def write_test_time(method, total_time, program="Backend"):
    with open(TEST_FILE, "a") as file:
        file.write(f"{program} Method: {method}. Time: {total_time} seconds\n")