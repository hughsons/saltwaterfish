from django import template
from models import *
from django.db import models
from django.db.models import Count, Min, Sum, Max, Avg
from django.db import connection, transaction
import logging
register = template.Library()


from datetime import date, timedelta
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
            result = Category.objects.all().filter(category_parent = parent).order_by('category_name')
        else:
            result = Category.objects.all()
            
    except Exception as e:
        result = e
        logging.info('LoginfoMessage:: %s',e)
    return result

@register.filter("productsdisplay")
def productsdisplay(category,count=""):
    logging.info('field name:: %s',category)
    try:
        if count =="":
            if category != '':
                result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid  and categoryid = %s',category)
            else:
                result = Products.objects.all()
        else:
            result = Products.objects.raw('select * from product_category,products where product_category.catalogid=products.catalogid  and categoryid = %s',category)
            result = sum(1 for result in result)
            logging.info('count:: %s',result)
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
