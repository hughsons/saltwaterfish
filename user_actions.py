from django.http import *
from forms import UploadForm
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
#from models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import unittest
from django.core.context_processors import csrf
from forms import *
from models import *
import random
from google.appengine.api import mail
import logging, random, hashlib, datetime
#from django.db import connection, transaction
PERPAGE=50
class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response


class ForgetPasswordActionClass(TemplateView):

    def post(self, request, *args, **kwargs):
      content = {}
      content = {'page_title': "Customer Forget Password"}
      form = ForgetPwdForm(request.POST)
      if form.is_valid():
          if form.cleaned_data['recaptcha'] == str(request.session['ReCaptcha']):
            customer_list = customers.objects.filter(email = form.cleaned_data['email'])
            if customer_list:
              customer = customer_list[0]
              success = True
              store_info_list = StoreSettings2.objects.filter(id__in=[3, 5, 32]).order_by('id')
              store_name = store_info_list[0].varvalue
              store_logo = store_info_list[1].varvalue
              store_url =  store_info_list[2].varvalue

              email = Emails.objects.filter(id = 11)[0]
              mail_subject = email.subject.replace('[store_name]', store_name)
              mail_body = email.body.replace('[store_name]', store_name)
              mail_body = mail_body.replace('[store_url]', store_url)
              mail_body = mail_body.replace("[oemail]", customer.email)
              mail_body = mail_body.replace("[password]", customer.pass_field)
              #test_html = mail_subject + "<br>" + mail_body
              mail.send_mail(sender="support@saltwaterfish.com", to=customer.email, subject=mail_subject, body=mail_body)
            else:
              (success, error_msg) = (False, "Email-id is not found in our records.")
          else:
            (success, error_msg) = (False, "Recaptcha is not matched.")
      else:
        (success, error_msg) = (False, "Incomplete or invalid form data")

      if  success:
        content = {'form': form, 'page_title': "Customer Forget Password"}
        #content['recaptcha'] = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
        content['message'] = "Password has been sent to your EMail. Please check your inbox"
        content.update(csrf(request))
        return HttpResponseRedirect('login?message=%s#forget' %content['message'])
      else:
        c = {'form': form, 'error_message': error_msg}

      return HttpResponseRedirect('login?error=%s#forget' %error_msg)


class CustomerLoginActionClass(TemplateView):

  def post(self, request, *args, **kwargs):
    if request.method == 'POST':
        #logout(request)
        customer_list=""
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.info('Form Is clean')
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if form.cleaned_data['recaptcha'] == str(request.session['ReCaptcha']):
                customer_list = customers.objects.filter(email = email,
                                                         pass_field= password, custenabled=1)
                if customer_list:
                    t = customers.objects.get(email = email,
                                              pass_field= password, custenabled=1)
                    t.lastlogindate = datetime.datetime.now()
                    t.save()
                    request.session['IsLogin'] = True
                    request.session['Customer'] = customer_list[0]
                    success = True
                    logging.info('LoginfoMessage:: %s',customer_list[0])
                    return HttpResponseRedirect('/myaccount')
                else:
                    return HttpResponseRedirect('/login')
            else:
                return HttpResponseRedirect('/?error_message=Racaptcha%20not%20matched')
        else:
            return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/login')


class AddToCartActionClass(TemplateView):
  
    def get(self, request, *args, **kwargs):
      html_text = ""
      item_id = 0
      cart_items = {}
      # Checking where item_id is available on the query string or not.
      if 'item_id' in request.GET:
        item_id = int(request.GET['item_id'])
        if "CartItems" in request.session:
          cart_items = request.session["CartItems"]
          if item_id in cart_items:
            cart_items[item_id] += 1
          else:
            cart_items[item_id] = 1
          request.session["CartItems"] = cart_items
        else:
          request.session["CartItems"] = {}
        
      cart_items = request.session["CartItems"]
      for key, value in cart_items.items():
        html_text += "%d - %d<br>\n" %(key, value)
        
      return HttpResponseRedirect("cartconfirmation?itemid=%d" %item_id)


class CartActionsClass(TemplateView):

    def get(self, request, *args, **kwargs):
      if "cmdUpdate" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        cart_items = request.session["CartItems"]
        cart_items[item_id] = quantity
        request.session["CartItems"] = cart_items
        
        #return HttpResponse(request.session["CartItems"][item_id])

      if "cmdRemove" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        cart_items = request.session["CartItems"]
        del cart_items[item_id]
        request.session["CartItems"] = cart_items

      return HttpResponseRedirect('viewcart')

class RegistrationActionClass(TemplateView):

    def SaveFormData(self, p_form):
          c = customers()
          c.contactid = 2
          c.email = p_form.cleaned_data['email']
          c.pass_field = p_form.cleaned_data['password']
          c.shipping_firstname = c.billing_firstname = c.first_name = p_form.cleaned_data['first_name']
          c.shipping_lastname = c.billing_lastname = c.last_name = p_form.cleaned_data['last_name']
          c.accountno = p_form.cleaned_data['account_no']
          c.shipping_company = c.billing_company = c.company = p_form.cleaned_data['company']
          c.shipping_address = c.billing_address = c.address1 = p_form.cleaned_data['address1']
          c.shipping_address2 = c.billing_address2 = c.address2 = p_form.cleaned_data['address2']
          c.shipping_city = c.billing_city = c.city = p_form.cleaned_data['city']            
          c.shipping_state = c.billing_state = c.state = p_form.cleaned_data['state']
          c.shipping_country = c.billing_country = c.country = p_form.cleaned_data['country']
          c.shipping_zip = c.billing_zip = c.zip = p_form.cleaned_data['zip']
          c.shipping_phone = c.billing_phone =  c.phone = p_form.cleaned_data['phone']
          c.comments = p_form.cleaned_data['comments']

          if not self.IsDuplicate(c.email):
            c.save();
            return (True, "", "Customer successfully registered", c)
          else:
            return (False, "You are already a registered customer. Duplicate registrations are not allowed.", "",  None)

    def IsDuplicate(self, p_email):
      customer_list = customers.objects.filter(email=p_email)
      if customer_list:
        is_dup =  True;
      else:
        is_dup = False;
      return is_dup 

    def GetRecaptcha(self, request):
          value = random.randrange(10000, 99999, 1)
          request.session['ReCaptcha'] = value
          return value

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        content = {'form': form, 'page_title': "Customer Registration"}
        content['recaptcha'] = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
        content.update(csrf(request))
        return render_template(request, "registration.htm", content)
    
    def post(self, request, *args, **kwargs):
      content = {}
      form = RegistrationForm(request.POST)
      if form.is_valid():
        # Validating Recaptcha
        actual_recaptcha = str(request.session['ReCaptcha'])
        user_recaptcha = form.cleaned_data['recaptcha'].strip()
        if user_recaptcha != actual_recaptcha:
          success = False
          is_human = False
          error_msg = "Human verfication is failed. Please retry"
        else:
          is_human = True
  
        if is_human:
          (success, error_msg, msg, customer) = self.SaveFormData(form)
      else:
        success = False
        error_msg = "Incomplete or invalid form data" 

      if  success:
        content = {'page_title': "Customer Registration",
                       'customer': customer
                      }

        email_template = Emails.objects.filter(id=22)[0]
        recent_customer = customers.objects.latest("contactid")
        store_info_list = StoreSettings2.objects.filter(id__in=[3, 5, 32]).order_by('id')
        store_name = store_info_list[0].varvalue
        store_logo = store_info_list[1].varvalue
        store_url =  store_info_list[2].varvalue

        mail_body = email_template.body_html
        mail_body = mail_body.replace("[billing_firstname]", recent_customer.billing_firstname)
        mail_body = mail_body.replace("[billing_lastname]", recent_customer.billing_lastname) 
        mail_body = mail_body.replace("[email]", recent_customer.email)
        mail_body = mail_body.replace("[billing_address]", recent_customer.billing_address)
        mail_body = mail_body.replace("[billing_address2]", recent_customer.billing_address2)
        mail_body = mail_body.replace("[billing_city]", recent_customer.billing_city)
        mail_body = mail_body.replace("[billing_state]", recent_customer.billing_state)
        mail_body = mail_body.replace("[billing_zip]", recent_customer.billing_zip)
        mail_body = mail_body.replace("[billing_country]", recent_customer.billing_country)
        mail_body = mail_body.replace("[billing_company]", recent_customer.billing_company)
        mail_body = mail_body.replace("[comments]", recent_customer.comments)
        mail_body = mail_body.replace("[accountno]", recent_customer.accountno)
        mail_body = mail_body.replace("[store_name]", store_name)
        mail_body = mail_body.replace("[store_url]", store_url)

        mail.send_mail(sender="support@saltwaterfish.com",
              to=customer.email,
              subject="Saltwaterfish.com: Customer Registration",
              body=mail_body)

        content.update(csrf(request))
        return  render_to_response('regconfirmation.htm', content)
      else:
        content = {'form': form, 
                   'page_title': "Customer Registration",
                   'error_message': error_msg,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
                   }
      content.update(csrf(request))
      return render_to_response('registration.htm', content)

