import copy
from abc import ABC
import pprint


class StoreBase(ABC):
    def get_values(self):
        return vars(self)

    def dump(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.get_values())


class Target(StoreBase):
    def __init__(self, raw=None):
        self.raw = raw
        self.identifier = None
        self.identifier_int = None
        self.identified = False
        self.ip = None
        self.url = None
        self.fqdn = None
        self.port = None
        self.status = None

    def __str__(self):
        return str(self.identifier) if self.identifier is not None else ''


class HeaderTarget(Target):
    def __init__(self, raw=None):
        super().__init__(raw)

    def __getattr__(self, name):
        return name

    def __str__(self):
        return 'target'


class TargetGroup:
    def __init__(self, begin_int, end_int=None, value=''):
        self.begin_int = begin_int
        self.end_int = end_int
        self.value = value

    def get_values(self):
        return vars(self)

    def dump(self):
        print(self.get_values())


class ValueData(ABC):
    def __init__(self, data):
        self.data = data
        self.header = False

    def set_header(self, v):
        self.header = v

    def set(self, k, v):
        self.data[k] = v

    def get(self, k):
        return self.data.get(k)

    def update(self, k, fn):
        self.data[k] = fn(self.data[k])

    def delete(self, k):
        del self.data[k]

    def map(self, fn):
        self.data = {k: fn(v) for k, v in self.data.items()}

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_values(self):
        values = self.data.copy()

        for k, v in self.data.items():
            if isinstance(v, StoreBase):
                values[k] = str(v)

                tvalues = v.get_values()
                for tk, tv in tvalues.items():
                    values[k + '.' + tk] = tv

        return values

    def dump(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.get_data())


class ValueDataFactory(ABC):
    def __init__(self, master_data, params):
        self.master = self._create_master(master_data, params)

    def _create_master(self, master_data, params):
        master = master_data.copy()

        for param in params:
            if param not in master:
                master[param] = None

        return master

    def create(self):
        data = copy.deepcopy(self.master)

        return self.build(data)

    def build(self, data):
        return ValueData(data)
