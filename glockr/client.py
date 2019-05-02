import requests
import fire
import requests.exceptions


# TODO API for waiting until release


class GClient(object):
    _PORT = '29410'
    _BASE_URL = 'http://127.0.0.1:{}'.format(_PORT)
    _URL_DICT = {
        'heart': _BASE_URL + '/',
        'add': _BASE_URL + '/res/add',
        'remove': _BASE_URL + '/res/remove',
        'show_all': _BASE_URL + '/res',

        'acquire': {
            'name': _BASE_URL + '/res/acquire?name={}',
            'label': _BASE_URL + '/res/acquire?label={}',
        },
        'release': {
            'name': _BASE_URL + '/res/release?name={}',
            'label': _BASE_URL + '/res/release?label={}',
        }
    }

    @classmethod
    def heartbeat(cls) -> bool:
        target_url = cls._URL_DICT['heart']
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
        target_url = cls._URL_DICT['add'] + '?name={}'.format(name)
        if label:
            target_url += '&label={}'.format(label)
        resp = requests.post(target_url)
        print(resp.json())

    @classmethod
    def remove(cls, name: str):
        target_url = cls._URL_DICT['remove'] + '?name={}'.format(name)
        resp = requests.post(target_url)
        print(resp.json())

    @classmethod
    def show_all(cls):
        target_url = cls._URL_DICT['show_all']
        resp = requests.get(target_url)
        print(resp.json())

    @classmethod
    def _acquire(cls, acquire_type: str, content: str):
        target_url = cls._URL_DICT['acquire'][acquire_type].format(content)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def _release(cls, release_type: str, content: str):
        target_url = cls._URL_DICT['release'][release_type].format(content)
        resp = requests.post(target_url)
        return resp.json()


def main():
    fire.Fire(GClient)


if __name__ == '__main__':
    main()
