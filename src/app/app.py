from flask import Flask
from src.app.config import DeveloperConfig
app = Flask(__name__)
app.config.from_object(DeveloperConfig)
