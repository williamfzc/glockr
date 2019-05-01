import requests


class GClient(object):
    BASE_URL = 'http://127.0.0.1:9410'
    URL_DICT = {
        'add': BASE_URL + '/res/add',
        'remove': BASE_URL + '/res/remove',
        'show_all': BASE_URL + '/res',

        'acquire': {
            'name': BASE_URL + '/res/acquire?name={}',
            'label': BASE_URL + '/res/acquire?label={}',
        },
        'release': {
            'name': BASE_URL + '/res/release?name={}',
            'label': BASE_URL + '/res/release?label={}',
        }
    }

    @classmethod
    def acquire_name(cls, name):
        return cls._acquire('name', name)

    @classmethod
    def acquire_label(cls, label):
        return cls._acquire('label', label)

    @classmethod
    def release_name(cls, name):
        return cls._release('name', name)

    @classmethod
    def release_label(cls, label):
        return cls._release('label', label)

    @classmethod
    def add(cls, name, label=None):
        target_url = cls.URL_DICT['add'] + '?name={}'.format(name)
        if label:
            target_url += '&label={}'.format(label)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def remove(cls, name):
        target_url = cls.URL_DICT['remove'] + '?name={}'.format(name)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def show_all(cls):
        target_url = cls.URL_DICT['show_all']
        resp = requests.get(target_url)
        return resp.json()

    @classmethod
    def _acquire(cls, acquire_type: str, content: str):
        target_url = cls.URL_DICT['acquire'][acquire_type].format(content)
        resp = requests.post(target_url)
        return resp.json()

    @classmethod
    def _release(cls, release_type: str, content: str):
        target_url = cls.URL_DICT['release'][release_type].format(content)
        resp = requests.post(target_url)
        return resp.json()


if __name__ == '__main__':
    print(GClient.add('name_1', label='label_1'))
    print(GClient.add('name_2', label='label_1'))
    print(GClient.add('name_3', label='label_2'))

    print(GClient.acquire_label('label_1'))
    print(GClient.show_all())

    print(GClient.release_name('name_2'))
    print(GClient.show_all())

    print(GClient.release_label('label_1'))
    print(GClient.show_all())
