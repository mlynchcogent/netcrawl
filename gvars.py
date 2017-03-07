import os
current_file_path = __file__
current_file_dir = os.path.dirname(__file__)

# Define the common timestamp format
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Define the filepath timestamp format
TIME_FORMAT_FILE = '%Y%m%d_%H%M%S'

# When a device fails to connect, try again with this much delay
DELAY_INCREASE = 0.3

# The delay factor s
BASE_DELAY = 1

# Set to false to get full tracebacks
RAISE_ERRORS = False

CRED_LIST = []

RUN_PATH = current_file_dir + '/runtime/' 
MAIN_DB_PATH = 'main'
DEVICE_DB_PATH = 'devices'
DEVICE_PATH = RUN_PATH + 'dev/'

