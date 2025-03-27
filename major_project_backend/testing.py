import os, time

# Get env variable, default to "false", store as boolean
test_mode_env = os.getenv("TEST_MODE", "false")
TEST_MODE = True if test_mode_env.lower() == "true" else False
TIME_PRECISION = 4
TEST_FILE = f"testing_times_{os.name}.txt"

def record_test_time(method, start_time):
    if TEST_MODE is False:
        return
    
    # If program is being tested, record time taken
    end_time = time.perf_counter()  # End timer
    total_time = round(end_time - start_time, TIME_PRECISION)  # Round results

    print(f"Writing to {TEST_FILE}: {method} took {total_time} seconds")

    # Log time to a file
    with open(TEST_FILE, "a") as file:
        file.write(f"Method: {method}. Time: {total_time} seconds\n")