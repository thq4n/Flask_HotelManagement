from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail, Message

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:admin@localhost/cnpm?charset=utf8mb4'
#app.config["SQLALCHEMY_DATABASE_URI"]='mysql://sql12384326:7fVrl2IQkw@sql12.freemysqlhosting.net/sql12384326?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.secret_key='This is secret'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thieuquan501@gmail.com'
app.config['MAIL_PASSWORD'] = 'flaskhotel'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db=SQLAlchemy(app=app)
admin=Admin(app=app,name="QUAN LI KHACH SAN", template_mode='bootstrap4')
login=LoginManager(app=app)

#MAIL:
mail = Mail(app)
