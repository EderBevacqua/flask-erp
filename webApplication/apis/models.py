from webApplication.apis import api
from flask_restplus import fields


class ProductDto:
    productModelApi = api.model("Product", {
        "id": fields.Integer(readonly=True),
        "vendorID": fields.Integer(readonly=True, description="The vendor Id"),
        "productName": fields.String(required=True, description="The product name"),
        "productCode": fields.Integer(required=True, description="The product code"),
        "price": fields.Fixed(decimals=2, required=False, description="The product price"),
    })

    dinamicProductModelApi = api.parser()
    dinamicProductModelApi.add_argument(
        "productName", type=str, required=True, help="Need enter the name")
    dinamicProductModelApi.add_argument(
        "productCode", type=int, required=True, help="Need enter the code")
    dinamicProductModelApi.add_argument(
        "price", type=float, required=False, help="Need enter the price")

    findProductModelApi = dinamicProductModelApi.copy()
    findProductModelApi.add_argument("id", type=int, required=False, help="Id")
    findProductModelApi.add_argument(
        "vendorID", type=int, required=False, help="VendorID")
    findProductModelApi.replace_argument(
        "productName", type=str, required=False, help="Name")
    findProductModelApi.replace_argument(
        "productCode", type=int, required=False, help="Code")
    findProductModelApi.replace_argument(
        "price", type=float, required=False, help="Price")


class VendorDto:
    vendorModelApi = api.model("Vendor", {
        "id": fields.Integer(readonly=True),
        "vendorName": fields.String(required=True, description="The vendor name"),
        "cnpj": fields.String(required=True, description="The vendor cnpj", example="00.000.000/0000-00", min_length=17, max_length=18),
        "city": fields.String(required=False, description="The vendor city"),
        "products": fields.List(fields.Nested(ProductDto.productModelApi)),
    })

    dinamicVendorModelApi = api.parser()
    dinamicVendorModelApi.add_argument(
        "id", type=int, required=True, help="Need enter the Id")
    dinamicVendorModelApi.add_argument(
        "vendorName", required=True, type=str, help="Need enter the Name")
    dinamicVendorModelApi.add_argument(
        "cnpj", required=True, type=str, help="Need enter the Cnpj this format '00.000.000/0000-00'")
    dinamicVendorModelApi.add_argument(
        "city", required=True, type=str, help="Need enter the City")

    findVendorModelApi = dinamicVendorModelApi.copy()
    findVendorModelApi.replace_argument(
        "id", type=int, required=False, help="Id")
    findVendorModelApi.replace_argument(
        "vendorName", required=False, type=str, help="Name")
    findVendorModelApi.replace_argument(
        "cnpj", required=False, type=str, help="Cnpj - format '00.000.000/0000-00'")
    findVendorModelApi.replace_argument(
        "city", required=False, type=str, help="City")
