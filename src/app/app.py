from flask import Flask
from flask_restful import Api
from src.app.homepage.homepage import HomePage

app = Flask(__name__)
api = Api(app)

api.add_resource(HomePage, '/')

