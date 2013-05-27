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
from views import LoginRequiredMixin
from models import *
from google.appengine.api import mail
import logging, random, hashlib, datetime
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

class RegistrationActionClass(TemplateView):
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
      return render_to_response('registration.htm', content)

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
class AddToWatchActionClass(LoginRequiredMixin,TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            item_id = int(request.GET['itemid'])
            t = ProductWaitinglist.objects.filter(catalogid=item_id, userid=request.session['Customer'].contactid)
            count = t.count()
            if count <= 0:
                logging.info('count:: %s',count)
                s = ProductWaitinglist(userid=request.session['Customer'].contactid, catalogid=item_id ,
                                user_email = request.session['Customer'].email, record_date = datetime.datetime.now())
                s.save()
                return HttpResponseRedirect('/mywishlist?err=Item is added to your wish list')
            else:
                logging.info('count:: %s',count)
                return HttpResponseRedirect('/mywishlist?err=Item Already Exists')
        except Exception, e:
            logging.info('LoginfoMessage:: %s',e)
            return HttpResponseRedirect('/mywishlist?err=Item Already Exists')


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
        if "CartItems" in request.session:
          cart_items = request.session["CartItems"]
          # If item is already added to the cart, incrementing the quantity
          # to the partiuclar item. Else assigning initial quantity as 1.
          if item_id in cart_items:
            cart_items[item_id] += 1
          else:
            cart_items[item_id] = 1
          request.session["CartItems"] = cart_items
        else:
          cart_items = {item_id:1}
          request.session["CartItems"] = cart_items
        
      cart_items = request.session["CartItems"]
      #for key, value in cart_items.items():
      #  html_text += "%d - %d<br>\n" %(key, value)
        
      return HttpResponseRedirect("cartconfirmation?itemid=%d" %item_id)

class CartActionsClass(TemplateView):

    def get(self, request, *args, **kwargs):

      if "cmdUpdate" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        cart_items = request.session["CartItems"]
        cart_items[item_id] = quantity
        request.session["CartItems"] = cart_items
        logging.info("\n\n\n\n\nUpdated. %s\n\n\n\n" %str(cart_items))
        
        #return HttpResponse(request.session["CartItems"][item_id])

      if "cmdDelete" in request.GET:
        item_id = int(request.GET['itemid'])
        quantity = int(request.GET['quantity'])
        cart_items = request.session["CartItems"]
        del cart_items[item_id]
        request.session["CartItems"] = cart_items

      return HttpResponseRedirect('viewcart')
