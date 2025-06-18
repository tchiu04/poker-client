import os

# Environment detection
IS_DOCKER = os.path.exists('/.dockerenv')

# Base paths for different environments
DOCKER_BASE_PATH = "/app/output"
LOCAL_BASE_PATH = "output"

# Use appropriate base path based on environment
BASE_PATH = DOCKER_BASE_PATH if IS_DOCKER else LOCAL_BASE_PATH

# Ensure local output directory exists
if not IS_DOCKER:
    os.makedirs(BASE_PATH, exist_ok=True)

# Network configuration
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5000

START_MONEY = 1000
RESULT_FILE = os.path.join(BASE_PATH, 'game_result.log')