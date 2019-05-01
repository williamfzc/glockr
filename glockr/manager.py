class GResource(object):
    class _Status(object):
        FREE = 'FREE'
        BUSY = 'BUSY'

    def __init__(self, name, label=None, **kwargs):
        self.name = name
        self.label = label
        self.status = self._Status.FREE

        self.__dict__.update(kwargs)

    def acquire(self):
        if self.status == self._Status.FREE:
            self.status = self._Status.BUSY
            return GResourceResponse(True)
        return GResourceResponse(False, 'res {} status: {}'.format(self.name, self.status))

    def release(self):
        # just make sure, res becomes free.
        self.status = self._Status.FREE
        return GResourceResponse(True)


class GResourceResponse(object):
    def __init__(self, result: bool, reason: str = None):
        self.result = result
        self.reason = reason if reason is not None else ''

    def to_dict(self):
        return {
            'result': self.result,
            'reason': self.reason,
        }


class GResourceManager(object):
    _store = dict()

    @classmethod
    def add(cls, res_name: str, res_label: str = None, **kwargs) -> GResourceResponse:
        if cls.is_existed(res_name):
            return GResourceResponse(False, '{} already existed'.format(res_name))

        res = GResource(res_name, label=res_label, **kwargs)
        cls._store[res_name] = res
        return GResourceResponse(True)

    @classmethod
    def remove(cls, res_name: str):
        if not cls.is_existed(res_name):
            return GResourceResponse(False, '{} not existed'.format(res_name))

        del cls._store[res_name]

    @classmethod
    def acquire_res(cls, res_name: str) -> GResourceResponse:
        if not cls.is_existed(res_name):
            return GResourceResponse(False, '{} not existed'.format(res_name))

        return cls._store[res_name].acquire()

    @classmethod
    def acquire_label(cls, label_name: str) -> GResourceResponse:
        target_list = list()
        for each_name, each_res in cls._store.items():
            if each_res.label == label_name:
                target_list.append(each_res)

        for each_res in target_list:
            acquire_result = cls.acquire_res(each_res.name)
            if not acquire_result.result:
                return acquire_result

        return GResourceResponse(True)

    @classmethod
    def release_res(cls, res_name):
        if not cls.is_existed(res_name):
            return GResourceResponse(False, '{} not existed'.format(res_name))

        return cls._store[res_name].release()

    @classmethod
    def release_label(cls, label_name):
        target_list = list()
        for each_name, each_res in cls._store.items():
            if each_res.label == label_name:
                target_list.append(each_res)

        for each_res in target_list:
            release_result = cls.release_res(each_res.name)
            if not release_result.result:
                return release_result

        return GResourceResponse(True)

    @classmethod
    def show_all(cls):
        return {
            each_name: each_res.__dict__
            for each_name, each_res in cls._store.items()
        }

    @classmethod
    def is_existed(cls, res_name: str) -> bool:
        return res_name in cls._store
