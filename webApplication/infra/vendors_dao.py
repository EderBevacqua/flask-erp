from contextlib import closing
import mysql.connector
from ..model.vendor import Vendor
from .db_config import con


def listVendors_dao():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("select p.id, v.id as vendorID, v.vendorName, v.cnpj, v.city, p.productName, p.productCode, p.price from product as p right join vendor as v on v.id = p.vendorID order by 2")
        rows = cursor.fetchall()
        result = []
        if rows:
            for (id, vendorID, vendorName, cnpj, city, productName, productCode, price) in rows:
                if result != []:
                    if result[-1].id == vendorID:
                        if id != None:
                            result[-1].add_products(id, vendorID,
                                                    productName, productCode, price)
                    else:
                        result.append(Vendor.newVendor(
                            {"id": vendorID, "vendorName": vendorName, "cnpj": cnpj, "city": city}))
                        if id != None:
                            result[-1].add_products(id, vendorID,
                                                    productName, productCode, price)
                else:
                    result.append(Vendor.newVendor(
                        {"id": vendorID, "vendorName": vendorName, "cnpj": cnpj, "city": city}))
                    if id != None:
                        result[-1].add_products(id, vendorID,
                                                productName, productCode, price)
            return result
        else:
            return []


def registerVendor_dao(newVendor):
    try:
        with closing(con()) as connection, closing(connection.cursor()) as cursor:
            sql = "INSERT INTO vendor (vendorName,cnpj,city) VALUES (%s,%s,%s)"
            cursor.execute(sql, (newVendor.vendorName,
                                 newVendor.cnpj, newVendor.city))
            connection.commit()
            cursor.execute("select LAST_INSERT_ID()")
            lastId = cursor.fetchone()
            if len(newVendor.products) > 0:
                sql2 = "INSERT INTO product (vendorID, productName, productCode, price) VALUES (%s,%s,%s,%s)"
                for p in newVendor.products:
                    cursor.execute(
                        sql2, (lastId[0], p.productName, p.productCode, p.price))
                    connection.commit()
            if cursor.rowcount >= 1:
                return True
            else:
                return False
    except Exception as err:
        return err


def findVendorId_dao(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("select p.id, v.id as vendorID, v.vendorName, v.cnpj, v.city, p.productName, p.productCode, p.price from product as p right join vendor as v on v.id = p.vendorID where v.id = '%s'" % (id))
        rows = cursor.fetchall()
        if rows:
            result = Vendor.newVendor(
                {"id": rows[0][1], "vendorName": rows[0][2], "cnpj": rows[0][3], "city": rows[0][4]})
            for (id, vendorID, vendorName, cnpj, city, productName, productCode, price) in rows:
                if id != None:
                    result.add_products(
                        id, vendorID, productName, productCode, price)
            return result
        else:
            return False


def findVendorCnpj_dao(cnpj):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("select cnpj from vendor where cnpj = '%s'" % (cnpj))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False


def findVendor_dao(data):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        queryFilter = "select p.id, v.id as vendorID, v.vendorName, v.cnpj, v.city, p.productName, p.productCode, p.price from product as p right join vendor as v on v.id = p.vendorID where"
        if data.id != "":
            queryFilter += " p.vendorID = '"+str(data.id)+"' AND "
        if data.vendorName != "":
            queryFilter += " v.vendorName = '"+data.vendorName+"' AND "
        if data.cnpj != "":
            queryFilter += " v.cnpj = '"+data.cnpj+"' AND "
        if data.city != "":
            queryFilter += " v.city = '"+data.city+"' AND "
        if queryFilter[-5::] == "where":
            return []
        queryFilter = queryFilter[:-5]+" order by 2"
        cursor.execute(queryFilter)
        rows = cursor.fetchall()
        result = []
        if rows:
            for (id, vendorID, vendorName, cnpj, city, productName, productCode, price) in rows:
                if result != []:
                    if result[-1].id == vendorID:
                        if id != None:
                            result[-1].add_products(id, vendorID,
                                                    productName, productCode, price)
                    else:
                        result.append(Vendor.newVendor(
                            {"id": vendorID, "vendorName": vendorName, "cnpj": cnpj, "city": city}))
                        if id != None:
                            result[-1].add_products(id, vendorID,
                                                    productName, productCode, price)
                else:
                    result.append(Vendor.newVendor(
                        {"id": vendorID, "vendorName": vendorName, "cnpj": cnpj, "city": city}))
                    if id != None:
                        result[-1].add_products(id, vendorID,
                                                productName, productCode, price)
            return result
        else:
            return []


def removeVendor_dao(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        if type(id) == list:
            for i in id:
                cursor.execute(
                    "DELETE FROM product where vendorID = '%s'" % (i))
                connection.commit()
                cursor.execute("DELETE FROM vendor where id = '%s'" % (i))
                connection.commit()
        else:
            cursor.execute("DELETE FROM product where vendorID = '%s'" % (id))
            connection.commit()
            cursor.execute("DELETE FROM vendor where id = '%s'" % (id))
            connection.commit()
        if cursor.rowcount >= 1:
            return True
        else:
            return False


def alterVendor_dao(data):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute("""UPDATE vendor set vendorName = "%s", cnpj = "%s", city = "%s" where id = "%s";""" % (
            data.vendorName, data.cnpj, data.city, data.id))
        connection.commit()
        if cursor.rowcount >= 1:
            return True
        else:
            return False
