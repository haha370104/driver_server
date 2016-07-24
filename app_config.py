from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret_config import db_url, port, route_password, route_username

app = Flask(__name__)

app.secret_key = 'A0Zr98jnjj/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://账号:密码@url:端口/数据库名'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['route_password'] = route_password
app.config['route_username'] = route_username
app.config['ALLOW_FILE'] = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
db = SQLAlchemy(app)
