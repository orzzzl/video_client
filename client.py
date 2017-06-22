from gateway_services import gateway_interface
from video_capture.video_interface import VideoInterface
from data_cleaner.cleaner import Cleaner
from data_cleaner.end_session_checker import EndSessionChecker
from uploader.video_uploader import VideoUploader
from threading import Thread
import os
from time import sleep
from datetime import datetime
from inventory import CAMERA_LIST

class client:
    def __init__(self):
        gateway_interface.init_gateways()
        self.session_id = -1
        self._vi = VideoInterface()
        self._vu = VideoUploader()
        self._cleaner = Cleaner()
        self._esc = EndSessionChecker()
        self.start_time = datetime.now()
        self.end_time = datetime.now()

        uploading_thread = Thread(target=self._vu.work)
        cleaning_thread = Thread(target=self._cleaner.work)
        esc_thread = Thread(target=self._esc.work)

        uploading_thread.start()
        cleaning_thread.start()
        esc_thread.start()

    def main(self):
        print('Initially recording is off, type "on" to turn it on and "off" to turn it off')
        print('type "exit" to quit')
        while True:
            line = input()

            if line == 'exit' or line == 'off':
                gateway_interface.stop_gateways()
                self._vi.stop()
                self.end_time = datetime.now()
                duration = self.end_time - self.start_time
                data = {
                    'session_id': self.session_id,
                    'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': str(duration),
                    'cameras': str(CAMERA_LIST)
                }
                self._esc.add_session_data(self.session_id, data)
                self._esc.add_session(self.session_id)
                self.session_id = -1


            if line == 'exit':
                sleep(1)
                os._exit(0)

            if line == 'on':
                gateway_interface.start_gateways()
                self.start_time = datetime.now()
                self.session_id = self._vu.create_session(self.start_time)
                self._vi.set_sission_id(self.session_id)
                self._vi.start()



if __name__ == '__main__':
    client_instance = client()
    client_instance.main()