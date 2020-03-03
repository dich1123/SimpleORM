import datatypes as dt

class Column:
    def __init__(self, primary_key=False, type=dt.String(), nullable=False):
        self.primary_key = primary_key
        self.type = type
        self.nullable = nullable
        if primary_key and not isinstance(type, dt.Integer):
            raise Exception('Primary Key must be INTEGER type')
