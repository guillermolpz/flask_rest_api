from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from db import Session, engine, connection_db
#from models import Usuario
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

from api.controllers import bp_api
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'

#BD
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
session_bd = Session()

app.register_blueprint(bp_api)

from models import *

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        #if 'x-access-tokens' in request.headers:
        #    token = request.headers['x-access-tokens']

        #if not token:
        #    return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(session["token"], app.config['SECRET_KEY'], options={"verify_signature": False})
            #current_user = Users.query.filter_by(public_id=data['public_id']).first()
            print("Esta iniciando")
        except:
            #return jsonify({'message': 'token is invalid'})
            print("El token no es valido o no esta logueado")
            return redirect(url_for('login'))
        #return f(data['public_id'],*args, **kwargs)
        return f(*args, **kwargs)
        #return f(current_user, *args, **kwargs)
    return decorator

@app.route('/', methods=['GET'])
@token_required
def index():
    return render_template('index.html')

@app.route('/index2', methods=['GET'])
def index2():
    return render_template('index2.html')

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({'mensaje': 'Endpoint desde hola'})

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        args = {
            "username":username,
            "password":password
        }
        response = requests.post('http://localhost:5000/Api/Methods/Login/', json=args)
        #print(dir(response))
        if response.status_code == 200:
            response_api = json.loads(response.text)
            session['token'] = response_api['token']
            #print(response_api)
            return render_template('index.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('login.html')
        
"""
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        #return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        return jsonify({'Respuesta':"Cloud not verify"})    

    with engine.connect() as con:
        user = con.execute(f"Select * from usuario where username = '{auth.username}'").one()
    print(user)
     
    if check_password_hash(user[2], auth.password):  
        # A qui se genera un token que solo va estar activo por durante 30 minutos
        token = jwt.encode({'public_id': user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.encode().decode('UTF-8')}) 

    #return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    return jsonify({'respuesta': 'Login requerido'})
"""

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        args = {
            "username":username,
            "password":password
        }
        response = requests.post('http://localhost:5000/create_user', json=args)
        #print(dir(response))
        if response.status_code == 200:
            return render_template('index.html')
        else:
            return render_template('registro.html')
    return render_template('registro.html')
 
"""  
@app.route('/create_user', methods=['POST'])
#@token_required
def create_user():
    #print(request)
    #print(dir(request))
    # Con esta funcionalidad podriamos blouear quien puede crear mas usuarios y no cualquiera
    #if current_user == 'admi':
    #else:
    #return jsonify({"respuesta":"El usuario no puede crear usuarios"})
    data = json.loads(request.data) 
    if 'username' not in data:
        return jsonify({"respuesta":"No esta enviando el username"})
    if 'password' not in data:
        return jsonify({"respuesta":"No esta enviando el password"})
    if len(data["username"]) == 0:
        return jsonify({"respuesta":"Username no puede ser vacio"})
    if len(data["password"]) == 0:
        return jsonify({"respuesta":"Password no puede ser vacio"})
    print(data)
    print(type(data))
    print(data["username"])
    with engine.connect() as con:
        hash_password = generate_password_hash(data["password"],method="sha256")
        nuevo_usuario = Usuario(username=data["username"], password=hash_password)
        session_bd.add(nuevo_usuario)
        try:
            session_bd.commit()
        except:
            return jsonify({"respuesta":"El usuario ya esta creado en la BD"})
    return jsonify({"respuesta":"Usuario creado correctamente"})
"""

@app.route('/obtener_venta', methods=['GET'])
@token_required
def obtener_venta(current_user):
    data = json.loads(request.data)
    print(data)
    if 'username' not in data:
        return jsonify({"respuesta":"Username no se envio en la peticion"})
    with engine.connect() as con:
        query_get_user = f"select * from usuario where username = '{data['username']}'"
        respuesta = con.execute(query_get_user).one()
        print(respuesta)
        #for i in respuesta:
        #    print(i)
        query_get_ventas = f"select * from ventas where username_id = '{respuesta[0]}'"
        respuesta_vetas = con.execute(query_get_ventas)
        print(respuesta_vetas)
        respuesta_vetas_leg = [i[0] for i in respuesta_vetas]
        print(respuesta_vetas_leg)
        #for i in respuesta_vetas:
        #    print(i)
        return jsonify({"Ventas usuario ":{"usuario":data['username'], "ventas":respuesta_vetas_leg}})
        #return jsonify({"respuesta":"OK"})
        
@app.route('/ventas', methods=['GET'])
def obtener_ventas():
    with engine.connect() as con:
        obtener_ventas = f"select * from ventas"
        ventas = con.execute(obtener_ventas)
        lista = list()
        for i in ventas:
            lista.append({"ID_VENTA":i[0], "valor_venta":i[2]})
        
    return jsonify({"Respuesta":lista})

@app.route('/ventas', methods=['PUT'])
def editar_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"El id no esta en la peticion"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"El valor de la venta no esta en la petición"})
    
    venta = Ventas.query.get(data["id"])
    venta.venta = data["valor"]
    db.session_bd.commit()
    return jsonify({"Respuesta":"Venta actualiada"})

@app.route('/ventas', methods=['POST'])
def crear_venta():
    data = json.loads(request.data)
    if 'user_id' not in data:
        return jsonify({"Respuesta":"El id de usuario no esta en la peticion"})
    if 'venta' not in data:
        return jsonify({"Respuesta":"El valor de la venta no esta en la petición"})
    if 'venta_product' not in data:
        return jsonify({"Respuesta":"La venta producto no fue enviada en la petición"})
    
    nueva_venta = Ventas(username_id=data['user_id'],venta=data['venta'],venta_product=data['venta_product'])
    db.session_bd.add(nueva_venta)
    db.session_bd.commit()
    return jsonify({"Respuesta":"Venta creada"})

@app.route('/ventas', methods=['DELETE'])
def ELIMINAR_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"El id de la venta no esta en la peticion"})
    
    venta = Ventas.query.get(data["id"])
    db.session_bd.delete(venta)
    db.session_bd.commit()
    return jsonify({"Respuesta":"Venta eliminada"})
    
if __name__ == "__main__":
    app.run(debug=True)