
Prerequisites
-
- Install mysql connector

Command: ~$ pip install mysql-connector-python

- ORM works only with MySQL

Installing
-
- Download all files to your computer
- Create some class from Model class (as in example.py)
- Now you can do CRUD operations (as in example.py)

Example.py:
-
```
from model import Model
from column import Column
import datatypes as dt


class Sidr(Model):
    # __table_name__ = 'SOMETABLE'
    # you can rename table as you want. otherwise table will be named as class name

    config = {'user': None, 'password': None, 'host': '127.0.0.1', 'database': None,
              'raise_on_warnings': True}  # you can insert setting into config straight
    
    """or add your info here"""
    config['user'] = 'user'  
    config['password'] = 'Hardpas!1123'
    config['database'] = 'example'

    id = Column(type=dt.Integer(), primary_key=True)  # creating new column with primary key(and auto increment) 
    say = Column(nullable=True)  # creating new column, can nullable
    word = Column(nullable=True)  # creating new column, can nullable

    def __init__(self, say, word):
        """
        Most operations are using instance 
        :param say: Column value
        :param word: Column value
        """
        self.say = say
        self.word = word


# Sidr.create_all()  # create table

a = Sidr('Hello', 'World')  # create
a.commit()  # save to db

a.say = 'HI!!!!!'  # update
a.commit()  # save to db
b = Sidr.select("id>50")  # selecting using string. returns generator with Sidr instances

for i in b:
    print(i)

b = Sidr.dict_select({})  # selecting using dict. in this case select all. returns generator with Sidr instances
for i in b:
    print(i)

a.delete()  # deleting element from db by instance
Sidr.delete_by_id(12)  # deleting element from db by primary key
```

 
 Authors
 -
 -Cherenkov Dima(DiCh)