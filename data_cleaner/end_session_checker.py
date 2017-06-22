from time import sleep
from database_services.video_writer import VideoWriter
from uploader.request_maker import RequestMaker
from inventory import logging

class EndSessionChecker:
    def __init__(self):
        self._sessions = set()
        self._vw = VideoWriter()
        self._session_to_data = {}

    def add_session_data(self, session_id, data):
        self._session_to_data[session_id] = data

    def add_session(self, session_id):
        self._sessions.add(session_id)

    def remove_session(self, session_id):
        self._sessions.remove(session_id)

    def work(self):
        logging.info("End Session Checker starts working.")
        while True:
            sleep(0.77)
            to_be_removed = []
            for s in self._sessions:
                if s >= 0:
                    res = self._vw.get_all_tasks_by_session(0, s)
                    if len(res) == 0:
                        print('session uploaded:', s)
                        to_be_removed.append(s)
                        RequestMaker.end_session(self._session_to_data[s])

            for s in to_be_removed:
                self.remove_session(s)
                del self._session_to_data[s]

