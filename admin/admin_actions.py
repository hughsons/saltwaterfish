from django.http import *
from forms import UploadForm
from django import template
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group, Permission
from models import *
from django.db import models
from django.db.models import Count, Min, Sum, Max, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import unittest
from django.db import connection, transaction
import logging
import datetime
from admin.views import LoginRequiredMixin
PERPAGE=50
class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)


@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

class ShippingManagerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            p = ShippingCategory(ship_categoryname=request.POST['ship_categoryname'], status=request.POST['status'])
            p.save()
            return HttpResponseRedirect('/adminshippingmanager?err=Successfully Added')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponseRedirect('/adminshippingmanager?err=Form Field Errors')

class TaxManagerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            try:
                t = Tax.objects.get(id=request.POST['id'])
                t.tax_code = int(request.POST['tax_code'])
                #t.tax_value1 = int(request.POST['tax_value1'])
                if request.POST['taxshipping'] == "" or request.POST['taxshipping'] != "":
                    t.tax_shipping = 1
                else:
                    t.tax_shipping = 0
                if "taxdiscount" in request.POST and request.POST['taxdiscount'] != "" :
                    t.tax_discount = 1
                else:
                    t.tax_discount = 0
                
                t.save()
                return HttpResponseRedirect('/taxmanager?err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/taxmanager?err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = Tax(tax_country = request.POST['tax_country'],
                        tax_shipping = '0',
                        tax_discount = '0',
                        tax_state = request.POST['tax_state'],
                        tax_zip_low = request.POST['tax_zip_low'],
                        tax_zip_high = request.POST['tax_zip_high'],
                        tax_value1 = request.POST['tax_value1'])
                t.save()
                return HttpResponseRedirect('/taxmanager?page=1&err=Successasfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/taxmanager?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/taxmanager?page=1&err=Form Field Errors')

class CMSManagerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            try:
                t = Extrapages.objects.get(id=request.POST['id'])
                t.htmlpage = request.POST['htmlpage']
                t.title = request.POST['title']
                t.content = request.POST['content']
                t.keywords = request.POST['keywords']
                t.link = request.POST['link']
                t.last_update = datetime.datetime.now()
                t.save()
                return HttpResponseRedirect('/cmspages?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = Extrapages(htmlpage = request.POST['htmlpage'],
                               title = request.POST['title'],
                               content = request.POST['content'],
                               keywords = request.POST['keywords'],
                               link = request.POST['link'],
                               last_update = datetime.datetime.now())
                t.save()
                return HttpResponseRedirect('/cmspages?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['id'] != "":
            try:
                Extrapages.objects.filter(id=request.GET['id']).delete()
                return HttpResponseRedirect('/cmspages?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')

class EmailManagerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            t = Emails.objects.get(id=request.POST['id'])
            t.name = request.POST['name'],
            t.etype = request.POST['etype'],
            t.subject = request.POST['subject'],
            t.body = request.POST['body'],
            t.body_html = request.POST['body_html'],
            t.to = request.POST['to'],
            t.save()
            return HttpResponseRedirect('/emailpages?page=1&err=Successfully Updated the Record')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponseRedirect('/emailpages?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['id'] != "":
            try:
                Emails.objects.filter(id=request.GET['id']).delete()
                return HttpResponseRedirect('/emailpages?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/emailpages?page=1&err=Form Field Errors')

class GiftManagerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            try:
                t = GiftCertificates.objects.get(id=request.POST['id'])
                t.certificate_name = request.POST['certificate_name']
                t.certificate_amount = request.POST['certificate_amount']
                
                t.save()
                return HttpResponseRedirect('/giftcertificates?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = GiftCertificates(certificate_name = request.POST['certificate_name'],
                                     certificate_amount = request.POST['certificate_amount'],
                                     certificate_date = datetime.datetime.now())
                t.save()
                return HttpResponseRedirect('/giftcertificates?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['id'] != "":
            try:
                GiftCertificates.objects.filter(id=request.GET['id']).delete()
                return HttpResponseRedirect('/giftcertificates?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')
            
class OrderStatusActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            try:
                t = OrderStatus.objects.get(id=request.POST['id'])
                t.statustext = request.POST['statustext']
                t.statusdefinition = request.POST['statusdefinition']
                t.statusid = request.POST['statusid']
                if 'Visible' in request.POST:
                    t.Visible = 1
                    logging.info('visible:: %s',request.POST['Visible'])
                else:
                    t.Visible = 0
                    logging.info('invisible:: %s',request.POST['Visible'])
                
                t.save()
                return HttpResponseRedirect('/ordersstatus?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/ordersstatus?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = GiftCertificates(certificate_name = request.POST['certificate_name'],
                                     certificate_amount = request.POST['certificate_amount'],
                                     certificate_date = datetime.datetime.now())
                t.save()
                return HttpResponseRedirect('/giftcertificates?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['id'] != "":
            try:
                GiftCertificates.objects.filter(id=request.GET['id']).delete()
                return HttpResponseRedirect('/giftcertificates?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/giftcertificates?page=1&err=Form Field Errors')
