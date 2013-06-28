from django.http import *
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import unittest
from django.core.context_processors import csrf
from forms import *
from views import *
from models import *
from google.appengine.api import mail
import logging, random, hashlib, datetime, settings
from quix.pay.transaction import CreditCard
from quix.pay.gateway.authorizenet import AimGateway
from classes import *
#from django.db import connection, transaction
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
              try:
                mail.send_mail(sender="support@saltwaterfish.com", to=customer.email, subject=mail_subject, body=mail_body)
              except Exception:
                request.session["ErrorMessage2"] = "Sorry, Unable to send an e-mail"
                (success, error_msg) = (False, "Sorry, Unable to send an e-mail")
            else:
              request.session["ErrorMessage2"] = "Email-id is not found in our records."
              (success, error_msg) = (False, "Email-id is not found in our records.")
          else:
            request.session["ErrorMessage2"] = "Recaptcha is not matched."
            (success, error_msg) = (False, "Recaptcha is not matched.")
      else:
        request.session["ErrorMessage2"] = "Invalid or Incomplete form data."
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

class RegistrationActionClassOld(TemplateView):
    '''Page: /registeruser '''

    def SaveFormData(self, p_form):
          c = customers()
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
          c.custenabled = 1
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
         
        content.update(csrf(request))
        content.update(leftwidget(request))
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
          if success:
             request.session['Message'] = "Customer successfully registered."
          else:
             request.session['ErrorMessage'] = "You are already a registered customer. Duplicate registrations are not allowed."
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

        try:
          mail.send_mail(sender="support@saltwaterfish.com",
                to=customer.email,
                subject="Saltwaterfish.com: Customer Registration",
                body=mail_body)
        except Exception:
          request.session['ErrorMessage'] = "Unable to send confirmation email."

        message = ''
        error_message = ''
        if 'Message' in request.session:
          message = request.session['Message']
          del request.session['Message']

        if 'ErrorMessage' in request.session:
          error_message = request.session['ErrorMessage']
          del request.session['ErrorMessage']

        content['message'] = message
        content['error_message'] = error_message
        
        content.update(csrf(request))
        return  render_to_response('regconfirmation.html', content)
      else:
        content = {'form': form,
                   'page_title': "Customer Registration",
                   'error_message': error_msg,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
                   }
      content.update(csrf(request))
      content.update(leftwidget(request))
      return render_to_response('registration.htm', content)

class RegistrationActionClass(TemplateView):
    '''Page: /registeruser '''

    def SaveFormData(self, p_form, IsShippingSame):
          c = customers()
          c.email = p_form.cleaned_data['email']
          c.pass_field = p_form.cleaned_data['password']

          c.billing_firstname =  p_form.cleaned_data['billing_first_name']
          c.billing_lastname =  p_form.cleaned_data['billing_last_name']
          #c.accountno = p_form.cleaned_data['account_no']
          c.billing_company =  p_form.cleaned_data['billing_company']
          c.billing_address =  p_form.cleaned_data['billing_address1']
          c.billing_address2 =  p_form.cleaned_data['billing_address2']
          c.billing_city =  p_form.cleaned_data['billing_city']            
          c.billing_state =  p_form.cleaned_data['billing_state']
          c.billing_country = p_form.cleaned_data['billing_country']
          c.billing_zip = p_form.cleaned_data['billing_zip']
          c.billing_phone =  p_form.cleaned_data['billing_phone_part1'] +  p_form.cleaned_data['billing_phone_part1'] +  p_form.cleaned_data['billing_phone_part1']
          c.custenabled = 1

          
          if IsShippingSame:
            c.shipping_firstname = c.billing_firstname =  p_form.cleaned_data['billing_first_name']
            c.shipping_lastname = c.billing_lastname =  p_form.cleaned_data['billing_last_name']
            #c.accountno = p_form.cleaned_data['account_no']
            c.shipping_company = c.billing_company =  p_form.cleaned_data['billing_company']
            c.shipping_address = c.billing_address =  p_form.cleaned_data['billing_address1']
            c.shipping_address2 = c.billing_address2 = p_form.cleaned_data['billing_address2']
            c.shipping_city = c.billing_city = p_form.cleaned_data['billing_city']            
            c.shipping_state = c.billing_state =  p_form.cleaned_data['billing_state']
            c.shipping_country = c.billing_country =  p_form.cleaned_data['billing_country']
            c.shipping_zip = c.billing_zip =  p_form.cleaned_data['billing_zip']
            c.shipping_phone = c.billing_phone = p_form.cleaned_data['billing_phone_part1'] +  p_form.cleaned_data['billing_phone_part1'] +  p_form.cleaned_data['billing_phone_part1']
            
          else: 
            c.shipping_firstname =  p_form.cleaned_data['shipping_first_name']
            c.shipping_lastname =  p_form.cleaned_data['shipping_last_name']
            #c.accountno = p_form.cleaned_data['account_no']
            #c.shipping_company =  p_form.cleaned_data['company']
            c.shipping_address =  p_form.cleaned_data['shipping_address1']
            c.shipping_address2 =  p_form.cleaned_data['shipping_address2']
            c.shipping_city =  p_form.cleaned_data['shipping_city']            
            c.shipping_state =  p_form.cleaned_data['shipping_state']
            c.shipping_country = p_form.cleaned_data['shipping_country']
            c.shipping_zip = p_form.cleaned_data['shipping_zip']
            c.shipping_phone =  p_form.cleaned_data['shipping_phone_part1'] +  p_form.cleaned_data['shipping_phone_part1'] +  p_form.cleaned_data['shipping_phone_part1'] 
            
            
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
         
        content.update(csrf(request))
        content.update(leftwidget(request))
        return render_template(request, "registration.htm", content)
    
    def post(self, request, *args, **kwargs):
      content = {}
      form = RegistrationForm(request.POST)
      
      if 'IsShippingAddressSame' in request.POST:
        is_shipping_address_same = True
      else:
        is_shipping_address_same = False

      if form.is_valid():
        (success, error_msg, msg, customer) = self.SaveFormData(form, is_shipping_address_same)
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
        #mail_body = mail_body.replace("[accountno]", recent_customer.accountno)
        mail_body = mail_body.replace("[store_name]", store_name)
        mail_body = mail_body.replace("[store_url]", store_url)

        try:
          mail.send_mail(sender="support@saltwaterfish.com",
                to=customer.email,
                subject="Saltwaterfish.com: Customer Registration",
                body=mail_body)
        except Exception:
          request.session['ErrorMessage'] = "Unable to send confirmation email."

        message = ''
        error_message = ''
        if 'Message' in request.session:
          message = request.session['Message']
          del request.session['Message']

        if 'ErrorMessage' in request.session:
          error_message = request.session['ErrorMessage']
          del request.session['ErrorMessage']

        content['message'] = message
        content['error_message'] = error_message
        
        content.update(csrf(request))
        if 'target_page' in request.session:
          render_to_response(request.session[target_page], content)

        return  render_to_response('regconfirmation.html', content)
      else:
        content = {'form': form,
                   'page_title': "Customer Registration",
                   'error_message': error_msg,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
                   }

      content.update(csrf(request))
      content.update(leftwidget(request))
      return render_to_response('registration1.html', content)


class UpdateAddressActionClass(LoginRequiredMixin,TemplateView):

  def get(self, request, *args, **kwargs):
    logging.info('\n\nUpdating Address\n\n')
    content = {}
    form = AddressForm(request.GET)

    if form.is_valid():
      address_type = form.cleaned_data['address_type'].strip()
    else:
      logging.info('\n\nForm is not valid\n\n')

    customer = request.session['Customer']
    html = "Billing Address is updated"
    if address_type == "billing":
      logging.info('\n\n   Updating Billing Address\n\n')
      customer.billing_firstname = form.cleaned_data['first_name'].strip()
      customer.billing_lastname = form.cleaned_data['last_name'].strip()
      customer.billing_address = form.cleaned_data['address1'].strip()
      customer.billing_address2 = form.cleaned_data['address2'].strip()
      customer.billing_city = form.cleaned_data['city'].strip()
      customer.billing_state = form.cleaned_data['state'].strip()
      customer.billing_country = form.cleaned_data['country'].strip()
      customer.billing_zip = form.cleaned_data['zip'].strip()
      customer.billing_company = form.cleaned_data['company'].strip()
      customer.billing_phone = form.cleaned_data['phone'].strip()
      customer.save()
      request.session['Customer'] = customer
      html = "<h4>Billing Address is updated</h4>"
    elif address_type == "shipping":
      logging.info('\n\n   Updating Billing Address\n\n')
      customer.shipping_firstname = form.cleaned_data['first_name'].strip()
      customer.shipping_lastname = form.cleaned_data['last_name'].strip()
      customer.shipping_address = form.cleaned_data['address1'].strip()
      customer.shipping_address2 = form.cleaned_data['address2'].strip()
      customer.shipping_city = form.cleaned_data['city'].strip()
      customer.shipping_state = form.cleaned_data['state'].strip()
      customer.shipping_country = form.cleaned_data['country'].strip()
      customer.shipping_zip = form.cleaned_data['zip'].strip()
      customer.shipping_company = form.cleaned_data['company'].strip()
      customer.shipping_phone = form.cleaned_data['phone'].strip()
      customer.save()
      request.session['Customer'] = customer
     
      html = "<h4>Shipping Address is updated</h4>"
    return HttpResponse(html)

class ChangePwdActionClass(TemplateView):

  def post(self, request, *args, **kwargs):
    form = ChangePwdForm(request.POST)
    if form.is_valid():
      customer = request.session["Customer"]
      email = form.cleaned_data['username']
      old_password = form.cleaned_data['old_password']
      new_password = form.cleaned_data['new_password']
      logging.info("\n\n\nEMail:%s" %email)
      logging.info("OldPassword: %s" %old_password)
      logging.info("New Password: %s\n\n\n" %new_password)
      customer_list = customers.objects.filter(contactid = customer.contactid, pass_field = old_password)
      logging.info("\n\n\n\n\nNumber of Customers %d\n\n\n\n" %len(customer_list))
      if not customer_list:
        logging.info("\n\n\n\n\nError\n\n\n\n")
        request.session["ErrorMessage"] = "Authentication failed. Current password is not matched."
        return HttpResponseRedirect('/changepwd')

      customer = customer_list[0]
      customer.pass_field = new_password
      customer.save()
      request.session['Customer'] = customer
      request.session["Message"] = "Your password is successfully changed."
      return HttpResponseRedirect('/myaccount')
    else:
      request.session["ErrorMessage"] = "Incomplete Form Data"
      return HttpResponseRedirect('/changepwd')

    return HttpResponseRedirect('/myaccount')

"""
class AddToWatchActionClass(TemplateView):

    def get(self, request, *args, **kwargs):
      wsh_id = -1
      item_id = int(request.GET['itemid'])
      if 'Customer' not  in request.session:
          return HttpResponseRedirect("login?target=addtowatchlist?itemid=%d" %item_id)

      customer = request.session['Customer']
      if "WSH_ID" not in request.session:
        wishList = WshWishlist()
        wishList.customerid = customer.contactid
        wishList.wsh_name = "WISHLIST"
        wishList.wsh_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        wishList.save()
        last_item = WshWishlist.objects.latest('wsh_id')
        wsh_id = last_item.wsh_id
        request.session['WSH_ID'] = last_item.wsh_id
        #request.session["Message"] = "Your Item has been added to 'Default Wish List'"
      else:
        wsh_id =  request.session['WSH_ID']

      # Checking whether the item is already added in the wishlist or not.
      object_list = WsiWishlistitems.objects.filter(wsh_id = wsh_id, catalogid = item_id)

      if object_list:
        request.session["ErrorMessage"] = "Item is already in your wishlist."
        return HttpResponseRedirect('/productlist')
      
      # Adding items to the detail table.
      wish_list_item = WsiWishlistitems()
      wish_list_item.wsh_id = wsh_id
      wish_list_item.catalogid = item_id
      wish_list_item.save()

      request.session["Message"] = "Item is added to your wish list"

      return HttpResponseRedirect('/mywishlist')
"""
class AddToWatchActionClass(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            item_id = int(request.GET['itemid'])
            if 'Customer' in request.session:
                t = ProductWaitinglist.objects.filter(catalogid=item_id, userid=request.session['Customer'].contactid)
                count = t.count()
                if count <= 0:
                    logging.info('count:: %s',count)
                    s = ProductWaitinglist(userid=request.session['Customer'].contactid, catalogid=item_id ,
                                    user_email = request.session['Customer'].email, record_date = datetime.datetime.now())
                    s.save()
                    return HttpResponse('<h2>Item is added to your wish list</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')
                else:
                    logging.info('count:: %s',count)
                    return HttpResponse('<h2>Item Already Exists</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')
            else:
                s = ProductWaitinglist(userid=0, catalogid=item_id ,user_name = request.GET['name'],
                                       user_email = request.GET['email'], record_date = datetime.datetime.now())
                s.save()
                return HttpResponse('<h2>Item is added to Wish list</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponse('<h2>Item Already Exists</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')
    def post(self, request, *args, **kwargs):
        try:
            item_id = int(request.GET['itemid'])
            t = ProductWaitinglist.objects.filter(catalogid=item_id, userid=request.session['Customer'].contactid)
            count = t.count()
            if count <= 0:
                logging.info('count:: %s',count)
                s = ProductWaitinglist(userid=request.session['Customer'].contactid, catalogid=item_id ,
                                user_email = request.session['Customer'].email, record_date = datetime.datetime.now())
                s.save()
                return HttpResponse('/mywishlist?err=Item is added to your wish list')
            else:
                logging.info('count:: %s',count)
                return HttpResponse('/mywishlist?err=Item Already Exists')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponse('/mywishlist?err=Item Already Exists')

class EmailToFriendActionClass(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            s = ProductEmailfriend(catalogid=request.GET['itemid'], user_name=request.GET['name'] ,user_email = request.GET['email'],friend_email = request.GET['femails'],
                                   friend_name = request.GET['fnames'], message = request.GET['emsg'], record_date = datetime.datetime.now())
            s.save()
            return HttpResponse('<h2>Successfully Sent</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponse('<h2>Problem Occured</h2><input name="cancel" type="button" value="Close Window" class=" b-close">')

class DeleteCartItemActionClass(TemplateView):

  def get(self, request, *args, **kwargs):
    id = int(request.GET['wsh_id'])
    productid = int(request.GET['catalogid'])
    WsiWishlistitems.objects.filter(wsh_id = id, catalogid=productid).delete()
    request.session["Message"] = "Your item is successfully deleted";
    return HttpResponseRedirect('/mywishlist');

class DeleteWishListActionClass(LoginRequiredMixin,TemplateView):
    
    def get(self, request, *args, **kwargs):
        
        if "catalogid" in request.GET and request.GET['catalogid'] != "":
            try:
                logging.info('LoginfoMessage:: %s',request.GET['catalogid'])
                deletewish = ProductWaitinglist.objects.filter(catalogid=request.GET['catalogid'], userid=request.session['Customer'].contactid).delete()
                return HttpResponseRedirect('/mywishlist?page=1&err=Successfully Deleted')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/mywishlist?&err=Problem occured while deleting')
        else:
            return HttpResponseRedirect('/mywishlist?&err=Problem occured while deleting')


class GeneralActionClass(LoginRequiredMixin,TemplateView):
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
        elif "action" in request.POST and request.POST['action'] == "editcrmresponse":
            crmid = request.POST['crmid']
            try:
                s = CrmMessages(crmid = crmid, sendername = "",
                                sender = 1, message = request.POST['message'],
                                datentime = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/editrequestform?crmid='+crmid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/editrequestform?crmid='+crmid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addresponse":
            try:
                t = Crm(custid=request.session['Customer'].contactid,custemail = request.POST['custemail'] , departmentid = request.POST['departmentid'] ,
                        subject = request.POST['subject'] , customer = request.POST['customer'] ,status=1, datentime = datetime.datetime.now())
                t.save()
                obj = Crm.objects.filter(custid=request.session['Customer'].contactid).latest('id').id
                logging.info('Last Insert Id:: %s',obj)
                s = CrmMessages(crmid = obj, sendername = request.POST['customer'] ,
                                sender = 1 , message = request.POST['message'] ,
                                datentime = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/myaccount?err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/myaccount?err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addrmaresponse":
            try:
                rmaid=request.POST['rmaid']
                s = RmaMessages(rmaid = rmaid, sendername = request.session['Customer'].contactid ,
                                sender = 1 , message = request.POST['message'] ,
                                datentime = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/rmarequest?crmid='+rmaid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/rmarequest?crmid='+rmaid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addrmarequest":
            try:
                oid=request.POST['oid']
                rmaid = oid
                s = Rma(orderid = oid,idrmamethod = 1, idrmareason=1, idrmastatus=1,comments = request.POST['message'],
                                rmadate = datetime.datetime.now(), idrmaaction="0",qty_received=0,qty_restock=0)
                s.save()
                return HttpResponseRedirect('/rmaservice?crmid='+oid+'&err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/rmaservice?crmid='+rmaid+'&err=Form Field Errors')
        elif "action" in request.POST and request.POST['action'] == "addaddressbook":
            
            try:
                s = CustomersAddressbook(contactid = request.session['Customer'].contactid, shipping_firstname = request.POST['shipping_firstname'],
                                         shipping_lastname = request.POST['shipping_lastname'], shipping_city = request.POST['shipping_city'],
                                         shipping_state = request.POST['shipping_state'], shipping_zip = request.POST['shipping_zip'],
                                         shipping_country = request.POST['shipping_country'], shipping_address = request.POST['shipping_address'],
                                         shipping_address2 = request.POST['shipping_address2'], date_added = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/addressbook?err=Successfully Updated the Record')
            except Exception, e:
                logging.info('LoginfoMessage:: %s',e)
                return HttpResponseRedirect('/addressbook?&err=Form Field Errors')
        else:
            return HttpResponseRedirect('/myaccount?err=Form Field Errors')

#=============================================================================
# Murthy Code lines below
#=============================================================================

class GuestLoginActionClass(TemplateView):

    def post(self, request, *args, **kwargs):

       if 'EMail' in request.POST:
           request.session['IsGuest'] = True
           request.session['GuestEMail'] = request.POST['EMail']
           guest_email = request.POST['EMail']
           customer_list = customers.objects.filter(email = guest_email) 
           if customer_list:
             request.session['ErrorMessage2'] = "You are already a registered customer. Please login from left pane."
             return HttpResponseRedirect('/checkoutlogin');

       return HttpResponseRedirect('/orderconfirmation');

class AddToCartActionClass(TemplateView):
  
    def get(self, request, *args, **kwargs):
      html_text = ""
      item_id = 0
      cart_items = {}

      # Checking whether the item_id is available on the query string or not.
      if 'item_id' in request.GET:
        item_id = int(request.GET['item_id'])
        # Checking whether cart itmes are in the session or not
        if 'CartItems' not in request.session:
          cart_dict = {}
          request.session['CartItems'] = cart_dict
        else:
          cart_dict = request.session['CartItems']

        cart = CartInfo()
        cart_dict = cart.Add(cart_dict, item_id)
        if cart.IsError:
          html = "<font color='red'> %d " %item_id + cart.Error() +  "</font>"
          return HttpResponse(html)
        else:
          request.session['CartItems'] = cart_dict
   
      return HttpResponseRedirect("cartconfirmation?itemid=%d" %item_id)

    def post(self, request, *args, **kwargs):
      item_id = int(request.POST['item_id'])
      quantity = int(request.POST['quantity'])
      price = float(request.POST['GiftAmount'].strip())

      # Checking whether cart itmes are in the session or not
      if 'CartItems' not in request.session:
        cart_dict = {}
        request.session['CartItems'] = cart_dict
      else:
        cart_dict = request.session['CartItems']

      cart = CartInfo()
      cart_dict = cart.AddGift(cart_dict, item_id, quantity, price)

      if cart.IsError:
        html = "<font color='red'> %d " %item_id + cart.Error() +  "</font>"
        return HttpResponse(html)
      else:
        request.session['CartItems'] = cart_dict
        
      #return HttpResponse(cart_dict)
      return HttpResponseRedirect("/viewcart")
      #return HttpResponseRedirect("cartconfirmation?itemid=%d" %item_id)

class CartActionsClassolder(TemplateView):
    '''Page Name: /cartaction '''

    def get(self, request, *args, **kwargs):

      cart = CartInfo()
      cart_dict = request.session['CartItems']
      if "cmdUpdate" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        # Checking the stock availability
        #product_list = Products.objects.filter(catalogid = item_id, stock__gt = quantity)
        cart_dict = cart.Update(cart_dict, item_id, quantity)
        if cart.IsError:
          request.session['ErrorMessage'] = cart.Error()
        else:
          request.session['CartItems'] = cart_dict
          
#        if product_list:
#          cart_items = request.session["CartItems"]
#          cart_items[item_id] = quantity
#          request.session["CartItems"] = cart_items
#          logging.info("\n\n\n\n\nUpdated. %s\n\n\n\n" %str(cart_items))
#        else:
#          request.session['ErrorMessage'] = 'Requested quantity is not avaialable in the store.'
        
        #return HttpResponse(request.session["CartItems"][item_id])

      if "cmdDelete" in request.GET:
        item_id = int(request.GET['itemid'])
        #quantity = int(request.GET['quantity'])
        #cart_items = request.session["CartItems"]
        cart_dict = cart.Delete(cart_dict, item_id)
        request.session["CartItems"] = cart_dict

      if ("cmdApplyStoreCredit.x" in request.GET or
          "cmdApplyStoreCredit.y" in request.GET or
          "cmdApplyStoreCredit" in request.GET):

        tm = time.localtime()
        sc = StoreCredit()
        sc.id = int(request.GET['hdnStoreCreditID'])
        sc.credit_value = float(request.GET['hdnStoreCredit'])
        request.session['StoreCredit'] = sc
        

        #request.session['CartInfo'].is_storecredit_applied = True
        #request.session['CartInfo'].store_credit_id = int(request.GET['hdnStoreCreditID'])
        #request.session['CartInfo'].store_credit = float(request.GET['hdnStoreCredit'])
        
#         store_credit = float(request.GET['hdnStoreCredit'])
#         order_total = request.session['CartInfo'].order_total
#         credit_id = int(request.GET['hdnStoreCreditID'])
#         current_date = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday)
#         obj_list = SwfCustomerCreditsLog.objects.filter(id = credit_id)
#         obj = obj_list[0]
# 
#         if order_total >= store_credit:
#           debugText = "Order Total is greater than store credit"
#           request.session['CartInfo'].store_credit = store_credit
#           order_total = order_total - store_credit
#           obj.customers_credit = 0
#         else:
#           debugText = "Store credit is greater than Order Total"
#           obj_list = SwfCustomerCreditsLog.objects.filter(id = credit_id)
#           obj = obj_list[0]
#           request.session['CartInfo'].store_credit = order_total
#           store_credit =  store_credit - order_total
#           order_total = 0
#           obj.customers_credit = store_credit
#           debugText += "\nUpdated Store credit of %f for id %d" %(store_credit, credit_id)
# 
#           
#         request.session['CartInfo'].order_total  = order_total
#         obj.customers_credit_applied = current_date
#         request.session["StoreCreditObject"] = obj
            
      if "cmdApplyCoupon" in request.GET:
        tm = time.localtime()
        current_date = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday)
        
        coupon_code = request.GET['txtCoupon'].strip()
        promotion_list = Promotions.objects.filter(promotion_enabled = 1, coupon = coupon_code, promotion_start__lte = current_date, promotion_end__gte = current_date)
                                                   
        if promotion_list:
          if 'PromotionalDiscount' in request.session:
              discounts_hash = request.session['PromotionalDiscount']
          else:
              discounts_hash = {}

          for promotion in promotion_list:
            product_id = promotion.promotion_product
            if product_id:
              discounts_hash[product_id] = promotion.promotion_amount
            else:
              discounts_hash[-1] = promotion.promotion_amount

          request.session['CouponCode'] = coupon_code
          request.session['PromotionalDiscount'] = discounts_hash
        else:
          request.session['ErrorMessage'] = 'Coupon Not found'

      return HttpResponseRedirect('viewcart')
      #return HttpResponse(request.GET)

class CartActionsClass(TemplateView):
    '''Page Name: /cartaction '''

    def get(self, request, *args, **kwargs):

      cart = CartInfo()
      cart_dict = request.session['CartItems']
      if "cmdUpdate" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        # Checking the stock availability
        #product_list = Products.objects.filter(catalogid = item_id, stock__gt = quantity)
        cart_dict = cart.Update(cart_dict, item_id, quantity)
        if cart.IsError:
          request.session['ErrorMessage'] = cart.Error()
        else:
          request.session['CartItems'] = cart_dict
          
#        if product_list:
#          cart_items = request.session["CartItems"]
#          cart_items[item_id] = quantity
#          request.session["CartItems"] = cart_items
#          logging.info("\n\n\n\n\nUpdated. %s\n\n\n\n" %str(cart_items))
#        else:
#          request.session['ErrorMessage'] = 'Requested quantity is not avaialable in the store.'
        
        #return HttpResponse(request.session["CartItems"][item_id])

      if "cmdDelete" in request.GET:
        item_id = int(request.GET['itemid'])
        #quantity = int(request.GET['quantity'])
        #cart_items = request.session["CartItems"]
        cart_dict = cart.Delete(cart_dict, item_id)
        request.session["CartItems"] = cart_dict

      if ("cmdApplyStoreCredit.x" in request.GET or
          "cmdApplyStoreCredit.y" in request.GET or
          "cmdApplyStoreCredit" in request.GET):

        tm = time.localtime()
        sc = StoreCredit()
        sc.id = int(request.GET['hdnStoreCreditID'])
        sc.credit_value = float(request.GET['hdnStoreCredit'])
        request.session['StoreCredit'] = sc
        

        #request.session['CartInfo'].is_storecredit_applied = True
        #request.session['CartInfo'].store_credit_id = int(request.GET['hdnStoreCreditID'])
        #request.session['CartInfo'].store_credit = float(request.GET['hdnStoreCredit'])
        
#         store_credit = float(request.GET['hdnStoreCredit'])
#         order_total = request.session['CartInfo'].order_total
#         credit_id = int(request.GET['hdnStoreCreditID'])
#         current_date = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday)
#         obj_list = SwfCustomerCreditsLog.objects.filter(id = credit_id)
#         obj = obj_list[0]
# 
#         if order_total >= store_credit:
#           debugText = "Order Total is greater than store credit"
#           request.session['CartInfo'].store_credit = store_credit
#           order_total = order_total - store_credit
#           obj.customers_credit = 0
#         else:
#           debugText = "Store credit is greater than Order Total"
#           obj_list = SwfCustomerCreditsLog.objects.filter(id = credit_id)
#           obj = obj_list[0]
#           request.session['CartInfo'].store_credit = order_total
#           store_credit =  store_credit - order_total
#           order_total = 0
#           obj.customers_credit = store_credit
#           debugText += "\nUpdated Store credit of %f for id %d" %(store_credit, credit_id)
# 
#           
#         request.session['CartInfo'].order_total  = order_total
#         obj.customers_credit_applied = current_date
#         request.session["StoreCreditObject"] = obj
            
      if "cmdApplyCoupon" in request.GET:
        tm = time.localtime()
        current_date = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday)
        
        coupon_code = request.GET['txtCoupon'].strip()
        promotion_list = Promotions.objects.filter(promotion_enabled = 1, coupon = coupon_code, promotion_start__lte = current_date, promotion_end__gte = current_date)
                                                   
        if promotion_list:
          if 'PromotionalDiscount' in request.session:
              discounts_hash = request.session['PromotionalDiscount']
          else:
              discounts_hash = {}

          if len(promotion_list) > 1:
            for promotion in promotion_list:
              product_id = promotion.promotion_product
              if product_id:
                discounts_hash[('PromotionalDiscount', 'ProductID', product_id)] = promotion.promotion_amount
          else:
            promotion = promotion_list[0]
            if promotion.by_category:
              product_cat_list = promotion.by_category.split(',')
              if promotion.promotion_freeshipping == 1:
                for cat_id in product_cat_list:
                  if cat_id:  
                    discounts_hash[('FreeShipping', 'ProductCategory', int(cat_id))] = 0
          
          request.session['CouponCode'] = coupon_code
          request.session['PromotionalDiscount'] = discounts_hash
        else:
          request.session['ErrorMessage'] = 'Coupon Not found or expired.'

      return HttpResponseRedirect('viewcart')
      #return HttpResponse(request.GET)

class PaypalStatusActionClass(TemplateView):

   def get(self, request, *args, **kwargs):
     post_str = ""
     for key, value in request.POST.items():
       post_str += "%s=%s<br>" %(key, value)

     return HttpResponse(post_str)


class UpdateAddressInSession(TemplateView):

  def get(self, request, *args, **kwargs):
    logging.info('\n\nEntered into Updating Address\n\n')
    content = {}
    form = AddressForm(request.GET)

    if form.is_valid():
      address_type = form.cleaned_data['address_type'].strip()
    else:
      logging.info(form.errors)
      logging.info('\n\nForm is not valid\n\n')


    if 'IsLogin' not in request.session or not request.session['IsLogin']:
        logging.info('\n\nUser is Not logged in\n\n')
        # This block will be executed when Gust user is submitted shipping address in
        # order confirmation page.
        customer = customers()
        customer.contactid = -1    
        if address_type == "billing":
          logging.info('\n\n   Updating Billing Address in session\n\n')
          customer.billing_firstname = form.cleaned_data['first_name'].strip()
          customer.billing_lastname = form.cleaned_data['last_name'].strip()
          customer.billing_address = form.cleaned_data['address1'].strip()
          customer.billing_address2 = form.cleaned_data['address2'].strip()
          customer.billing_city = form.cleaned_data['city'].strip()
          customer.billing_state = form.cleaned_data['state'].strip()
          customer.billing_country = form.cleaned_data['country'].strip()
          customer.billing_zip = form.cleaned_data['zip'].strip()
          customer.billing_company = form.cleaned_data['company'].strip()
          customer.billing_phone = form.cleaned_data['phone'].strip()
          request.session['Customer'] = customer
          html = "<h4>Billing Address is updated in session</h4>"
        elif address_type == "shipping":
          logging.info('\n\n   Updating Shipping Address in session\n\n')
          customer.shipping_firstname = form.cleaned_data['first_name'].strip()
          customer.shipping_lastname = form.cleaned_data['last_name'].strip()
          customer.shipping_address = form.cleaned_data['address1'].strip()
          customer.shipping_address2 = form.cleaned_data['address2'].strip()
          customer.shipping_city = form.cleaned_data['city'].strip()
          customer.shipping_state = form.cleaned_data['state'].strip()
          customer.shipping_country = form.cleaned_data['country'].strip()
          customer.shipping_zip = form.cleaned_data['zip'].strip()
          customer.shipping_company = form.cleaned_data['company'].strip()
          customer.shipping_phone = form.cleaned_data['phone'].strip()
          logging.info("\n\n\nFirst Name: %s" %customer.shipping_firstname)
          request.session['Customer'] = customer
         
          html = "<h4>Shipping Address is updated in session</h4>"
        
    return HttpResponseRedirect("/orderconfirmation")
        

class CommitOrderActionClass(TemplateView):

  def post(self, request, *args, **kwargs):
    logging.info('\n\nEntered into Commit Order Page')
    content = {}

    is_login = False;
    is_guest = False;
    is_save_card = False;
    gateway = ''
    #if form.is_valid():
    #  return HttpResponse("Form is Valid")
    #else:
    #  return HttpResponse("Form is not Valid")

    if 'IsLogin' in request.session:
      if request.session['IsLogin']:
        is_login = True;
        is_guest = False;

    if 'IsGuest' in request.session:
      if request.session['IsGuest'] and not is_login:
        is_guest = True;
        
    # If there is no login and no guest, then redirect to checkoutlogin page.
    if not is_login and not is_guest:
      return HttpResponseRedirect('/checkoutlogin')
        
    if 'gateway' in request.GET:
      request.session['PaymentGateway'] = request.GET['gateway']
      gateway = request.GET['gateway']
      
    if 'PaymentGateway' in request.session:
      gateway = request.session['PaymentGateway']

    data = request.POST 
    if is_login:
      if gateway == 'paypal':
        form = PaypalOrderFormLoggedIn(data)
      elif gateway == 'AUTHORIZENET':
        customer = request.session['Customer']
        form = AuthorizeNetFormLoggedIn(data, card_list = GetCreditCardList(customer.contactid))
      elif gateway == 'None':
        form = NoGateWay(data)
    elif is_guest:
      if gateway == 'paypal':
        form = PaypalOrderFormNoLogin(data, card_list = [])
      elif gateway == 'AUTHORIZENET':
        form = AuthorizeNetFormNoLogin(data, card_list = [])
      customer = None   
    
    if form.is_valid():
      # If gust, we should save the customer information with login credentials and then continue.
      if is_login: 
        customer = request.session['Customer']        
      elif is_guest:
        customer = customers()
        customer.email = form.cleaned_data['username'].strip()
        customer.pass_field = form.cleaned_data['password'].strip()

      customer.shipping_firstname = form.cleaned_data['shipping_first_name'].strip()
      customer.shipping_lastname = form.cleaned_data['shipping_last_name'].strip()
      customer.shipping_address = form.cleaned_data['shipping_address1'].strip()
      customer.shipping_address2 = form.cleaned_data['shipping_address2'].strip()
      customer.shipping_city = form.cleaned_data['shipping_city'].strip()
      customer.shipping_state = form.cleaned_data['shipping_state'].strip()
      customer.shipping_zip = form.cleaned_data['shipping_zip'].strip()
      customer.shipping_company = form.cleaned_data['shipping_company'].strip()
      phone_part1 = form.cleaned_data['shipping_phone_part1'].strip()
      phone_part2 = form.cleaned_data['shipping_phone_part2'].strip()
      phone_part3 = form.cleaned_data['shipping_phone_part3'].strip()
      customer.shipping_phone = phone_part1 + phone_part2 + phone_part3
      
      isBillingAddressSame = False
      if "IsBillingAddressSame" in request.POST:
         isBillingAddressSame = True

      if isBillingAddressSame:
        customer.billing_firstname = customer.shipping_firstname
        customer.billing_lastname = customer.shipping_lastname
        customer.billing_address = customer.shipping_address
        customer.billing_address2 = customer.shipping_address2
        customer.billing_city = customer.shipping_city
        customer.billing_state = customer.shipping_state
        customer.billing_zip = customer.shipping_zip
        customer.billing_phone = customer.shipping_phone
      else:
        customer.billing_firstname = form.cleaned_data['billing_first_name'].strip()
        customer.billing_lastname = form.cleaned_data['billing_last_name'].strip()
        customer.billing_address = form.cleaned_data['billing_address1'].strip()
        customer.billing_address2 = form.cleaned_data['billing_address2'].strip()
        customer.billing_city = form.cleaned_data['billing_city'].strip()
        customer.billing_state = form.cleaned_data['billing_state'].strip()
        customer.billing_zip = form.cleaned_data['billing_zip'].strip()
        phone_part1 = form.cleaned_data['billing_phone_part1'].strip()
        phone_part2 = form.cleaned_data['billing_phone_part2'].strip()
        phone_part3 = form.cleaned_data['billing_phone_part3'].strip()
        customer.billing_phone = phone_part1 + phone_part2 + phone_part3

      customer.custenabled = 1
      customer.save() 
        

      shipping_method_hash = request.session['ShippingMethod']

      cart = request.session['CartInfo']

      #html = ""
      #for key, value in request.POST.items():
      #  html += "%s -> %s<br>" %(key, value)
 
      # Collecting User Selected Data in Shipping Methods
      data_hash = {}
      for key, vaue in shipping_method_hash.items():
        if 'OverNightShipping%d' %key  in request.POST:
          data_hash['OverNightShipping'] = request.POST['OverNightShipping%d' %key]
          overnight_shipping_value = GetPriorityShippingCharge(key)
          cart.order_total += overnight_shipping_value
          data_hash['Over Night Shipping'] = overnight_shipping_value
            
        if 'HoldPackageAtFedex%d' %key in request.POST:
          data_hash['HoldPackageAtFedex'] = request.POST['HoldPackageAtFedex%d' %key]

        if 'FedexLocationCode%d' %key in request.POST:
          data_hash['Fedex Location Code'] = request.POST['FedexLocationCode%d' %key]

        if 'ReqDeliveryDate%d' %key in request.POST:
          data_hash['Requested Delivery Date'] = request.POST['ReqDeliveryDate%d' %key]
          if len(data_hash['ReqDeliveryDate'].strip()) > 0:
            if time.strptime(data_hash['Requested Delivery Date'], "%m/%d/%Y").tm_wday == 5:
              sat_delivery_value = GetSaturdayShippingCharge(key)
              data_hash['Saturday Delivery'] = sat_delivery_value
              cart.order_total += sat_delivery_value 

        shipping_method_hash[key] = data_hash
      
      #for key, value in shipping_method_hash.items():
      #  html += "%s -> %s<br>" %(key, value)
        
      #html += "<br><b>" + str(cart.order_total) + "</b>" 

      #return HttpResponse(html)
    
      request.session['CartInfo'] = cart
      request.session['ShippingMethod'] = shipping_method_hash 
      request.session['OrderComment'] = form.cleaned_data['comment'].strip()
     
      if is_guest:
        customer = customers.objects.all().latest('contactid')
        request.session['Customer'] = customer
        request.session['IsLogin'] = True
        del request.session['GuestEMail']
        is_login = True
        is_guest = False

      if is_login and gateway == 'AUTHORIZENET':
        previous_card = form.cleaned_data['previous_cards']
        if not previous_card: 
          card_holder_name = form.cleaned_data['card_holder_name'].strip()
          card_number = form.cleaned_data['card_number'].strip()
          card_type = form.cleaned_data['card_type'].strip()
          card_expdate = form.cleaned_data['card_expdate'].strip()
          card_cvn = form.cleaned_data['card_cvn'].strip()
          is_save_card = form.cleaned_data['is_save_card']
                  
          # Authenticating Card Number
          card = CreditCard(
              number = card_number,
              month = card_expdate.split('/')[0],
              year = '20%s' %card_expdate.split('/')[1],
              first_name = card_holder_name.split(' ')[0],
              last_name = card_holder_name.split(' ')[1],
              code = card_cvn
          )
        else:
          is_save_card = False
          orders = Orders.objects.all().filter(ocardno = previous_card)[0]
          number = orders.ocardno
          month = orders.ocardexpiresmonth
          year = orders.ocardexpiresyear
          first_name = orders.ocardname.split(' ')[0]
          last_name = orders.ocardname.split(' ')[1]
          code = orders.ocardverification        
          card = CreditCard(
              number = orders.ocardno,
              month = orders.ocardexpiresmonth,
              year = orders.ocardexpiresyear,
              first_name = orders.ocardname.split(' ')[0],
              last_name = orders.ocardname.split(' ')[1],
              code = orders.ocardverification
          )

        gateway = AimGateway(settings.AUTHORIZENET_API_LOGIN_ID, settings.AUTHORIZENET_API_PASSWORD)
        gateway.use_test_mode = settings.TEST_MODE
        gateway.use_test_url = settings.TEST_MODE_URL
        response = gateway.authorize(1, card)
        #return HttpResponse("<h1>Done</h1>")
        
        if response.status_strings[response.status] == "Approved":
          response = gateway.sale("%8.2f" %cart.order_total, card)
          if response.status_strings[response.status] == "Approved":
            if is_save_card:
              # This will trigger the save credit card option in Call Back Code.
              request.session['CreditCard'] = card.__dict__
            return HttpResponseRedirect(settings.CALLBACK_URL + '?tx=%s&st=Approved&amt=%s&cc=USD&item_number=' %(response.trans_id,
                                                                                                                  "%8.2f" %request.session['CartInfo'].order_total))
          else:
            request.session['ErrorMessage'] =  "<h5>%s - %s: %s</h5>" %(response.trans_id, response.status_strings[response.status], response.message)
        else:
          request.session['ErrorMessage'] =  "%s - %s: %s" %(response.trans_id, response.status_strings[response.status], response.message)
        return HttpResponseRedirect('/orderconfirmation')    

      elif is_login and gateway == 'paypal':
          return  HttpResponseRedirect('/paypalredirection')  
      elif is_login and gateway == 'None':
          #obj = request.session["StoreCredit"]
          #obj.save()
          tx = "SC%s" %datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
          amount = request.session["CartInfo"].store_credit
          return HttpResponseRedirect(settings.CALLBACK_URL + '?tx=%s&st=Approved&amt=%s&cc=USD&item_number=' %(tx, amount))

    else:
      html = ""
      for key, value in form.errors.items():
        html += "%s, " %(key)
      
      html = html[0:-2]
      request.session['ErrorMessage'] = 'Please fill mandatory fields. %s' %html
    return HttpResponseRedirect('/orderconfirmation')


class AddReefPackagesActionClass(TemplateView):
  '''Page Name: Reef Packages'''
  def post(self, request, *args, **kwargs):
    html = "Hi<br>"
    item_count = len(request.POST)
    #for key, value in   

    if 'CartItems' not in request.session:
      cart_dict = {}
      request.session['CartItems'] = cart_dict
    else:
      cart_dict = request.session['CartItems']

    for i in range(1, item_count):
      if "quantity%d" %i in request.POST:
        #html += "%s -  %s<br>" %(request.POST["catalogid%s" %i], request.POST["quantity%s" %i])
        quantity = request.POST["quantity%s" %i]
        if quantity:
          item_id = int(request.POST["catalogid%s" %i])
          quantity = int(quantity)
          #html += "%s - %s<br>" %(item_id, quantity)
          cart = CartInfo()
          cart_dict = cart.AddReef(cart_dict, item_id, quantity)

    request.session['CartItems'] = cart_dict
    return HttpResponseRedirect("/viewcart")
