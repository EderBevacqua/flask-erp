from flask import request
from flask_restplus import Resource
from . import api
from .models import VendorDto
from ..model.vendor import Vendor
from ..services.vendors_services import \
    listVendors_service,\
    findVendorId_service,\
    removeVendor_service,\
    alterVendor_service,\
    registerVendor_service,\
    findVendorCnpj_service,\
    findVendor_service,\
    validateCnpj_service

nameSpace_apivendor = api.namespace(
    'vendors', description='Operations about vendors')


@nameSpace_apivendor.route("/")
class vendor(Resource):
    @nameSpace_apivendor.response(204, "Not content")
    @nameSpace_apivendor.response(200, "Success", VendorDto.vendorModelApi)
    @nameSpace_apivendor.marshal_list_with(VendorDto.vendorModelApi)
    def get(self):
        vendors = listVendors_service()
        if vendors == []:
            return None, 204
        return vendors

    @nameSpace_apivendor.response(422, "Unprocessable entity")
    @nameSpace_apivendor.response(201, "Object created")
    @nameSpace_apivendor.expect(VendorDto.vendorModelApi, validate=True)
    def post(self):
        new = nameSpace_apivendor.payload
        if validateCnpj_service(new["cnpj"]) == False:
            return {"message": "Invalid cnpj"}, 422
        if not "city" in nameSpace_apivendor.payload:
            new.update({"city": ""})
        registerVendor = Vendor.newVendor({"id": "",  "vendorName": new["vendorName"], "cnpj": new["cnpj"], "city": new[
            "city"]})
        for p in new["products"]:
            if not "price" in p:
                p.update({"price": 0})
            registerVendor.add_products(
                "", "", p["productName"], p["productCode"], p["price"])
        result = registerVendor_service(registerVendor)
        if result == True:
            return {"message": "Ok"}, 201
        elif result == False:
            return {"message": "Not register"}
        else:
            return {"message": str(result)}, 400


@nameSpace_apivendor.route("/findAnyField", doc={"description": "Find vendor with any field"})
class vendorFilterAnyField(Resource):
    @nameSpace_apivendor.response(400, "Validation error")
    @nameSpace_apivendor.response(404, "Not found")
    @nameSpace_apivendor.response(200, "Success")
    @nameSpace_apivendor.expect(VendorDto.findVendorModelApi)
    @nameSpace_apivendor.marshal_list_with(VendorDto.vendorModelApi)
    def post(self):
        findVendor = request.args.to_dict()
        if not "id" in findVendor or findVendor["id"] == 0:
            findVendor.update({"id": ""})
        if not "vendorName" in findVendor or findVendor["vendorName"] == "string":
            findVendor.update({"vendorName": ""})
        if not "cnpj" in findVendor or findVendor["cnpj"] == "string":
            findVendor.update({"cnpj": ""})
        if not "city" in findVendor or findVendor["city"] == "string":
            findVendor.update({"city": ""})

        find = Vendor.newVendor(findVendor)
        vendor = findVendor_service(find)
        if vendor != []:
            return vendor, 200
        else:
            return {"message": "Vendor id not found"}, 404


@nameSpace_apivendor.route("/<int:id>")
class vendorById(Resource):
    @nameSpace_apivendor.doc(params={"id": "An vendo Id"}, type=int)
    @nameSpace_apivendor.response(404, "Not found")
    @nameSpace_apivendor.marshal_with(VendorDto.vendorModelApi)
    def get(self, id):
        vendor = findVendorId_service(id)
        if vendor == []:
            return None, 404
        return vendor[0]

    @nameSpace_apivendor.response(204, "Vendor deleted")
    @nameSpace_apivendor.response(404, "Not found")
    def delete(self, id):
        if findVendorId_service(id):
            if removeVendor_service(id) == True:
                return "", 204
        else:
            return {"message": "Vendor id not found"}, 404

    @nameSpace_apivendor.response(200, "Success")
    @nameSpace_apivendor.response(304, "Not modified")
    @nameSpace_apivendor.response(404, "Not found")
    @nameSpace_apivendor.response(422, "Unprocessable entity")
    @nameSpace_apivendor.expect(VendorDto.dinamicVendorModelApi, validate=True)
    def put(self, id):
        vendor = request.args.to_dict()
        vendor.update({"id": id})
        alterVendor = Vendor.newVendor(vendor)
        fVendor = findVendorId_service(alterVendor.id)
        if fVendor != []:
            if validateCnpj_service(alterVendor.cnpj) == False:
                return {"message": "Invalid cnpj"}, 422
            if fVendor[0].cnpj != alterVendor.cnpj:
                if findVendorCnpj_service(alterVendor.cnpj) == True:
                    return {"Message": "CNPJ already registered"}
            if alterVendor_service(alterVendor) == True:
                return {"message": "Vendor modified"}, 200
            else:
                return {"message": "Not modified"}, 304
        else:
            return {"message": "Vendor id not found"}, 404
