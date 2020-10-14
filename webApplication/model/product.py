class Product():
    def __init__(self, id, vendorID, productName, productCode, price):
        self.id = id
        self.vendorID = vendorID
        self.productName = productName
        self.productCode = productCode
        self.price = price

    def productDict(self):
        d = dict()
        d["id"] = self.id
        d["vendorID"] = self.vendorID
        d["productName"] = self.productName
        d["productCode"] = self.productCode
        d["price"] = self.price
        return d

    def getProduct(self):
        return self.id, self.vendorID, self.productName, self.productCode, self.price

    @staticmethod
    def newProduct(data):
        try:
            id = data["id"]
            vendorID = data["vendorID"]
            productName = data["productName"]
            productCode = data["productCode"]
            price = data["price"]
            return Product(id=id, vendorID=vendorID, productName=productName, productCode=productCode, price=price)
        except Exception as e:
            return {"Error creating new product": str(e)}
