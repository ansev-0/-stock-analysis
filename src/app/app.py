from flask import Flask
from src.app.config import DeveloperConfig
from flask import session
from datetime import timedelta


app = Flask(__name__)
app.config.from_object(DeveloperConfig)
