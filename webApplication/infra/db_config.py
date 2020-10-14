import mysql.connector


def con():
    return mysql.connector.connect(host="localhost", user="user_app", passwd="pass_user_app", db="fast_lunch_db")


sql_create_table_vendor = "CREATE TABLE IF NOT EXISTS vendor (id INT AUTO_INCREMENT NOT NULL,vendorName varchar(50) NOT NULL, cnpj varchar(18) NOT NULL UNIQUE, city char(50), PRIMARY KEY (id));"
sql_create_table_product = "CREATE TABLE IF NOT EXISTS product (id INT AUTO_INCREMENT NOT NULL,vendorID INT NOT NULL,productName VARCHAR(50) NOT NULL, productCode INT NOT NULL, price DECIMAL(8,2), PRIMARY KEY (id), constraint vendorID_fk foreign key(vendorID) references vendor(id));"


def createTable(cursor, sql):
    cursor.execute(sql)


def popularDbVendors(cursor, id, vendorName, cnpj, city):
    sqlVendors = "INSERT IGNORE INTO vendor (id, vendorName, cnpj, city) VALUES (%s,%s,%s,%s)"
    cursor.execute(sqlVendors, (id, vendorName, cnpj, city))


def popularDbProducts(cursor, id, vendorID, productName, productCode, price):
    sqlProducts = "INSERT IGNORE INTO product (id, vendorID, productName, productCode, price) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sqlProducts, (id, vendorID,
                                 productName, productCode, price))


def init():
    con = mysql.connector.connect(
        host="localhost", user="user_app", passwd="pass_user_app")
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS fast_lunch_db")
    cursor.execute("USE fast_lunch_db")
    createTable(cursor, sql_create_table_vendor)
    createTable(cursor, sql_create_table_product)

    try:
        popularDbVendors(cursor, 1, 'Burger Bar',
                         '53.783.201/0001-79', 'Chicago')
        popularDbVendors(cursor, 2, 'Jokers Bar', '12.046.553/0001-64', 'Uta')
        popularDbVendors(cursor, 3, 'MAMA MIA',
                         '95.951.103/0001-43', 'Manhattan')

        popularDbProducts(cursor, 1, 1, 'x-Salada', 22, 15)
        popularDbProducts(cursor, 2, 1, 'x-Egg', 88, 25.50)
        popularDbProducts(cursor, 3, 2, 'x-Bacon', 44, 150.50)
        popularDbProducts(cursor, 4, 3, 'Spaguetti', 55, 150.50)

    except Exception as e:
        return {"error":str(e)}
    cursor.close()
    con.commit()
    con.close()
