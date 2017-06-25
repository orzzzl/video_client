from uploader.request_maker import RequestMaker
from database_services.video_writer import VideoWriter
from inventory import logging
from threading import Thread


class VideoUploader(RequestMaker):
    def __init__(self):
        RequestMaker.__init__(self)
        self._video_writer = VideoWriter()

    def process_file(self, f, s, c):
        logging.info('uploading: %s' % f)
        RequestMaker.upload(f, s, c)
        logging.info('end uploading %s' % f)
        self._video_writer.set_complete(f, 1)

    def work(self):
        logging.info('upload worker start working')
        while True:
            tasks = []
            to_dos = self._video_writer.get_all_tasks(0, 1)
            for entity in to_dos:
                t = Thread(target=self.process_file, args=(entity['file_path'], entity['session_id'], entity['camera_idx']))
                tasks.append(t)

            for t in tasks:
                t.start()

            for t in tasks:
                t.join()

if __name__ == '__main__':
    vu = VideoUploader()
    vu.work()