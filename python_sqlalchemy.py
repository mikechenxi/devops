from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Numeric, DateTime
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
#engine = create_engine('mysql://root:pwd@127.0.0.1:3306/sqlalchemy?charset=utf8')

Base = declarative_base()
class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key = True)
    name = Column(String(32))
    age = Column(Integer)
    score = Column(Numeric(12, 2))
    board_date = Column(DateTime)

# create table
Base.metadata.create_all(engine)

obj_session = sessionmaker(engine)
db_session = obj_session()

# create
obj = User(name = 'name', age = 12, score = 12.5, board_date = '2020-01-01 19:30:05')
obj_list = [
    User(name = 'name2', age = 13, score = 15, board_date = '2020-02-03 00:00:00'),
    User(name = 'name3', age = 14, score = 14.32, board_date = '2020-04-01')
]
db_session.add(obj)
db_session.add_all(obj_list)
db_session.commit()

# retrieve
all_list = db_session.query(User).all()
for obj in all_list:
    print(obj.id, obj.name, obj.age, obj.score, obj.board_date)
filter_list = db_session.query(User).filter(User.age =='12')
for obj in filter_list:
    print(obj.id, obj.name, obj.age, obj.score, obj.board_date)

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
