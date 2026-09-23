import os
from dotenv import load_dotenv

# Carga el .env desde la ruta absoluta
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Global variables
STAGE = (os.getenv("STAGE") or 'staging').lower()
VALID_TOKEN = os.getenv("VALID_TOKEN") or ("sample" if STAGE != "production" else None)
DOWNLOAD_DIR = os.path.abspath(os.getenv("DOWNLOAD_DIR", "temp_downloads"))
PORT = int(os.getenv("PORT", 3000))
METRICS_PORT = int(os.getenv("METRICS_PORT", 9090))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
DOWNLOAD_MAX_TIMEOUT = int(os.getenv("DOWNLOAD_MAX_TIMEOUT", 4))


def validate_runtime_configuration():
    if STAGE == "production" and (not VALID_TOKEN or VALID_TOKEN == "sample"):
        raise RuntimeError(
            "VALID_TOKEN must be set to a non-default value in production"
        )
