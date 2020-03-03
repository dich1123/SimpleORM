import mysql.connector as mc
import datatypes as dt
from query import Query
from column import Column


class Model:
    """
    CRUD operations here
    """

    config = {'user': None, 'password': None, 'host': '127.0.0.1', 'database': None,
              'raise_on_warnings': True}
    __table_name__ = None

    def __init__(self, *args, **kwargs):  # in a case, when you are not using init in your class
        elements = self.__class__.__dict__
        elements = {i: j for i, j in elements.items() if isinstance(j, Column)}

        primary_key = {i: j for i, j in elements.items() if j.primary_key}  # element with primary key
        elements = {i: j for i, j in elements.items() if i not in primary_key}  # elements without primary key

        for i, j in kwargs.items():
            elements[i].type.correct_type(j)
            self.__dict__[i] = j

    @classmethod
    def _connect(cls):
        try:
            cnx = mc.connect(**cls.config)
            cls.cnx = cnx
        except mc.Error as error:
            print('Exception: ', error)

    @classmethod
    def _execute(cls, query, data=None):
        if not hasattr(cls, 'cnx'):
            cls._connect()
        try:
            cursor = cls.cnx.cursor()
            if not data:
                cursor.execute(query)

            else:
                cursor.execute(query, data)
                cls.cnx.commit()

            return cursor, cursor.lastrowid  # MODIFIED FROM FETCH ALL!!! BE CAREFUL
        except mc.Error as error:
            print('Execute EXCEPTION: ', error)
            return cursor, cursor.lastrowid

    @classmethod
    def create_all(cls):  # create table in DB
        if not cls.__table_name__:
            cls.__table_name__ = cls.__name__.lower()
        column_keys = [key for key in cls.__dict__.keys() if isinstance(cls.__dict__[key], Column)]  # only Column type

        primary_keys_amount = 0
        table_schema = '('
        for i in column_keys:
            column = cls.__dict__[i]
            if column.primary_key:
                primary_keys_amount += 1
            if primary_keys_amount > 1:
                raise mc.Error('Multiple primary key defined')

            null_checker = lambda x: 'NOT NULL' if not x else ''
            if hasattr(column.type, 'length'):
                table_schema += f"{i} {column.type.data_type}({column.type.length})" \
                                f" {column.primary_key and 'PRIMARY KEY AUTO_INCREMENT' or ''} " \
                                f"{null_checker(column.nullable)}, "  # in 4th position primary key if it's True
            else:
                table_schema += f"{i} {column.type.data_type}" \
                                f" {column.primary_key and 'PRIMARY KEY AUTO_INCREMENT' or ''} " \
                                f"{null_checker(column.nullable)}, "  # in 4th position primary key if it's True

        table_schema = table_schema[:-2].strip() + ')'

        query = f'CREATE TABLE {cls.__table_name__} {table_schema} ;'

        try:
            cls._execute(query)
        except mc.Error as err:
            print('Create ALL exception', err)

    @classmethod
    def dict_select(cls, search_values):  # search_values is a dict with {column_name: value, ...}
        if not cls.__table_name__:
            cls.__table_name__ = cls.__name__.lower()

        query = Query.dict_select(cls, search_values)

        answ = cls._execute(query)[0]

        for i in answ:
            data = i[1:]
            new_instance = cls(*data)
            new_instance._id_item = i[0]
            yield new_instance

    @classmethod
    def select(cls, search_info):  # search info is a string with correct SQL syntax in comparison elements
        if not cls.__table_name__:
            cls.__table_name__ = cls.__name__.lower()
        query = Query.select(cls, search_info)
        answ = cls._execute(query)[0]

        for i in answ:
            data = i[1:]
            new_instance = cls(*data)
            new_instance._id_item = i[0]
            yield new_instance

    def delete(self):
        if not hasattr(self, '_id_item'):
            raise Exception("You don't have such data in your DB or you're trying to delete without primary key,\n "
                            "\t\t\tuse staticmethod delete for deleting via primary key")

        query = Query.delete(self, self._id_item)
        self.__class__._execute(query)
        self.__class__.cnx.commit()

    @classmethod
    def delete_by_id(cls, unique_id):

        query = Query.class_delete(cls, unique_id)
        cls._execute(query)
        cls.cnx.commit()

    def commit(self):  # just update instance and then commit. your data will update. instance commit
        if not hasattr(self, '_id_item'):
            if not self.__table_name__:
                self.__table_name__ = self.__class__.__name__.lower()

            query, values = Query.create_query(self, 'insert')
            try:
                self._id_item = self.__class__._execute(query, values)[1]
            except mc.Error as error:
                print('Commit EXCEPTION: ', error)

        else:
            query, values = Query.create_query(self, 'update')
            try:
                self.__class__._execute(query, values)[1]
            except mc.Error as error:
                print('Commit EXCEPTION: ', error)

    def __repr__(self):
        answ = f'{self.__class__.__name__} '
        for i in self.__dict__:
            answ += f'{i}: {self.__dict__[i]}, '
        return answ[:-2]
