from model import Model
from column import Column
import datatypes as dt


class Sidr(Model):
    config = {'user': None, 'password': None, 'host': '127.0.0.1', 'database': None,
              'raise_on_warnings': True}
    config['user'] = 'user'
    config['password'] = 'Hardpas!1123'
    config['database'] = 'example'

    id = Column(type=dt.Integer(), primary_key=True)
    say = Column(nullable=True)
    word = Column(nullable=True)

    def __init__(self, say, word):
        self.say = say
        self.word = word


# Sidr.create_all()

a = Sidr('Hello', 'World')  # create
a.commit()  # save to db

a.say = 'HI!!!!!'  # update
a.commit()  # save to db
b = Sidr.select("id>50")  # selecting using string

for i in b:
    print(i)

b = Sidr.dict_select({})  # selecting using dict. in this case select all
for i in b:
    print(i)

a.delete()  # deleting element from db by instance
Sidr.delete_by_id(12)  # deleting element from db by primary key
