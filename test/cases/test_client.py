import unittest
import subprocess
import requests
import time
import json

from glockr.config import PORT
from glockr.client import GClient

BASE_URL = 'http://127.0.0.1:{}'.format(PORT)


class TestClient(unittest.TestCase):
    _server_process = None

    @staticmethod
    def get_current_dict() -> dict:
        target_url = BASE_URL + '/res'
        resp = requests.get(target_url)
        resp_dict = json.loads(resp.text)
        return resp_dict

    @classmethod
    def setUpClass(cls):
        super(TestClient, cls).setUpClass()
        cls._server_process = subprocess.Popen('python -m glockr.server start', shell=True)
        time.sleep(3)

    def test_1_add(self):
        name_list = list(range(0, 30))
        for label in range(5):
            for _ in range(5):
                GClient.add(str(name_list.pop()), str(label))

    def test_2_show_all(self):
        current_dict = GClient.show_all()
        assert len(current_dict) == 25

    def test_3_acquire_name(self):
        # check 15-19
        for each_name in range(15, 20):
            each_name = str(each_name)
            GClient.acquire('name', each_name)

            # try to acquire it again
            resp = GClient.acquire('name', each_name)
            assert not resp['result']

            # try to acquire by label
            resp = GClient.acquire('label', str(2))
            assert not resp['result']

            # release
            resp = GClient.release('name', each_name)
            assert resp['result']

            # check its status
            resp = GClient.show_all()
            assert resp[each_name]['status'] == 'FREE'

    @classmethod
    def tearDownClass(cls):
        super(TestClient, cls).tearDownClass()
        cls._server_process.kill()


if __name__ == '__main__':
    unittest.main()
