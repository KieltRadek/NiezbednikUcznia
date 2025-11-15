from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os


Base = declarative_base()
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "UsersDatabase.db"))
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Session = sessionmaker(bind=engine)