from sqlalchemy import create_engine, insert, select, ForeignKey
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

def CreateDB():
	metadata = MetaData()
	engine = create_engine("mysql+pymysql://root:aA123456@localhost:3306/test")
	session = Session(bind=engine)
	user_new= Table('user_new', metadata,
	 	Column('id', Integer(), primary_key=True),
	    Column('name', String(200), nullable=False),
	    Column('familia', String(200),  nullable=False),
	    Column('otchestvo', String(200), nullable=False),
	    Column('mob', String(200), nullable=False),
	    Column('mail', String(200), nullable=False),
	    Column('have_child', String(200), nullable=False),
	    Column('org', String(200), nullable=False),
	    Column('password', String(200), default=False),
	    Column('check_rule', Integer(), default=False),
	    Column('rule', Integer(), default=False),
	    Column('block', Integer(), default=0),
	    Column('created_on', DateTime(), default=datetime.now),
		)

	child_new= Table('child_new', metadata,
	 	Column('id', Integer(), primary_key=True),
	 	Column('user_id', Integer(), ForeignKey(user_new.c.id)),
	    Column('child_name', String(200), nullable=False),
	    Column('child_fam', String(200),  nullable=False),
	    Column('child_otchestvo', String(200), nullable=False),
	    Column('child_bith', , DateTime(), nullable=False),
		)

	news_new= Table('news_new', metadata,
	 	Column('id', Integer(), primary_key=True),
	    Column('title', String(200), nullable=False),
	    Column('pic', String(200),  nullable=False),
	    Column('data', String(200), nullable=False),
	    Column('date', String(200), nullable=False),
	    Column('author', String(200), nullable=False),
		)

	metadata.create_all(engine)