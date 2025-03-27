from home_automation.app.utils import count_lines, rotate_log

TEST_LOG_FILE_PATH = "tests/assets/example.log"


def test_count_lines():
    assert count_lines(TEST_LOG_FILE_PATH) == 19


def test_rotate_log(tmp_path):
    # Create a temporary log file with content
    log_file = tmp_path / "test.log"
    log_file.write_text("Sample log content")

    # Call the rotate_log function
    rotate_log(str(log_file))

    # Check that the original log file exists and is empty
    assert log_file.exists()
    assert log_file.read_text() == ""

    # Check that a rotated file with a timestamp exists
    rotated_files = list(tmp_path.glob("test_*.log"))
    assert len(rotated_files) == 1
    rotated_file = rotated_files[0]
    # Ensure that the rotated file ends with .log
    assert rotated_file.name.endswith(".log")
    # Ensure that it contains the original content
    assert rotated_file.read_text() == "Sample log content"
