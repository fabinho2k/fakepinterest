#Usando o init para criar o site

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__) #criando o site

#Passando os parâmetros para criação do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = "4c79fa9794106503b6014d8b53e13091"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts" #Local onde as fotos postadas pelo usuário, ficará salva

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from fakepinterest import routes