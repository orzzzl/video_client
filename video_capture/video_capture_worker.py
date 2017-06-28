from datetime import datetime
from datetime import timedelta

import cv2

from inventory import VIDEO_FORMAT, VIDEO_DIMENTION, RECORDING_INTERVAL, logging
from threading import Thread

from database_services.video_writer import VideoWriter


class VideoCaptureWorker:
    def __init__(self, gateway):
        self._vw = VideoWriter()
        self.gateway = gateway
        self.fourcc = cv2.VideoWriter_fourcc(*'VP80')
        self.idx = gateway.secret
        self.is_recording_on = False
        self.session_id = -1
        self.start_time = datetime.now()
        self.cur_time = datetime.now()

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
            if not self.is_recording_on:
                continue
            frame_buffer = []
            self.start_time = datetime.now()
            self.set_file_name(self.start_time)
            logging.info('start recording file: %s' % self.file_name)
            while self.is_recording_on:
                self.cur_time = datetime.now()
                if self.cur_time - self.start_time >= timedelta(seconds=RECORDING_INTERVAL):
                    break
                if self.gateway.has_next():
                    frame = self.gateway.next()
                    if frame['session_id'] == self.session_id:
                        frame_buffer.append(frame)
            logging.info(self.gateway.has_next())
            if not self.is_recording_on:
                while self.gateway.has_next():
                    frame = self.gateway.next()
                    if frame['session_id'] != self.session_id:
                        break
                    frame_buffer.append(frame)
            logging.info('end recording file: %s' % self.file_name)
            buffer_copy = frame_buffer[:]
            db_thread = Thread(target=self.create_video_file, args=(self.file_name, self.session_id, buffer_copy))
            db_thread.start()
            del frame_buffer


    def create_video_file(self, file_name, session_id, frame_buffer):
        self._vw.write_task_to_db(datetime.now(), file_name, session_id, self.idx, 0)
        total_frames = len(frame_buffer)
        if (frame_buffer[-1]['session_id'] != frame_buffer[0]['session_id']):
            logging.info(frame_buffer[-1]['session_id'])
            logging.info(frame_buffer[0]['session_id'])
            assert(False)
        total_secs = (frame_buffer[-1]['time'] - frame_buffer[0]['time']).total_seconds()
        if total_secs == 0:
            return
        frame_rate = total_frames * 1.0 / total_secs
        logging.info(self.session_id)
        logging.info(frame_rate)
        logging.info(file_name)
        logging.info(len(frame_buffer))
        for i in range(3):
            logging.info(str(i) + "  " + str(frame_buffer[i]['time']) + "   " + str(frame_buffer[i]["session_id"]))
            logging.info(str(-i) + "  " + str(frame_buffer[-i]['time']) + "   " + str(frame_buffer[-i]["session_id"]))
        out = cv2.VideoWriter(file_name, self.fourcc, float(frame_rate), VIDEO_DIMENTION)
        for frame in frame_buffer:
            out.write(frame['frame'])
        out.release()
        self._vw.set_complete(file_name, 0)
       #self.write_to_db(file_name, session_id)



    def write_to_db(self, filename, session_id):
        logging.info('start writing file to db: %s' % filename)
        assert session_id >= 0
        self._vw.write_task_to_db(datetime.now(), filename, session_id, self.idx, 1)
        logging.info('end writing file: %s' % filename)
