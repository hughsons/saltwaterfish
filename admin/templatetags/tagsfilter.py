from django import template
from models import *
from django.db import models
from django.db.models import Count, Min, Sum, Max, Avg
from django.db import connection, transaction
import logging
register = template.Library()


from datetime import date, timedelta

def GetParentCategory(category_id):
    #SELECT category_name, category_parent from category where id = 4
    cursor = connection.cursor()
    parent_id = 99999
    levels = 0
    while (parent_id > 0 and levels < 100):
      cursor.execute("SELECT id, category_name, category_parent from _category where id = %d" %category_id)
      row = cursor.fetchone()
      category_id = row[0]
      categoryid=row[0]
      category_name = row[1]
      parent_id = row[2]
      
      category_id = parent_id
      levels += 1
    #logging.info('categoryid:: %s',categoryid)
    return (categoryid, category_name, parent_id)

@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    delta = value - date.today()

    if delta.days == 0:
        return "Today!"
    elif delta.days < 1:
        return "%s %s ago!" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 1:
        return "In %s days" % delta.days
    else:
        return "hero"

@register.filter("subtractval")  
def subtractval(value, arg):
    return value - arg

@register.filter("multiplyval")  
def multiplyval(value, arg):
    return float(value) * float(arg)

@register.filter("truncate_chars")
def truncate_chars(oid,who_commented):
    crm_messages = ""
    crm_id = ""
    try:
        crm_obj = Crm.objects.all().filter(orderid = oid)
        for crms in crm_obj:
            crm_id = crms.id
            #logging.info('crmid:: %s',crms.id)
        crm_messages = CrmMessages.objects.filter(crmid=crm_id, sender=who_commented)
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    
    logging.info('crmid:: %s',crm_id)
    return crm_messages


@register.filter("orderquestions")
def orderquestions(oid,questionid):
    crm_messages = ""
    crm_id = ""
    try:
        crm_obj = OrderQuestions.objects.all().filter(orderid = oid, questionid = questionid)
        for crms in crm_obj:
            crm_id = crms.answer
            #logging.info('crmid:: %s',crms.id)
        #crm_messages = CrmMessages.objects.filter(crmid=crm_id, sender=who_commented)
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    
    logging.info('crmid:: %s',crm_id)
    return crm_id

@register.filter("orderdiscount")
def orderdiscount(oid):
    crm_messages = ""
    crm_id = ""
    try:
        crm_obj = OrderQuestions.objects.all().filter(orderid = oid, questionid = questionid)
        for crms in crm_obj:
            crm_id = crms.answer
            #logging.info('crmid:: %s',crms.id)
        #crm_messages = CrmMessages.objects.filter(crmid=crm_id, sender=who_commented)
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    
    logging.info('crmid:: %s',crm_id)
    return crm_id

@register.filter("rmastatus")
def rmastatus(statusid):
    result = ""
    try:
        crm_obj = Rmastatus.objects.all().filter(idrmastatus = statusid)
        for crms in crm_obj:
            result = crms.rmastatus
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("rmamethods")
def rmamethods(statusid):
    result = ""
    try:
        crm_obj = Rmamethod.objects.all().filter(idrmamethod = statusid)
        for crms in crm_obj:
            result = crms.rmamethod
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("rmareasons")
def rmareasons(statusid):
    result = ""
    try:
        crm_obj = Rmareason.objects.all().filter(idrmareason = statusid)
        for crms in crm_obj:
            result = crms.rmareason
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    return result


@register.filter("rmaordervalues")
def rmaordervalues(oid,field):
    
    result = ""
    try:
        crm_obj = Orders.objects.all().filter(orderid = oid)
        for crms in crm_obj:
            if field == "invoicenum_prefix":
                result = crms.invoicenum_prefix
            elif field == "invoicenum":
                result = crms.invoicenum
            else:
                result = crms.ofirstname + ' ' +crms.olastname
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    logging.info('LoginfoMessage:: %s',result)
    return result

@register.filter("shippingcountries")
def shippingcountries(field):
    logging.info('field name:: %s',field)
    try:
        if field == 'states':
            countries = ShippingStates.objects.all()
        else:
            countries = ShippingCountries.objects.all()
            
    except Exception as e:
        countries = e
        logging.info('LoginfoMessage:: %s',e)
    return countries

@register.filter("categoriesdisplay")
def categoriesdisplay(parent):
    #logging.info('category name:: %s',parent)
    try:
        if parent != '':
            result = Category.objects.all().filter(category_parent = parent, hide=0).order_by('category_name')
        else:
            result = Category.objects.all().filter(hide=0)
            
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("productsdisplay")
def productsdisplay(category,count="",noi=""):
    logging.info('field name:: %s',category)
    noi = noi if noi !="" else 12
    try:
        if count =="":
            if category != '':
                result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and hide=0 and categoryid = %s',category)
            else:
                result = Products.objects.all()
        else:
            result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and hide=0 and categoryid = %s',category)
            result = sum(1 for result in result)
            logging.info('count:: %s',result)
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("featureddisplay")
def featureddisplay(category,count="",noi=""):
    logging.info('Category name:: %s',category)
    noi = noi if noi !="" else 3
    try:
        if count == "":
            if category != '':
                catparent = Category.objects.all().filter(id = category, category_parent=1).count()
                logging.info('Category_Parent:: %s',catparent)
                if catparent ==0:
                    result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and products.categoryspecial=1 and hide=0 and categoryid = %s',category)[:noi]
                else:
                    product_category = Category.objects.all().filter(category_parent = catparent, hide=0)
                    pcats =""
                    for pwcats in product_category:
                        pcats += str(pwcats.id)+", "
                    pcats = pcats[:-2]+''
                    logging.info('Category_Products:: %s',pcats)
                    result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and products.categoryspecial=1 and hide=0 and categoryid in ('+pcats+') ORDER BY RAND()')[:noi]
            else:
                result = Products.objects.all()
        else:
            result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid  and hide=0 and categoryid = %s ORDER BY RAND()',category)
            result = sum(1 for result in result)
            logging.info('count:: %s',result)
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("featuredcount")
def featuredcount(category,count=""):
    logging.info('field name:: %s',category)
    try:
        results = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and hide=0 and products.categoryspecial=1 and categoryid = %s',category)
        result = sum(1 for result in results)
        logging.info('sum total:: %s',result)
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("crmdepartment")
def crmdepartment(department):
    logging.info('department name:: %s',department)
    try:
        if department != '':
            result = CrmDepartment.objects.all().filter(id = department)
            #result = result['department]
        else:
            result = CrmDepartment.objects.all()
            
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result


@register.filter("crmlastmessage")
def crmlastmessage(crmid,limits=""):
    logging.info('crmid name:: %s',limits)
    
    try:
        if crmid != '':
            if limits != "all":
                result = CrmMessages.objects.all().filter(crmid = crmid).order_by('-id')[0:1]
            else:
                result = CrmMessages.objects.all().filter(crmid = crmid).order_by('-id')
        else:
            result = CrmMessages.objects.all()
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("crmstatus")
def crmstatus(crmid,limits=""):
    #logging.info('crmid name:: %s',limits)
    try:
        if crmid != '':
            if limits != "all":
                result = CrmStatus.objects.all().filter(id = crmid).order_by('-id')[0:1]
            else:
                result = CrmStatus.objects.all().filter(id = crmid).order_by('-id')
        else:
            result = CrmStatus.objects.all()
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("fetchproduct")
def fetchproduct(pid):
    logging.info('product name:: %s',id)
    final_result= {}
    try:
        if pid != '':
            result = Products.objects.raw("select * from products where catalogid=%s",pid )
        else:
            result = Products.objects.all()
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    logging.info('filter tag result:: %s',result)
    return result

@register.filter("strreplace")
def strreplace(strtag,replacetag="",replacewith=""):
    try:
        result = strtag.replace(replacetag, "")
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("fetchoitems")
def fetchoitems(pid):
    logging.info('product name:: %s',pid)
    final_result= {}
    try:
        if pid != '':
            result = Oitems.objects.raw("select * from oitems where orderitemid=%s",pid )
        else:
            result = Oitems.objects.all()
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    logging.info('filter tag result:: %s',result)
    return result

@register.filter("fetchrmaoitem")
def fetchrmaoitem(pid):
    logging.info('product name:: %s',pid)
    final_result= {}
    try:
        if pid != '':
            result = RmaOitem.objects.all().filter(orderitemid=pid)
        else:
            result = RmaOitem.objects.all()
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    logging.info('filter tag result:: %s',result)
    return result

@register.filter("featuredcount")
def featuredcount(category,count=""):
    logging.info('field name:: %s',category)
    try:
        results = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and hide=0 and products.categoryspecial=1 and categoryid = %s',category)
        result = sum(1 for result in results)
        logging.info('sum total:: %s',result)
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("relatedpitems")
def relatedpitems(pid,count=""):
    logging.info('field name:: %s',pid)
    try:
        results = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid and hide=0 and products.catalogid = %s',pid)[:1]
        for prods in results:
            result=prods.categoryid
        categoryid, category_name, parent_id = GetParentCategory(result)
        result = category_name
        #logging.info('sum total:: %s',category_name)
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result
