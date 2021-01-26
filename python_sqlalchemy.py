from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connect_args = {
    'user': 'root',
    'password': 'pwd',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'sqlalchemy',
    'charset': 'utf8'
}

engine = create_engine('mysql+pymysql://', connect_args = connect_args)
#engine = create_engine('mysql+pymysql://root:pwd@127.0.0.1:3306/sqlalchemy?charset=utf8')

Base = declarative_base()
class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    age = Column(Integer)

# create table
Base.metadata.create_all(engine)

obj_session = sessionmaker(engine)
db_session = obj_session()

# create
obj = User(name = 'name', age = 12)
obj_list = [
    User(name = 'name2', age = 13),
    User(name = 'name3', age = 14)
]
db_session.add(obj)
db_session.add_all(obj_list)
db_session.commit()

# retrieve
all_list = db_session.query(User).all()
for obj in all_list:
    print(obj.id, obj.name, obj.age)
filter_list = db_session.query(User).filter(User.age =='12')
for obj in filter_list:
    print(obj.id, obj.name, obj.age)

# update
filter_list = db_session.query(User).filter(User.age =='12')
filter_list.update({'age':20})
db_session.commit()

# delete
filter_list = db_session.query(User).filter(User.age =='20')
filter_list.delete()
db_session.commit()

db_session.close()


# https://www.cnblogs.com/caesar-id/p/11079774.html
