from flask import request, jsonify
from app.models.order_model import OrderModel
from app.models.adress_model import AdressModel
from app.models.order_adress_model import OrderAdressModel
from app.models.order_product_model import OrderProductModel
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from http import HTTPStatus
from dataclasses import asdict

@jwt_required()
def create_order():
    data_json = request.json
    adress_id = data_json.pop('adress_id')
    adress = asdict(AdressModel.query.get(adress_id))
    adress.pop('adress_id')
    print(adress)

    # TODO -> Verificação se já existe o endereço cadastrado na tabela
    # order_adresses
    order_adress = OrderAdressModel(**adress)
    order_adress.save_self()

    user = get_current_user()

    products = data_json.pop('products')

    data_json['user_id'] = user.user_id
    data_json['adress_id'] = order_adress.order_adress_id

    order = OrderModel(**data_json)
    order.save_self()
    
    for product in products:
        product['order_id'] = order.order_id
        order_product = OrderProductModel(**product)
        order_product.save_self()


    return jsonify(order), HTTPStatus.CREATED


@jwt_required()
def read_order():
    user = get_current_user()

    return jsonify(user.orders), HTTPStatus.OK

@jwt_required()
def update_order(order_id):
    order = OrderModel.query.get(order_id)
    status = request.json.get('status')

    # TODO -> Verificar se somente o status esta sendo
    # atualizado

    # TODO -> Verificação se o user do token é o 
    # proprietario da order sendo atualizada

    order.status = status

    order.save_self()

    return jsonify(order), HTTPStatus.OK

@jwt_required()
def delete_order(order_id):
    # order = OrderModel.query.get(order_id)

    # TODO -> Deleção da order envolve varios cascade
    # deve-se montar eles no relationship primeiro

    # order.delete_self()

    return '', HTTPStatus.NO_CONTENT
