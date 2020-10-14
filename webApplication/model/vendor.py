from ..model.product import Product


class Vendor():
    def __init__(self, id, vendorName, cnpj, city):
        self.id = id
        self.vendorName = vendorName
        self.cnpj = cnpj
        self.city = city
        self.products = []

    def add_products(self, id, vendorID, productName, productCode, price) -> "Product":
        product = Product(id, vendorID, productName, productCode, price)
        self.products.append(product)

    def get_products(self):
        return [product.productDict() for product in self.products]

    def getVendor(self):
        return self.id, self.vendorName, self.cnpj, self.city

    def __dict__(self):
        d = dict()
        d["id"] = self.id
        d["vendorName"] = self.vendorName
        d["cnpj"] = self.cnpj
        d["city"] = self.city
        d["products"] = [product.productDict() for product in self.products]

    @staticmethod
    def newVendor(data):
        try:
            id = data["id"]
            vendorName = data["vendorName"]
            cnpj = data["cnpj"]
            city = data["city"]
            return Vendor(id=id, vendorName=vendorName, cnpj=cnpj, city=city)
        except Exception as e:
            return {"Error creating new vendor": str(e)}
