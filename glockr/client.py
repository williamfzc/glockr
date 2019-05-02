import requests
import fire


class GClient(object):
    _BASE_URL = 'http://127.0.0.1:9410'
    _URL_DICT = {
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
    def acquire_name(cls, name):
        print(cls._acquire('name', name))

    @classmethod
    def acquire_label(cls, label):
        print(cls._acquire('label', label))

    @classmethod
    def release_name(cls, name):
        print(cls._release('name', name))

    @classmethod
    def release_label(cls, label):
        print(cls._release('label', label))

    @classmethod
    def add(cls, name, label=None):
        target_url = cls._URL_DICT['add'] + '?name={}'.format(name)
        if label:
            target_url += '&label={}'.format(label)
        resp = requests.post(target_url)
        print(resp.json())

    @classmethod
    def remove(cls, name):
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
