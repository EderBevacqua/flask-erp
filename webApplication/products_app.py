from flask import Blueprint, request, render_template, redirect, flash
from .model.product import Product
from .services.vendors_services import \
    listVendors_service,\
    findVendorId_service

from .services.products_services import \
    listProducts_service,\
    registerProduct_service,\
    findProductId_service,\
    findProduct_service,\
    alterProduct_service,\
    removeProduct_service


products_app = Blueprint('products_app', __name__,
                         template_folder='templates', static_folder='static', static_url_path="/webApplication/static")


@products_app.route('/products', methods=['GET'])
def products():
    vendors = listVendors_service()
    products = listProducts_service()
    if products == []:
        flash("list products empty")
        return render_template("/products/products.html", products=[], vendorSelec=vendors)
    else:
        return render_template("/products/products.html", products=products, vendorSelec=vendors)


@products_app.route('/products/register', methods=['POST'])
def registerProducts():
    try:
        newproduct = request.form.to_dict()
        newproduct.update({"id": ""})
        if newproduct["price"] == "":
            newproduct.update({"price": 0})
        newRegister = Product.newProduct(newproduct)
        register = registerProduct_service(newRegister)
        if register == True:
            flash('Register successful')
            return redirect('/products')
        if register == False:
            flash('Not register')
            return redirect('/products')
    except Exception as e:
        flash('Error: ', str(e))
        return redirect('/products')


@products_app.route('/products/find', methods=['POST'])
def findProduct():
    if request.method == 'POST':
        find = request.form.to_dict()
        fproduct = Product.newProduct(find)
        products = findProduct_service(fproduct)
        vendors = listProducts_service()
        if products != []:
            return render_template("/products/products.html", products=products, vendorSelec=vendors)
        else:
            flash("Not Found")
            return redirect("/products")


@products_app.route('/products/alter', methods=['GET', 'POST'])
def alterProduct():
    if request.method == 'POST':
        alterProduct = request.form.to_dict()
        alterProduct.update({"vendorID":""})
        alterRegister = Product.newProduct(alterProduct)
        if alterProduct_service(alterRegister) == True:
            flash("Product modified")
            return redirect("/products")
        else:
            flash("Not modified")
            return redirect("/products")


@products_app.route('/products/multiremove', methods=['POST'])
def multiRemoveVendor():
    if request.method == "POST":
        ids = request.form.getlist('checkRemove')
        result = [int(id) for id in ids]
        remove = removeProduct_service(result)
        if remove == True:
            flash("Products removed")
            return redirect("/products")
        else:
            flash("Unable to remove Products")
            return redirect("/products")


@products_app.route('/products/remove/<id>', methods=['GET', 'POST'])
def removeProduct(id):
    if removeProduct_service(id) != False:
        flash("Product removed")
        return redirect("/products")
    else:
        flash("Product not removed")
        return redirect("/products")
