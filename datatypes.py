import abc
import datetime

class DataType(abc.ABC):
    python_type = abc.abstractproperty()

    @abc.abstractmethod
    def __init__(self):
        self.data_type = None

    @classmethod
    def correct_type(cls, data):
        if isinstance(data, cls.python_type):
            return True
        raise Exception('Wrong Data Type Assigment')


class String(DataType):  # data type
    python_type = str

    def __init__(self, length=300):
        self.length = length
        self.data_type = 'VARCHAR'


class Integer(DataType):  # data type
    python_type = int

    def __init__(self, length=50):
        self.length = length
        self.data_type = 'INTEGER'


class DateTime(DataType):  # data type
    python_type = datetime.datetime

    def __init__(self):
        self.data_type = 'DATETIME'






class Kekeke:
    a = String()

b = Kekeke()
b.a = 'Lolol'
