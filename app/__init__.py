from flask import Flask
from dotenv import load_dotenv
from app.connectors.mysql_connector import engine
from sqlalchemy import text
from app.models.product import Product

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import LoginManager
from app.models.user import User
import os

# Load Controller Files
from app.controllers.product import product_routes
from app.controllers.user import user_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    # Menggunakan SQLAlchemy untuk menyimpan data
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(product_routes)
app.register_blueprint(user_routes)

@app.route('/')
def my_app():

    # Fetch all Products
    product_query = select(Product)
    connection = engine.connect()
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(product_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.name}')

    return "<p>Insert Success</p>"