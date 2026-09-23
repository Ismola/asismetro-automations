from utils.config import DOWNLOAD_DIR, MAX_CONTENT_LENGTH, METRICS_PORT


def test_runtime_defaults():
    assert DOWNLOAD_DIR.endswith("temp_downloads")
    assert MAX_CONTENT_LENGTH == 10 * 1024 * 1024
    assert METRICS_PORT == 9090
