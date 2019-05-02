import requests
import fire
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
    def acquire_name(cls, name: str):
        print(cls._acquire('name', name))

    @classmethod
    def acquire_label(cls, label: str):
        print(cls._acquire('label', label))

    @classmethod
    def release_name(cls, name: str):
        print(cls._release('name', name))

    @classmethod
    def release_label(cls, label: str):
        print(cls._release('label', label))

    @classmethod
    def add(cls, name: str, label: str = None):
        target_url = _URL_DICT['add'] + '?name={}'.format(name)
        if label:
            target_url += '&label={}'.format(label)
        resp = requests.post(target_url)
        print(resp.json())

    @classmethod
    def remove(cls, name: str):
        target_url = _URL_DICT['remove'] + '?name={}'.format(name)
        resp = requests.post(target_url)
        print(resp.json())

    @classmethod
    def show_all(cls):
        target_url = _URL_DICT['show_all']
        resp = requests.get(target_url)
        print(resp.json())

    @classmethod
    def _acquire(cls, acquire_type: str, content: str):
        target_url = _URL_DICT['acquire'] + '?{}={}'.format(acquire_type, content)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def _release(cls, release_type: str, content: str):
        target_url = _URL_DICT['release'] + '?{}={}'.format(release_type, content)
        resp = requests.post(target_url)
        return resp.json()


def main():
    fire.Fire(GClient)


if __name__ == '__main__':
    main()
