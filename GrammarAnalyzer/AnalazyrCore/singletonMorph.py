import pymorphy2


class Singleton(object):

    __instance = None

    def __init__(self):
        if not Singleton.__instance:
            print('Class has been initialized')
        else:
            print("Instance already created:", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = pymorphy2.MorphAnalyzer()
        return cls.__instance
