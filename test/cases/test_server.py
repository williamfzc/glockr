import unittest
import subprocess
import requests
import time
import json

from glockr.config import PORT

BASE_URL = 'http://127.0.0.1:{}'.format(PORT)


class TestServer(unittest.TestCase):
    _server_process = None

    @staticmethod
    def get_current_dict() -> dict:
        target_url = BASE_URL + '/res'
        resp = requests.get(target_url)
        resp_dict = json.loads(resp.text)
        return resp_dict

    def get_res_status(self, name) -> str:
        current_dict = self.get_current_dict()
        return current_dict[str(name)]['status']

    @classmethod
    def setUpClass(cls):
        super(TestServer, cls).setUpClass()
        cls._server_process = subprocess.Popen('python -m glockr.server start', shell=True)
        time.sleep(3)

    def test_1_add(self):
        target_url = BASE_URL + '/res/add'

        name_list = list(range(0, 30))
        for label in range(5):
            for _ in range(5):
                # 'data' seems does not work?
                each_url = target_url + '?name={}&label={}'.format(name_list.pop(), label)
                resp = requests.post(each_url)
                assert resp.ok

    def test_2_show_all(self):
        current_dict = self.get_current_dict()
        assert len(current_dict) == 25

    def test_3_acquire_name(self):
        acquire_url = BASE_URL + '/res/acquire'
        release_url = BASE_URL + '/res/release'

        # check 15-19
        for each_name in range(15, 20):
            # check its status
            assert self.get_res_status(each_name) == 'FREE'

            # acquire
            each_acquire_url = acquire_url + '?name={}'.format(each_name)
            resp = requests.post(each_acquire_url)
            assert resp.ok

            # check its status
            assert self.get_res_status(each_name) == 'BUSY'

            # try to acquire it again
            resp = requests.post(each_acquire_url)
            resp_dict = json.loads(resp.text)
            assert not resp_dict['result']

            # try to acquire by label
            each_acquire_label_url = acquire_url + '?label={}'.format(2)
            resp = requests.post(each_acquire_label_url)
            resp_dict = json.loads(resp.text)
            assert not resp_dict['result']

            # release
            each_release_url = release_url + '?name={}'.format(each_name)
            resp = requests.post(each_release_url)
            assert resp.ok

            # check its status
            assert self.get_res_status(each_name) == 'FREE'

    def test_4_acquire_label(self):
        acquire_url = BASE_URL + '/res/acquire'
        release_url = BASE_URL + '/res/release'

        # check 15-19
        for each_name in range(15, 20):
            each_status = self.get_res_status(each_name)
            assert each_status == 'FREE'

        # acquire label '2'
        each_release_label_url = acquire_url + '?label={}'.format(2)
        resp = requests.post(each_release_label_url)
        resp_dict = json.loads(resp.text)
        assert resp_dict['result']

        # check 15-19
        for each_name in range(15, 20):
            each_status = self.get_res_status(each_name)
            assert each_status == 'BUSY'

        # release label '2'
        each_release_label_url = release_url + '?label={}'.format(2)
        resp = requests.post(each_release_label_url)
        resp_dict = json.loads(resp.text)
        assert resp_dict['result']

        # check 15-19
        for each_name in range(15, 20):
            each_status = self.get_res_status(each_name)
            assert each_status == 'FREE'

    @classmethod
    def tearDownClass(cls):
        super(TestServer, cls).tearDownClass()
        cls._server_process.kill()


if __name__ == '__main__':
    unittest.main()
