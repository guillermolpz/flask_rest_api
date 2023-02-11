from attr import validate
from flask import Blueprint,jsonify,request
from flask_restplus import Api,Resource,fields

from api.functions import *

bp_api = Blueprint('Api',__name__,url_prefix="/Api")

api = Api(bp_api, version="1.0", title="Api", description="End Points")
ns_model = api.namespace('Methods', description='Methods')

class VerificarDatos():
    Login = api.model('login',{
        "username":fields.String(description=u"username", required=True,),
        "password":fields.String(description=u"password", required=True,),
    })

@ns_model.route("/Login/")
@api.doc(description="Correo y contraseña")
class Login(Resource):
    @api.expect(VerificarDatos.Login, validate=True)
    def post(self):
        #user = {"username":"bbb","password":"bbb"}
        #valida = valida_user(user["username"], user["password"])
        auth = request.json
        valida = valida_user(auth["username"],auth["password"])
        if 'token' in valida:
            return jsonify(valida)
        return jsonify({"Respuesta":"Login requerido"})
    
@ns_model.route('/CreateUser/')
@api.doc(description="Correo y contraseña")
class CrearUsario(Resource):
    @api.expect(VerificarDatos.Login, validate=True)
    def post(self):
        usuario = request.json
        usuario_creado = crear_usurio(usuario['username'], usuario['password'])
        return jsonify(usuario_creado)