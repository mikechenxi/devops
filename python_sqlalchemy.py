from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import and_, or_, asc, desc, func

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

# use sessionmaker
db_session = sessionmaker(engine)()
# db_session = scoped_session(sessionmaker(engine))

# create
obj = User(name = 'name', age = 12, score = 12.5, board_date = '2020-01-01 19:30:05')
obj_list = [
    User(name = 'name2', age = 12, score = 15, board_date = '2020-02-03 00:00:00'),
    User(name = 'name3', age = 14, score = 14.32, board_date = '2020-04-01')
]
db_session.add(obj)
db_session.add_all(obj_list)
db_session.commit()
# retrieve
filter_list = db_session.query(User).all()
filter_list = db_session.query(User).first()
filter_list = db_session.query(User).count()
filter_list = db_session.query(User).limit(2)
filter_list = db_session.query(User).distinct()
filter_list = db_session.query(User).order_by(User.id.asc()).all()
filter_list = db_session.query(User.id.label('idd'), User.age)
filter_list = db_session.query(User).filter(User.age == 12)
filter_list = db_session.query(User).filter(User.age > 12)
filter_list = db_session.query(User).filter(User.age <= 12)
filter_list = db_session.query(User).get(1)  # use primary key
filter_list = db_session.query(User).filter(and_(User.age == 12, User.id == 1))
filter_list = db_session.query(User).filter(or_(User.age == 12, User.id == 2))
filter_list = db_session.query(User).filter(User.id.in_([1,2]))
filter_list = db_session.query(User).filter(User.id.notin_([1,2]))
filter_list = db_session.query(User).filter(User.name.like('%name%'))
filter_list = db_session.query(User).filter(User.name.notlike('%name%'))
filter_list = db_session.query(User).filter(User.name.is_(None))
filter_list = db_session.query(User).filter(User.name.isnot_(None))
filter_list = db_session.query(func.count(User.age).label('count'), User.age).group_by(User.age)
for obj in filter_list:
    print(obj.id, obj.name, obj.age, obj.score, obj.board_date)
    #print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
# update
filter_list = db_session.query(User).filter(User.age =='12')
filter_list.update({'age':20})
db_session.commit()
# delete
filter_list = db_session.query(User).filter(User.age =='20')
filter_list.delete()
db_session.commit()

db_session.close()

# use metadata
metadata = MetaData(engine)
users = Table('users', metadata, autoload = True)

con = engine.connect()
con.execute(users.insert(), name = 'name5', age = 23, score = 12.5, board_date = '2020-01-03 12:00:00')
con.execute(users.select(users.c.id == 18)).first()
con.execute(users.update(users.c.id == 18), name = 'aaa', age=1123)
con.execute(users.delete(users.c.id == 18))
con.close()

users.insert({users.c.name: 'aa'}).execute()
users.select(users.c.id == 1).execute().first()
users.update(users.c.id == 5, {users.c.age: 123}).execute()
users.delete(users.c.id == 5).execute()

# use engine
engine.execute('insert into users (name) values ("aaaa")')
engine.execute('select * from users where id = 1').first()
engine.execute('update users set age = 111 where id = 5')
engine.execute('delete from users where id = 5')
