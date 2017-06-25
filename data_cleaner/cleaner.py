from database_services.video_writer import VideoWriter
from time import sleep
import os
from inventory import logging


class Cleaner:
    def __init__(self):
        self._vw = VideoWriter()

    def work(self):
        logging.info('cleaner starts working.')
        while True:
            sleep(3)
            to_be_cleaned = self._vw.get_all_tasks(1, 1)
            for entity in to_be_cleaned:
                os.remove(entity['file_path'])
                self._vw.clear_finished_task(entity['file_path'])
