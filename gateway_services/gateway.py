import queue
import cv2
from threading import Thread
from inventory import logging, MAX_QUEUE_SIZE

class Gateway:
    def __init__(self, num_of_channels, camera_idx):
        self.secret = camera_idx
        assert num_of_channels == 1 or num_of_channels == 2
        self.on = False
        self._num_of_channels = num_of_channels
        self._queue0 = queue.Queue()

        if num_of_channels == 2:
            self._queue1 = queue.Queue()
            self._idxs = [0, 0]
        self._camera = cv2.VideoCapture(camera_idx)
        fetching_thread = Thread(target=self.fetch_from_camera)
        fetching_thread.start()


    def fetch_from_camera(self):
        while True:
            if (not self._camera.isOpened()) or (not self.on):
                continue
            # if self._queue0.qsize() >= MAX_QUEUE_SIZE:
            #     continue
            ret, frame = self._camera.read()
            assert ret
            self._queue0.put(frame)

    def set_on(self):
        logging.info('gateway_services ' + str(self.secret) + ' is on')
        logging.info('size ' + str(self._queue0.qsize()))
        self.on = True

    def set_off(self):
        logging.info('gateway_services ' + str(self.secret) + ' is off')
        self.on = False

    def has_next(self, channel_idx=0):
        if self._num_of_channels == 1:
            return not self._queue0.empty()
        other_idx = 1 - channel_idx
        if self._idxs[channel_idx] >= self._idxs[other_idx]:
            return not self._queue0.empty()
        else:
            return not self._queue1.empty()

    def next(self, channel_idx=0):
        assert self.has_next(channel_idx)
        if self._num_of_channels == 1:
            return self._queue0.get()
        other_idx = 1 - channel_idx
        if self._idxs[channel_idx] >= self._idxs[other_idx]:
            ans = self._queue0.get()
            self._queue1.put(ans)
        else:
            ans = self._queue1.get()
        self._idxs[channel_idx] += 1
        min_val = min(self._idxs[0], self._idxs[1])
        if min_val >= 1000:
            self._idxs[0] -= min_val
            self._idxs[1] -= min_val
        return ans
