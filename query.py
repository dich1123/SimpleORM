from column import Column


class Query:

    @staticmethod
    def create_query(item, query_type):
        attributes = []
        values = []
        for i in item.__dict__:

            try:
                item.__class__.__dict__[i].type.correct_type(item.__dict__[i])  # checking type correct
            except KeyError:
                pass

            if not str(i).startswith('_'):
                attributes.append(i)
                values.append(item.__dict__[i])

        if query_type.lower() == 'insert':
            attributes = ', '.join(attributes)
            query = f'INSERT INTO {item.__table_name__} ({attributes}) ' \
                    f'VALUES ({"".join("%s, " * len(values))[:-2]});'

            return query, tuple(values)

        if query_type.lower() == 'update':
            attributes = '=%s, '.join(attributes) + '=%s'

            class_attr = item.__class__.__dict__
            unique_key = [key for key in class_attr.keys() if isinstance(class_attr[key], Column)]  # class attr
            unique_key = [key for key in unique_key if class_attr[key].primary_key]  # class attrs with primary_key
            query = f'UPDATE {item.__table_name__} SET {attributes} WHERE {unique_key[0]}={item._id_item};'

            return query, tuple(values)

    @staticmethod
    def query(expression):
        pass

    @staticmethod
    def select(cls, search_info):
        if not search_info:
            return f'SELECT * FROM {cls.__table_name__};'
        else:
            return f'SELECT * FROM {cls.__table_name__} WHERE {search_info};'

    @staticmethod
    def dict_select(cls, search_values):

        if list(search_values.values()) == ['']*len(search_values):
            if not search_values:
                query = f"SELECT * FROM {cls.__table_name__};"

        else:
            values = [f"{key}='{item}'" for (key, item) in search_values.items()]
            values = ' AND '.join(values)
            query = f"SELECT * FROM {cls.__table_name__} WHERE {values};"

        return query

    @staticmethod
    def delete(item, _id_item):
        if not item.__class__.__table_name__:
            table_name = item.__class__.__name__.lower()
        else:
            table_name = item.__class__.__table_name__

        class_attr = item.__class__.__dict__
        unique_key = [key for key in class_attr.keys() if isinstance(class_attr[key], Column)]  # class attr
        unique_key = [key for key in unique_key if class_attr[key].primary_key]  # class attrs with primary_key

        query = f"DELETE FROM {table_name} WHERE {unique_key[0]}={_id_item};"
        return query

    @staticmethod
    def class_delete(cls, unique_id):
        if not cls.__table_name__:
            table_name = cls.__name__.lower()
        else:
            table_name = cls.__table_name__

        class_attr = cls.__dict__
        unique_key = [key for key in class_attr.keys() if isinstance(class_attr[key], Column)]  # class attr
        unique_key = [key for key in unique_key if class_attr[key].primary_key]  # class attrs with primary_key

        query = f"DELETE FROM {table_name} WHERE {unique_key[0]}={unique_id};"
        return query
