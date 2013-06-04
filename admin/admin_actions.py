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
import logging, datetime, hashlib

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
                if "tax_shipping" in request.POST:
                    t.tax_shipping = 1
                else:
                    t.tax_shipping = 0
                if "taxdiscount" in request.POST:
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
        elif "action" in request.POST and request.POST['action'] == "massedit" and request.POST['bacthaction'] != '':
            try:
                if request.POST['bacthaction'] == "delete":
                    for a in request.POST.getlist('delid'):
                        Promotions.objects.filter(id=a).delete()
                        logging.info('Deleting this Record:: %s',a)
                    return HttpResponseRedirect('/couponmanager?page=1&msg=Successfully Deleted the Record')
                elif request.POST['bacthaction'] == "disable":
                    for a in request.POST.getlist('delid'):
                        t = Promotions.objects.get(id=a)
                        t.promotion_enabled =0
                        t.save()
                        logging.info('Disabling this Record:: %s',a)
                    return HttpResponseRedirect('/couponmanager?page=1&msg=Successfully Disabled the Record')
                elif request.POST['bacthaction'] == "enable":
                    for a in request.POST.getlist('delid'):
                        t = Promotions.objects.get(id=a)
                        t.promotion_enabled =1
                        t.save()
                        logging.info('Enabling this Record:: %s',a)
                    return HttpResponseRedirect('/couponmanager?page=1&msg=Successfully Enabled the Record')
                else:
                    return HttpResponseRedirect('/couponmanager?page=1&err=Form Field Errors')
                    
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponse('/couponmanager?page=1&err=Form Field Errors')

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
        elif "action" in request.POST and request.POST['action'] == "editbanner":
            try:
                t = SiteBanners.objects.get(id=request.POST['id'])
                t.banner_name = request.POST['banner_name']
                t.banner_type = request.POST['banner_type']
                t.banner_content = request.POST['banner_content']
                t.banner_link = request.POST['banner_link']
                t.banner_status = request.POST['banner_status']
                t.datentime = datetime.datetime.now()
                t.save()
                return HttpResponseRedirect('/viewbanners?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/viewbanners?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addbanner":
            try:
                t = SiteBanners(banner_name = request.POST['banner_name'],
                               banner_type = request.POST['banner_type'],
                               banner_content = request.POST['banner_content'],
                               banner_link = request.POST['banner_link'],
                               banner_status = request.POST['banner_status'],
                               datentime = datetime.datetime.now())
                t.save()
                return HttpResponseRedirect('/viewbanners?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/viewbanners?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['action'] != "delbanner" and request.GET['id'] != "" :
            try:
                Extrapages.objects.filter(id=request.GET['id']).delete()
                return HttpResponseRedirect('/cmspages?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/cmspages?page=1&err=Form Field Errors')
        elif "action" in request.GET and request.GET['action'] == "delbanner" and request.GET['bid'] != "":
            try:
                SiteBanners.objects.filter(id=request.GET['bid']).delete()
                return HttpResponseRedirect('/viewbanners?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/viewbanners?page=1&err=Form Field Errors')


class EmailManagerActionClass(LoginRequiredMixin,TemplateView):
    @csrf_exempt
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


class StaffActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            try:
                t = Admins.objects.get(id=request.POST['id'])
                t.email = request.POST['email']
                t.ip_restricted = request.POST['ip_restricted']
                t.name = request.POST['name']
                t.save()
                return HttpResponseRedirect('/admins?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/admins?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = Admins(email = request.POST['email'], username = request.POST['username'],
                           userlevel = 0, name = request.POST['name'],
                           #ip_restricted = request.POST['ip_restricted'],
                           pass_field = hashlib.md5(request.POST['password']).hexdigest(),
                           lastchange = datetime.datetime.now())
                t.save()
                return HttpResponse('/?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponse('/admins?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "adminpass":
            try:
                staffid = request.POST['id']
                t = Admins.objects.get(id=staffid,pass_field = hashlib.md5(request.POST['old_pass']).hexdigest())
                if request.POST['new_pass2'] == request.POST['new_pass1']:
                    t.pass_field = hashlib.md5(request.POST['new_pass2']).hexdigest()
                    t.lastchange = datetime.datetime.now()
                    t.save()
                    return HttpResponseRedirect('/addadminsform?mode=change&id='+staffid+'&err=Successfully Updated the Record')
                else:
                    return HttpResponseRedirect('/addadminsform?mode=change&id='+staffid+'&err=Form Field Errors')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/addadminsform?mode=change&id='+staffid+'&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/admins?page=1&err=Form Field Errors')

class CustomerActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "edit":
            custid = request.POST['id']
            try:
                t = customers.objects.get(contactid=request.POST['id'])
                #t.email = request.POST['email']
                t.pass_field = request.POST['pass_field']
                t.billing_company = request.POST['billing_company']
                t.billing_firstname = request.POST['billing_firstname']
                t.billing_lastname = request.POST['billing_lastname']
                t.billing_address = request.POST['billing_address']
                t.billing_address2 = request.POST['billing_address2']
                t.billing_city = request.POST['billing_city']
                t.billing_state = request.POST['billing_state']
                t.billing_zip = request.POST['billing_zip']
                t.billing_country = request.POST['billing_country']
                t.billing_phone = request.POST['billing_phone']
                t.shipping_company = request.POST['shipping_company']
                t.shipping_firstname = request.POST['shipping_firstname']
                t.shipping_lastname = request.POST['shipping_lastname']
                t.shipping_address = request.POST['shipping_address']
                t.shipping_address2 = request.POST['shipping_address2']
                t.shipping_city = request.POST['shipping_city']
                t.shipping_state = request.POST['shipping_state']
                t.shipping_zip = request.POST['shipping_zip']
                t.shipping_country = request.POST['shipping_country']
                t.shipping_phone = request.POST['shipping_phone']
                #t.custenabled = request.POST['custenabled']
                t.accountno = request.POST['accountno']
                #logging.info('mailist:: %s',request.POST['maillist'])
                if "mailist" in request.POST.keys():
                    t.maillist = 1
                else:
                    t.mailist = 0
                t.comments = request.POST['comments']
                t.last_update = datetime.datetime.now()
                
                t.save()
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/dbcustomersinfo?id='+custid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "add":
            try:
                t = customers(email = request.POST['email'], pass_field = request.POST['pass_field'] ,
                              billing_company = request.POST['billing_company'] , billing_firstname = request.POST['billing_firstname'] ,
                              billing_lastname = request.POST['billing_lastname'] , billing_address = request.POST['billing_address'] ,
                              billing_address2 = request.POST['billing_address2'] , billing_city = request.POST['billing_city'] ,
                              billing_state = request.POST['billing_state'] , billing_zip = request.POST['billing_zip'] ,
                              billing_country = request.POST['billing_country'] , billing_phone = request.POST['billing_phone'] ,
                              shipping_company = request.POST['shipping_company'] , shipping_firstname = request.POST['shipping_firstname'] ,
                              shipping_lastname = request.POST['shipping_lastname'] , shipping_address = request.POST['shipping_address'] ,
                              shipping_address2 = request.POST['shipping_address2'] , shipping_city = request.POST['shipping_city'] ,
                              shipping_state = request.POST['shipping_state'] , shipping_zip = request.POST['shipping_zip'] ,
                              shipping_country = request.POST['shipping_country'] , shipping_phone = request.POST['shipping_phone'] ,
                              custenabled = 1 , accountno = request.POST['accountno'] , comments = request.POST['comments'] , maillist = 1 ,
                              last_update = datetime.datetime.now())
                t.save()
                return HttpResponseRedirect('/customers?page=1&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/customers?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addrewards":
            custid = request.POST['custid']
            try:
                t = CustomerRewards(contactid = custid, orderid = request.POST['orderid'],
                           datentime = datetime.datetime.now(), points = request.POST['points'],)
                t.save()
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "massdelete" and request.POST['bacthaction'] == 'delete':
            try:
                for a in request.POST.getlist('delid'):
                    customers.objects.filter(contactid=a).delete()
                    logging.info('Deleting this Record:: %s',a)
                return HttpResponseRedirect('/customers?page=1&msg=Successfully Deleted the Record')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/customers?page=1&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/customers?page=1&err=Form Field Errors')

    def get(self, request, *args, **kwargs):
        if "action" in request.GET and request.GET['action'] == "deletereward" and request.GET['reid'] != "":
            custid = request.GET['custid']
            try:
                CustomerRewards.objects.filter(id=request.GET['reid']).delete()
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Form Field Errors')
        if "action" in request.GET and request.GET['action'] == "deletestreward" and request.GET['reid'] != "":
            custid = request.GET['custid']
            storereward = request.GET['reid']
            try:
                SwfCustomerCreditsLog.objects.filter(id=storereward).delete()
                logging.info('LoginfoMessage:: %s',storereward)
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/bcustomersinfo?id='+custid+'&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/customers?page=1&err=Form Field Errors')

class CRMActionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "massaction":
            logging.info('status type:: %s',request.POST['status'])
            try:
                if "status" in request.POST and request.POST['status'] == "delete":
                    for a in request.POST.getlist('delid'):
                        Crm.objects.filter(id=a).delete()
                        logging.info('Deleting this Record:: %s',a)
                    return HttpResponseRedirect('/acrm?page=1&err=Successfully Updated the Record')
                elif "status" in request.POST and request.POST['status'] >= 1:
                    for a in request.POST.getlist('delid'):
                        t = Crm.objects.get(id=a)
                        t.status = request.POST['status']
                        t.save()
                        logging.info('updating this Record:: %s',a)
                    return HttpResponseRedirect('/acrm?page=1&err=Successfully Updated the Record')
                else:
                    return HttpResponseRedirect('/acrm?page=1&err=Form Field Errors')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/acrm?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "editcrm":
            crmid = request.POST['id']
            try:
                t = Crm.objects.get(id=crmid)
                t.custemail = request.POST['custemail']
                t.customer = request.POST['customer']
                t.phone = request.POST['phone']
                t.status = request.POST['status']
                t.save()
                return HttpResponseRedirect('/crmedit?id='+crmid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/crmedit?id='+crmid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addresponse":
            crmid = request.POST['id']
            try:
                t = Crm.objects.get(id=crmid)
                t.status = request.POST['status']
                t.save()
                s = CrmMessages(crmid = crmid, sendername = request.POST['sendername'] ,
                                sender = 0 , message = request.POST['message'] ,
                                datentime = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/crmedit?id='+crmid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/crmedit?id='+crmid+'&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/acrm?page=1&err=Form Field Errors')

class ProductsctionClass(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        if "action" in request.POST and request.POST['action'] == "massdelete" and request.POST['bacthaction'] == 'delete':
            try:
                for a in request.POST.getlist('delid'):
                    Products.objects.filter(catalogid=a).delete()
                    logging.info('Deleting this Record:: %s',a)
                return HttpResponseRedirect('/products?page=1&msg=Successfully Deleted the Record')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/products?page=1&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "editarticle":
            try:
                pid = request.POST['id']
                t = ProductArticle.objects.get(id=pid)
                t.article_title = request.POST['article_title']
                t.long_review = request.POST['long_review']
                t.review_date = datetime.datetime.now()
                
                t.save()
                logging.info('update this Record:: %s',pid)
                return HttpResponseRedirect('/productarticles?pid='+str(t.catalogid)+'&msg=Successfully Deleted the Record')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/productarticles?pid='+str(t.catalogid)+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addarticle":
            try:
                pid = request.POST['catalog']
                t = ProductArticle(catalogid=pid,
                                   article_title = request.POST['article_title'],
                                   long_review = request.POST['long_review'],
                                   review_date = datetime.datetime.now())
                t.save()
                logging.info('update this Record:: %s',pid)
                return HttpResponseRedirect('/productarticles?pid='+str(pid)+'&msg=Successfully Deleted the Record')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/productarticles?pid='+str(pid)+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "editreview":
            try:
                pid = request.POST['id']
                t = ProductReview.objects.get(id=pid)
                t.user_name = request.POST['user_name']
                t.user_email = request.POST['user_email']
                t.user_city = request.POST['user_city']
                t.short_review = request.POST['short_review']
                t.rating = request.POST['rating']
                if "approved" in request.POST:
                    t.approved = 1
                else:
                    t.approved = 0
                    
                t.long_review = request.POST['long_review']
                t.review_date = datetime.datetime.now()
                t.save()
                logging.info('update this Record:: %s',pid)
                return HttpResponseRedirect('/productreviews?pid='+str(t.catalogid)+'&msg=Successfully Deleted the Record')
                
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/productreviews?pid='+str(t.catalogid)+'&err=Form Field Errors')

        else:
            return HttpResponseRedirect('/products?page=1&err=Form Field Errors')
