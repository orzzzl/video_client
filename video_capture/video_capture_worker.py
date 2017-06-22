from datetime import datetime
from datetime import timedelta

import cv2

from inventory import VIDEO_FORMAT, VIDEO_DIMENTION, FRAME_RATE, RECORDING_INTERVAL, logging
from threading import Thread

from database_services.video_writer import VideoWriter


class VideoCaptureWorker:
    def __init__(self, gateway):
        self.gateway = gateway
        self.fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.idx = gateway.secret
        self.is_recording_on = False
        self.session_id = -1

    def turn_on_recording(self):
        self.is_recording_on = True

    def turn_off_recording(self):
        self.is_recording_on = False

    def set_file_name(self, start_time):
        self.file_name = ':'.join(str(start_time).split()) + ':' + str(self.idx) + VIDEO_FORMAT
        self.file_name = './data/' + self.file_name
        self.file_name = self.file_name.replace(':', '@')

    def record(self):
        while True:
            if not self.is_recording_on or not self.gateway.on:
                continue
            start_time = datetime.now()
            self.set_file_name(start_time)
            self.out = cv2.VideoWriter(self.file_name, self.fourcc, FRAME_RATE, VIDEO_DIMENTION)
            logging.info('start recording file: %s' % self.file_name)
            while self.is_recording_on and \
                    datetime.now() - start_time < timedelta(seconds=RECORDING_INTERVAL):
                if self.gateway.has_next():
                    frame = self.gateway.next()
                    self.out.write(frame)
            self.out.release()
            logging.info('end recording file: %s' % self.file_name)
            db_thread = Thread(target=self.write_to_db, args=(self.file_name, self.session_id, self.idx))
            db_thread.start()

    def write_to_db(self, filename, session_id, camera_idx):
        logging.info('start writing file to db: %s' % filename)
        assert session_id >= 0
        VideoWriter().write_video_to_db(datetime.now(), filename, session_id, camera_idx)
        logging.info('end writing file: %s' % filename)
