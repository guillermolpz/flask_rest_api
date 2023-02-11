from db import engine
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from query import *

#from models import *

llave = 'Th1s1ss3cr3t'

def valida_user(username, password):
    with engine.connect() as con:
        try:
            user = con.execute(f"Select * from usuario where username = '{username}'").one()
        except:
            user = None
            
    if user:
        if check_password_hash(user[2], password):  
            # A qui se genera un token que solo va estar activo por durante 30 minutos
            token = jwt.encode({'public_id': user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, llave)  
            return {'token' : token.encode().decode('UTF-8')}
        
    return {'respuesta': 'Contraseña incorrecta'}

def crear_usurio(username, password):
    hash_password = generate_password_hash(password,method="sha256")
    #nuevo_usuario = Usuario(username=username, password=hash_password)
    #session_bd.add(nuevo_usuario)
    try:
        engine.execute(insertar_usuario(username, password))
    except:
        return {"respuesta":"El usuario ya esta creado en la BD"}
    return {"respuesta":"Usuario creado correctamente"}