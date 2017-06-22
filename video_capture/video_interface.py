from video_capture.video_capture_worker import VideoCaptureWorker
from gateway_services.gateway_interface import get_gateways, start_gateways
from threading import Thread
from uploader.request_maker import RequestMaker

class VideoInterface:
    def __init__(self):
        self.gateways = get_gateways()
        self.workers = []
        for g in self.gateways:
            self.workers.append(VideoCaptureWorker(g))

        for worker in self.workers:
            working_thread = Thread(target=worker.record)
            working_thread.start()


    def start(self):
        for worker in self.workers:
            worker.turn_on_recording()

    def stop(self):
        for worker in self.workers:
            worker.turn_off_recording()

    def set_sission_id(self, session_id):
        for worker in self.workers:
            worker.session_id = session_id


if __name__ == '__main__':
    start_gateways()
    vi = VideoInterface()
    session_id = RequestMaker().create_session()
    vi.set_sission_id(session_id)
    vi.start()