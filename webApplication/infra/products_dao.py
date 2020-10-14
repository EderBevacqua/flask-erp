from contextlib import closing
import mysql.connector
from ..model.product import Product
from ..model.vendor import Vendor
from .db_config import con


def listProducts_dao():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("select * from product order by 1")
        rows = cursor.fetchall()
        result = []
        if rows:
            for (id, vendorID,  productName, productCode, price) in rows:
                result.append(Product.newProduct(
                    {"id": id, "vendorID": vendorID,  "productName": productName, "productCode": productCode, "price": price}))
            return result
        else:
            return []


def registerProduct_dao(newProduct):
    try:
        with closing(con()) as connection, closing(connection.cursor()) as cursor:
            sql2 = "INSERT INTO product (vendorID, productName, productCode, price) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql2, (newProduct.vendorID, newProduct.productName,
                                  newProduct.productCode, newProduct.price))
            connection.commit()
            if cursor.lastrowid:
                return True
            else:
                return False
    except Exception as err:
        return err


def findProductId_dao(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("select * from product where id = '%s'" % (id))
        rows = cursor.fetchall()
        if rows:
            for (id, vendorID, productName, productCode, price) in rows:
                if id != None:
                    result = Product.newProduct(
                        {"id": id, "vendorID": vendorID,  "productName": productName, "productCode": productCode, "price": price})
            return result
        else:
            return False


def findProduct_dao(data):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        queryFilter = "select * from product where"
        if data.id != "":
            queryFilter += " id = '"+str(data.id)+"' AND "
        if data.vendorID != "":
            queryFilter += " vendorID = '"+str(data.vendorID)+"' AND "
        if data.productName != "":
            queryFilter += " productName = '"+data.productName+"' AND "
        if data.productCode != "":
            queryFilter += " productCode = '"+data.productCode+"' AND "
        if data.price != "":
            queryFilter += " price = '"+str(data.price)+"' AND "
        if queryFilter[-5::] == "where":
            return []
        queryFilter = queryFilter[:-5]+" order by 1"
        cursor.execute(queryFilter)
        rows = cursor.fetchall()
        result = []
        if rows:
            for (id, vendorID,  productName, productCode, price) in rows:
                result.append(Product.newProduct(
                    {"id": id, "vendorID": vendorID,  "productName": productName, "productCode": productCode, "price": price}))
            return result
        else:
            return []


def alterProduct_dao(data):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("""UPDATE product set productName = "%s", productCode = "%s", price = "%s" where id = "%s";""" % (
            data.productName, data.productCode, data.price, data.id))
        connection.commit()
        if cursor.rowcount >= 1:
            return True
        else:
            return False


def removeProduct_dao(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        if type(id) == list:
            for i in id:
                cursor.execute("DELETE FROM product where id = '%s'" % (i))
                connection.commit()
        else:
            cursor.execute("DELETE FROM product where id = '%s'" % (id))
            connection.commit()
        if cursor.rowcount >= 1:
            return True
        else:
            return False
