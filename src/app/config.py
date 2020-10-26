import os

MAIL_USERNAME = 'financialoptteam@gmail.com'

class Config:
    SECRET_KEY = 'my_secret_key'

class DeveloperConfig(Config):
    SECRET_KEY = 'my_secret_key'
    DEBUG = True
    AUTH_TYPE = 1 # Database Authentication
    AUTH_USER_REGISTRATION = True
    AUTH_USER_REGISTRATION_ROLE = 'Public'
    # Config for Flask-WTF Recaptcha necessary for user registration
    RECAPTCHA_PUBLIC_KEY = 'GOOGLE PUBLIC KEY FOR RECAPTCHA'
    RECAPTCHA_PRIVATE_KEY = 'GOOGLE PRIVATE KEY FOR RECAPTCHA'
    # Config for Flask-Mail necessary for user registration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = 'espartanosopt'
    MAIL_DEFAULT_SENDER = 'financialoptteam@gmail.com'


