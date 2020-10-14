from flask import Blueprint, request, render_template, redirect, flash
from .model.vendor import Vendor
from .services.vendors_services import \
    listVendors_service,\
    registerVendor_service,\
    findVendorId_service,\
    findVendorCnpj_service,\
    findVendor_service,\
    removeVendor_service,\
    alterVendor_service,\
    validateCnpj_service

vendors_app = Blueprint('vendors_app', __name__,
                        template_folder='templates', static_folder='static', static_url_path="/webApplication/static")


@vendors_app.route('/', methods=['GET'])
def index():
    vendors = listVendors_service()
    if vendors == []:
        flash("list empty")
        return render_template("/index.html", vendors=[])
    else:
        return render_template("/index.html", vendors=vendors)


@vendors_app.route('/vendors', methods=['GET'])
def vendors():
    vendors = listVendors_service()
    if vendors == []:
        flash("list vendors empty")
        return render_template("/vendors/vendors.html", vendors=[])
    else:
        return render_template("/vendors/vendors.html", vendors=vendors)


@vendors_app.route('/vendors/remove/<id>', methods=['GET', 'POST'])
def remoVevendor(id):
    if removeVendor_service(id) != False:
        flash("Vendor removed")
        return redirect("/vendors")
    else:
        flash("Vendor not removed")
        return redirect("/vendors")


@vendors_app.route('/vendors/multiremove', methods=['POST'])
def multiRemoveVendor():
    if request.method == "POST":
        ids = request.form.getlist('checkRemove')
        result = [int(id) for id in ids]
        remove = removeVendor_service(result)
        if remove == True and ids != []:
            flash("Vendors removed")
            return redirect("/vendors")
        else:
            flash("Unable to remove vendors")
            return redirect("/vendors")


@vendors_app.route('/vendors/register', methods=['POST'])
def registerVendor():
    try:
        newVendor = request.form.to_dict()
        newVendor.update({"id": ""})
        newRegister = Vendor.newVendor(newVendor)
        if findVendorCnpj_service(newRegister.cnpj) == False:
            if validateCnpj_service(newRegister.cnpj) == False:
                flash('Invalid cnpj')
                return redirect('/vendors')
            reg = registerVendor_service(newRegister)
            if reg == True:
                flash('Register successful')
                return redirect('/vendors')
            else:
                flash('Not registered')
                return redirect('/vendors')
        else:
            flash('CNPJ already registered')
            return redirect('/vendors')
    except Exception as e:
        flash('Error: ', str(e))
        return redirect('/vendors')


@vendors_app.route('/vendors/alter', methods=['GET', 'POST'])
def alterVendor():
    alterVendor = request.form.to_dict()
    vendor = findVendorId_service(alterVendor["id"])
    if vendor != []:
        if vendor[0].cnpj != alterVendor.get("cnpj"):
            if findVendorCnpj_service(alterVendor["cnpj"]) == True:
                flash('CNPJ already registered')
                return redirect('/vendors')
            if validateCnpj_service(alterVendor["cnpj"]) == False:
                flash('Invalid cnpj')
                return redirect('/vendors')
        vendor = Vendor.newVendor(alterVendor)
        if alterVendor_service(vendor) == True:
            flash("Vendor modified")
            return redirect("/vendors")
        else:
            flash("Not modified")
            return redirect("/vendors")


@vendors_app.route('/vendors/find', methods=['POST'])
def findVendor():
    if request.method == 'POST':
        find = request.form.to_dict()
        fvendor = Vendor.newVendor(find)
        vendor = findVendor_service(fvendor)
        if vendor != []:
            return render_template("/vendors/vendors.html", vendors=vendor)
        else:
            flash("Not Found")
            return redirect("/vendors")
