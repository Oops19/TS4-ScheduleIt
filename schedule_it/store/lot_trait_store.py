from ts4lib.utils.singleton import Singleton


class LotTraitStore(object, metaclass=Singleton):
    def __init__(self):
        self.add = ()
        self.remove = ()
