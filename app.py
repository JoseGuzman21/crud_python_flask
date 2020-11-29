from flask import Flask, jsonify, request
from products import products
from marshmallow import ValidationError
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong"})

@app.route('/v1/products', methods=['GET'])
def getproducts():
    return jsonify({"products": products, "message": "Products list"})

@app.route('/v1/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    products_found = [product for product in products if product['name'] == product_name]
    if (len(products_found)) > 0:
        return jsonify({'product': products_found[0], "status": 200})
    return jsonify({'message': 'Product not found', "status": 404})

@app.route('/v1/products', methods=['POST'])
def addProduct():
    try:
        new_product = {
            "name": request.json['name'],
            "price": request.json['price'],
            "quantity": request.json['quantity']
        }
        products.append(new_product)
        return jsonify({"message":"Product Added Succesfully", "products": products, "status": 200})
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/v1/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    product_found = [product for product in products if product['name'] == product_name]
    if (len(product_found)) > 0:
        product_found[0]['name'] = request.json['name']
        product_found[0]['price'] = request.json['price']
        product_found[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Products updated",
            "products": product_found[0],
            "status": 200
        })
    return jsonify({"message": "product not found", "status": 404})

@app.route('/v1/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    product_found = [product for product in products if product['name'] == product_name]
    if (len(product_found)) > 0:
        products.remove(product_found[0])
        return jsonify({
            "message": "Produc Deleted",
            "products": products,
            "status": 200
        })
    return jsonify({"message": "product not found", "status": 400})

if __name__ == '__main__':
    app.run(debug=True)