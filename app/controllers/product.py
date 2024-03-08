from flask import Blueprint, render_template, request, jsonify
from app.connectors.mysql_connector import engine

from app.models.product import Product
from sqlalchemy import select
from flask_login import current_user, login_required

from sqlalchemy.orm import sessionmaker
from app.utils.api_response import api_response

from app.decorators.role_checker import role_required

from cerberus import Validator
from app.validations.product_schema import product_schema

from flask_jwt_extended import jwt_required, get_jwt

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
@role_required('Admin')
def product_insert():

    v = Validator(product_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        # Validate Gagal
        return jsonify({"error": v.errors}), 400
    
    # new_product = Product(
    #         name=request.form['name'], 
    #         price=request.form['price'], 
    #         description=request.form['description']
    #     )
    
    new_product = Product(
            name=json_data['name'], 
            price=json_data['price'], 
            description=json_data['description']
        )
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        session.add(new_product)
        session.commit()

    except Exception as e:
        # Operation jika gagal
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    # Operation sukses
    return { "message": "Input data berhasil"}

@product_routes.route("/product/<id>", methods=['DELETE'])
@role_required('Admin')
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
@jwt_required()
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
    

