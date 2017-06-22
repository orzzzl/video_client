import requests
from inventory import get_address
from random import randint
class RequestMaker:

    @staticmethod
    def upload(file_path, session_id, camera_idx):
        data = {
            'session_id': session_id,
            'camera_idx': camera_idx
        }
        file_name = file_path.split('/')[-1]
        url = get_address() + '/upload'
        files = {
            file_name: open(file_path, 'rb')
        }
        r = requests.post(url, files=files, data=data)
        return r

    @staticmethod
    def create_session(start_time):
        data = {
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'customer_id': randint(0, 11),
            'pod_id': 0
        }
        url = get_address() + '/createsession'
        r = requests.post(url, data)
        response = int(eval(r.content)['session_id'])
        return response

    @staticmethod
    def end_session(data):
        url = get_address() + '/endsession'
        requests.post(url, data)


if __name__ == '__main__':
    rm = RequestMaker()
    rm.create_session()