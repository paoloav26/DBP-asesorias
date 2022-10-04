from operator import le
from tkinter.messagebox import NO
from flask import (
    abort, 
    jsonify,
    Flask, 
    request,
    render_template
)
from flask_cors import CORS

from models import setup_db, Personas, Maletas

ITEM_POR_PARGINA = 5

def paginate(request,selection):
    pagina = request.args.get('page',1,int)
    start = ITEM_POR_PARGINA*(pagina-1) 
    end = start+ITEM_POR_PARGINA

    return [item.format() for item in selection[start:end]]

def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app, origins=['http://127.0.0.1:5001'], max_age=10)

    # request handler
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/')
    def home():
        return "Hola!"


    # api-endpoints
    @app.route('/maletas', methods=['GET'])
    def get_maletas():
        status = 500
        try:
            selection = Personas.query.order_by('id').all()
            personas = paginate(request,selection)

            if len(personas) == 0:
                status=404
                abort(status)

            return jsonify({
                'success': True,
                'personas': personas,
                'total_personas': len(selection),
                'personas_en_pagina': len(personas)
            })

        except Exception as e:
            print(e)
            abort(status)

    @app.route('/maletas', methods=['POST'])
    def post_maletas():
        status = 500
        try:

            args = request.get_json()
            id_ = args.get('id',None) 
            nombre = args.get('nombre',None)
            apellidos = args.get('apellidos',None)
            numero = args.get('numero_telefonico',None)
            correo = args.get('correo',None)

            persona = Personas.query.filter_by(id=id_).one_or_none()
            
            if persona != None:
                status = 409
                abort(status)

            if id_ == None or nombre == None or apellidos == None or numero == None or correo == None:
                status = 400
                abort(status)

            persona = Personas(id=id_,nombre=nombre,apellidos=apellidos,numero_telefonico=numero,correo=correo)

            persona.insert()

            persona = Personas.query.filter_by(id=id_).one_or_none()

            return jsonify({
                'success': True,
                'persona': persona.format()
            })

        except Exception as e:
            print(e)
            abort(status)


    @app.route('/something/<id>', methods=['PATCH'])
    def UPDATE(id):
        return jsonify({
            'success': True
        })

    @app.route('/something/<id>', methods=['DELETE'])
    def DELETE(id):
        return jsonify({
            'success': True
        })

    # error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'code': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(409)
    def conlfict(error):
        return jsonify({
            'success': False,
            'code': 409,
            'message': 'Conflict'
        }), 409

    @app.errorhandler(500)
    def intenal_server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server Error'
        }), 500

    return app