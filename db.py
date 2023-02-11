from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#Conexion en localhost
connection_db = "postgresql://postgres:postgres01@localhost:5432/flask_db"
#Conexion con sqlite
#connection_db = "sqlite:///basedatos.db"
#Conexion en heroku
#connection_db = "postgresql://wenbvlffcfxkhm:e0ac7d0af6b020e9098f8ab8410fcd9589a4b874bbddbc05ccb640571ed71bcf@ec2-52-4-104-184.compute-1.amazonaws.com:5432/d2pqjmi94fjgq"
base = declarative_base()
engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)