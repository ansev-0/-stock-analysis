import os

class Config:
    SECRET_KEY = 'my_secret_key'

class DeveloperConfig(Config):
    DEBUG = True