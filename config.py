import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

SQLALCHEMY_DATABASE_URI = 'postgresql://andres2:andres2@localhost:5432/inin'

SECURITY_REGISTERABLE = False
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'cuando la luna se pone re-grandota'

SECURITY_REGISTER_USER_TEMPLATE = 'security/others.html'
SECURITY_CHANGE_PASSWORD_TEMPLATE = 'security/others.html'
SECURITY_FORGOT_PASSWORD_TEMPLATE = 'security/others.html'
SECURITY_SEND_CONFIRMATION_TEMPLATE = 'security/others.html'
SECURITY_SEND_LOGIN_TEMPLATE = 'security/others.html'
