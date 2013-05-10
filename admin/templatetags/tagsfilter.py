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
            else:
                result = crms.ofirstname + ' ' +crms.olastname
    except Exception as e:
        crm_id = e
        logging.info('LoginfoMessage:: %s',e)
    logging.info('LoginfoMessage:: %s',result)
    return result
