import requests
import fire
import json
import requests.exceptions

from glockr import config

# TODO API for waiting until release

_PORT = config.PORT
_BASE_URL = 'http://127.0.0.1:{}'.format(_PORT)

_URL_DICT = {
    each_name: _BASE_URL + each_router
    for each_name, each_router in config.ROUTER.items()
}


class GClient(object):
    @classmethod
    def heartbeat(cls) -> bool:
        target_url = _URL_DICT['heartbeat']
        try:
            resp = requests.get(target_url)
        except requests.exceptions.ConnectionError:
            return False
        return resp.ok

    @classmethod
    def add(cls, name: str, label: str = None) -> dict:
        target_url = _URL_DICT['add'] + '?name={}'.format(name)
        if label:
            target_url += '&label={}'.format(label)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def remove(cls, name: str) -> dict:
        target_url = _URL_DICT['remove'] + '?name={}'.format(name)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def show_all(cls) -> dict:
        target_url = _URL_DICT['show_all']
        resp = requests.get(target_url)
        return resp.json()

    @classmethod
    def download(cls, result_file_path: str) -> dict:
        target_url = _URL_DICT['show_all']
        resp = requests.get(target_url)

        with open(result_file_path, 'w+', encoding=config.CHARSET) as f:
            f.write(resp.text)

        return resp.json()

    @classmethod
    def upload(cls, result_file_path: str) -> list:
        result_list = list()
        with open(result_file_path, encoding=config.CHARSET) as f:
            data_dict = json.loads(f.read())
        for each_data in data_dict.values():
            each_result = cls.add(each_data['name'], each_data['label'])
            result_list.append(each_result)
        return result_list

    @classmethod
    def acquire(cls, acquire_type: str, content: str) -> dict:
        target_url = _URL_DICT['acquire'] + '?{}={}'.format(acquire_type, content)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def release(cls, release_type: str, content: str) -> dict:
        target_url = _URL_DICT['release'] + '?{}={}'.format(release_type, content)
        resp = requests.post(target_url)
        return resp.json()


def output2console(output_content: (list, dict)):
    print(json.dumps(output_content))


class GClient4CLI(object):
    @classmethod
    def heartbeat(cls) -> bool:
        return GClient.heartbeat()

    @classmethod
    def acquire_name(cls, name: str):
        output2console(GClient.acquire('name', name))

    @classmethod
    def acquire_label(cls, label: str):
        output2console(GClient.acquire('label', label))

    @classmethod
    def release_name(cls, name: str):
        output2console(GClient.release('name', name))

    @classmethod
    def release_label(cls, label: str):
        output2console(GClient.release('label', label))

    @classmethod
    def add(cls, name: str, label: str = None):
        output2console(GClient.add(name, label))

    @classmethod
    def remove(cls, name: str):
        output2console(GClient.remove(name))

    @classmethod
    def show_all(cls):
        output2console(GClient.show_all())

    @classmethod
    def upload(cls, result_file_path: str):
        output2console(GClient.upload(result_file_path))

    @classmethod
    def download(cls, result_file_path: str):
        output2console(GClient.download(result_file_path))


def main():
    fire.Fire(GClient4CLI)


if __name__ == '__main__':
    main()
