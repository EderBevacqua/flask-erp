from validate_docbr import CNPJ
from ..infra.vendors_dao import \
    listVendors_dao,\
    registerVendor_dao,\
    findVendorId_dao,\
    findVendorCnpj_dao,\
    findVendor_dao,\
    removeVendor_dao,\
    alterVendor_dao

from ..model.vendor import Vendor


def listVendors_service():
    return listVendors_dao()


def registerVendor_service(registerVendor):
    return registerVendor_dao(registerVendor)


def findVendorId_service(id):
    result = findVendorId_dao(id)
    if result != False:
        return [result]
    else:
        return []


def findVendorCnpj_service(cnpj):
    return findVendorCnpj_dao(cnpj)


def validateCnpj_service(cnpjVendor):
    cnpj = CNPJ()
    return cnpj.validate(cnpjVendor)


def findVendor_service(data):
    return findVendor_dao(data)


def removeVendor_service(id):
    return removeVendor_dao(id)


def alterVendor_service(data):
    return alterVendor_dao(data)
