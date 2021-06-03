import flask, json, sqlite3, random, string
from flask import request
from waitress import serve
from threading import Thread
from src.shiba import ShibaJudge

class ShibaAPI(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        app = flask.Flask(__name__)
        app.config["DEBUG"] = False

        @app.route('/v1/login', methods=['GET'])
        def login():
            email = request.args.get("email")
            password = request.args.get("password")

            shiba = ShibaJudge()
            shiba.auth(email, password)
            #shiba.download()
            #print(shiba.pdf(detailed=True))

            return flask.jsonify(status='ok')

        print("[API] L'API de Shiba est lancé")
        serve(app, host="0.0.0.0", port=80)