from flask import Blueprint, render_template, request
from app.connectors.mysql_connector import engine

from app.models.product import Product
from sqlalchemy import select
from flask_login import current_user, login_required

from sqlalchemy.orm import sessionmaker
from app.utils.api_response import api_response


# Definisikan Blueprint untuk rute-rute terkait produk
product_routes = Blueprint('product_routes', __name__)

# Tentukan rute untuk URL '/product' 
# diprotect menggunakan @login_required

@product_routes.route("/product", methods=['GET'])
@login_required
def product_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        product_query = select(Product)

        # Penambahan filter apabila menggunakan search_query
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            product_query = product_query.where(Product.name.like(f'%{search_query}%'))

        products = session.execute(product_query)
        products = products.scalars()
        response_data['products'] = products
 
        response_data['name'] = current_user.name

        # Render template HTML 'product_home.html' dari direktori 'templates/products/'
        return render_template("products/product_home.html", response_data = response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
@product_routes.route("/product", methods=['POST'])
@login_required
def product_insert():
    try:
        # Menerima data dari formulir HTML
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        # Membuat objek Product baru
        new_product = Product(name=name, price=price, description=description)

        connection = engine.connect()
        Session = sessionmaker(connection)
        # Menggunakan SQLAlchemy untuk menyimpan data
        session = Session()
        session.begin()
        session.add(new_product)
        session.commit()

        # Operasi sukses
        return { "message": "Input data berhasil"}

    except Exception as e:
        # Operasi jika gagal
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )


# @product_routes.route("/product", methods=['POST'])
# def product_insert():
#     new_product = Product(
#                     name=request.form['name'], 
#                     price=request.form['price'], 
#                     description=request.form['description']
#                     )
#     session = Session()
#     session.begin()
#     try:
#         session.add(new_product)
#         session.commit()

#     except Exception as e:
#         # Operation jika gagal
#         session.rollback()
#         return api_response(
#             status_code=500,
#             message=str(e),
#             data={}
#         )
    
#     # Operation sukses
#     return { "message": "Input data berhasil"}


@product_routes.route("/product/<id>", methods=['DELETE'])
def product_delete(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        product_to_delete = session.query(Product).filter(Product.id==id).first()
        session.delete(product_to_delete)
        session.commit()
        # Operation sukses
        return {"message":"Data detail pembelian berhasil dihapus"}
    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        ) 
    
@product_routes.route("/product/<id>", methods=['PUT'])
def product_update(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        product_to_update= session.query(Product).filter(Product.id==id).first()
        
        product_to_update.name = request.form['name']
        product_to_update.price = request.form['price']
        product_to_update.description = request.form['description']
        
        session.commit()
        # Operation sukses
        return {"message":"Data detail pembelian berhasil diedit"}
    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        ) 
    

