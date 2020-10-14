from ..infra.products_dao import \
    listProducts_dao,\
    registerProduct_dao,\
    findProduct_dao,\
    findProductId_dao,\
    alterProduct_dao,\
    removeProduct_dao


from ..model.product import Product


def listProducts_service():
    return listProducts_dao()


def registerProduct_service(registerProduct):
    return registerProduct_dao(registerProduct)


def findProductId_service(id):
    result = findProductId_dao(id)
    if result != False:
        return [result]
    else:
        return []


def findProduct_service(data):
    return findProduct_dao(data)


def alterProduct_service(data):
    return alterProduct_dao(data)


def removeProduct_service(id):
    return removeProduct_dao(id)
