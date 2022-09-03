from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
from dotenv import load_dotenv
load_dotenv() # load environnement variables


engine = create_engine(f"mysql+pymysql://{environ.get('DB_USER')}:{environ.get('DB_PASS')}@{environ.get('DB_HOST')}/{environ.get('DB_NAME')}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

