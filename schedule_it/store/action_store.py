from ts4lib.utils.singleton import Singleton


class ActionStore(object, metaclass=Singleton):
    def __init__(self):
        self.actions = {}
        self.on_lot_load = {}  # 'a:d': None, ...
        self.on_lot_unload = {}  # 'a:d': None, ...
