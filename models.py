from sqlalchemy import Column, String, Integer
#from db import base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from app import db

#class Usuario(base):
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    username = db.Column(String(70), unique=True)
    password = db.Column(String(200))
    ventas = relationship('Ventas', backref="usuario", cascade='delete, merge')

class Ventas(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    username_id = db.Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE'))
    venta = db.Column(Integer)
    venta_product = db.Column(Integer)
    
#base.metadata.create_all(engine)

#https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/