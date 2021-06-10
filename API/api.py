import flask, json, sqlite3, random, string
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
from threading import Thread
from core.shiba import ShibaJudge
from core.data import ShibaData
from core.error import *
import jwt


class ShibaAPI(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        app = flask.Flask(__name__)
        app.config["DEBUG"] = False
        limiter = Limiter(
            app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"]
        )

        @app.route('/v1/login', methods=['POST'])
        @limiter.limit("3 per hour")
        def login():

            email = request.args.get("email")
            password = request.args.get("password")

            if email == None or password == None:
                return flask.jsonify(status='error', message='bad request'), 400

            shiba = ShibaJudge()

            try:
                if shiba.auth(email, password):

                    try:
                        data = ShibaData(email, shiba.ville)
                        data.login()
                    except:
                        bde = 'error'

                    jwt_token = jwt.encode({"token": shiba.token, "email": email, "ville":shiba.ville}, "valou", algorithm="HS256")
                    return flask.jsonify(status='success', token=jwt_token, bde=bde), 200
                else:
                    return flask.jsonify(status='error', message='invalid login'), 401
            except:
                return flask.jsonify(status='error', message='server internal error'), 500

        print("[API] L'API de Shiba est lancé")
        serve(app, host="0.0.0.0", port=80)