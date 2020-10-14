from flask import request
from flask_restplus import Resource
from . import api
from .models import ProductDto
from ..model.product import Product
from ..services.products_services import \
    listProducts_service,\
    findProductId_service,\
    removeProduct_service,\
    alterProduct_service,\
    registerProduct_service,\
    findProduct_service


nameSpace_apiproduct = api.namespace(
    'products', description='Operations about products')


@nameSpace_apiproduct.route("/")
class product(Resource):
    @nameSpace_apiproduct.response(204, "Not content")
    @nameSpace_apiproduct.response(200, "Success", ProductDto.productModelApi)
    @nameSpace_apiproduct.marshal_list_with(ProductDto.productModelApi)
    def get(self):
        products = listProducts_service()
        if products == []:
            return None, 204
        return products


@nameSpace_apiproduct.route("/findAnyField", doc={"description": "Find product with any field"})
class productFilterAnyField(Resource):
    @nameSpace_apiproduct.response(404, "Not found")
    @nameSpace_apiproduct.response(200, "Success")
    @nameSpace_apiproduct.expect(ProductDto.findProductModelApi)
    @nameSpace_apiproduct.marshal_with(ProductDto.productModelApi)
    def post(self):
        findProduct = request.args.to_dict()
        if not "id" in findProduct or findProduct["id"] == 0:
            findProduct.update({"id": ""})
        if not "vendorID" in findProduct or findProduct["vendorID"] == 0:
            findProduct.update({"vendorID": ""})
        if not "productName" in findProduct or findProduct["productName"] == "string":
            findProduct.update({"productName": ""})
        if not "productCode" in findProduct or findProduct["productCode"] == 0:
            findProduct.update({"productCode": ""})
        if not "price" in findProduct or findProduct["price"] == 0:
            findProduct.update({"price": ""})
        find = Product.newProduct(findProduct)
        product = findProduct_service(find)
        if product != []:
            return product, 200
        else:
            return {"message": "Vendor id not found"}, 404


@nameSpace_apiproduct.route("/<int:vendorID>")
class productByVendorID(Resource):
    @nameSpace_apiproduct.doc(params={"vendorID": "Need enter VENDOR ID"})
    @nameSpace_apiproduct.expect(ProductDto.productModelApi)
    @nameSpace_apiproduct.response(400, "Validation error")
    @nameSpace_apiproduct.response(201, "Object created")
    def post(self, vendorID):
        product = nameSpace_apiproduct.payload
        if not "price" in product:
            product.update({"price": 0})
        registerProduct = Product.newProduct({"id": "", "vendorID": vendorID, "productName": product["productName"], "productCode": product["productCode"], "price": product[
            "price"]})
        result = registerProduct_service(registerProduct)
        if result == True:
            return {"message": "Ok"}, 201
        elif result == False:
            return {"message": "Not register"}
        else:
            return {"message": str(result)}, 400


@nameSpace_apiproduct.route("/<int:id>")
class productById(Resource):
    @nameSpace_apiproduct.doc(params={"id": "Product Id"})
    @nameSpace_apiproduct.response(404, "Not found")
    @nameSpace_apiproduct.marshal_with(ProductDto.productModelApi)
    def get(self, id):
        product = findProductId_service(id)
        if product == []:
            return None, 404
        return product[0]

    @nameSpace_apiproduct.response(204, "Product deleted")
    @nameSpace_apiproduct.response(404, "Not found")
    @nameSpace_apiproduct.doc(params={"id": "Product Id"})
    def delete(self, id):
        if findProductId_service(id):
            if removeProduct_service(id) == True:
                return None, 204
        else:
            return {"message": "Product id not found"}, 404

    @nameSpace_apiproduct.response(304, "Not modified")
    @nameSpace_apiproduct.response(404, "Not found")
    @nameSpace_apiproduct.response(200, "Success")
    @nameSpace_apiproduct.doc(params={"id": "Need enter the Id"})
    @nameSpace_apiproduct.expect(ProductDto.dinamicProductModelApi, validate=True)
    def put(self, id):
        product = request.args.to_dict()
        product.update({"id": id, "vendorID": ""})
        if not "price" in product:
            product.update({"price": 0})
        alterProduct = Product.newProduct(product)
        vendor = findProductId_service(alterProduct.id)
        if vendor != []:
            if alterProduct_service(alterProduct) == True:
                return {"message": "Product modified"}, 200
            else:
                return {"message": "Not modified"}, 304
        else:
            return {"message": "Product id not found"}, 404
