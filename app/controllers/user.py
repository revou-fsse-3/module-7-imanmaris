from flask import Blueprint, render_template, request, redirect
from app.connectors.mysql_connector import engine
from app.models.user import User
from sqlalchemy import select
from app.utils.api_response import api_response

from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user

# Definisikan Blueprint untuk rute-rute terkait produk
user_routes = Blueprint('user_routes', __name__)

# Tentukan rute untuk URL '/register'
@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")

@user_routes.route("/register", methods=['POST'])
def do_registration():
    try:
        # Menerima data dari formulir HTML
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Membuat objek Product baru
        # new_user = User(name=name, email=email, password=password)
        new_user = User(name=name, email=email)
        new_user.set_password(password)



        connection = engine.connect()
        Session = sessionmaker(connection)
        # Menggunakan SQLAlchemy untuk menyimpan data
        session = Session()
        session.begin()
        session.add(new_user)
        session.commit()

        # Operasi sukses
        return { "message": "Input data register berhasil"}
    
    except Exception as e:
        # Operasi jika gagal
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )


@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    # Menggunakan SQLAlchemy untuk menyimpan data
    session = Session()

    try:
        user = session.query(User).filter(User.email==request.form['email']).first()

        if user == None:
            return {"message": "Email belum terdaftar"}
        
        # Check password
        if not user.check_password(request.form['password']):
            return {"message": "Password salah"}
        
        login_user(user, remember=False)
        return redirect('/product')
        
    except Exception as e :
        return {"message" : "Login belum berhasil"}
    

@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/login')
