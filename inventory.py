import logging

# Network Config
SERVER_ADDRESS = '192.168.0.18'
PORT = 8999

def get_address():
    return 'http://' + SERVER_ADDRESS + ':' + str(PORT)


# Video Recording Preference
VIDEO_FORMAT = '.avi'
FRAME_RATE = 20.0
VIDEO_DIMENTION = (640, 480)
RECORDING_INTERVAL = 5

# Gateway
MAX_QUEUE_SIZE = 100
CAMERA_LIST = [0, 1]

# Logging Config
logging.basicConfig(
    filename="clientlog.txt",
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Video Database Table
VIDEO_TABLE_NAME = 'video_uploading_tasks'