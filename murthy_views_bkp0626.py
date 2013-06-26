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
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import unittest
from forms import *
from models import *
from django.db.models import Count, Min, Sum, Max, Avg
from django.db import connection
import random, logging
import functools
from functools import wraps
from django.core.context_processors import csrf
from classes import *
from views import *
from django.db.models import Max

import time
import calendar

PERPAGE=50
class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s"%value

def checkuserlogin_dispatch(f):
    def wrap(request, *args, **kwargs):
        if 'IsLogin' in request.session and request.session['IsLogin'] and request.session['Customer'].email !="":
            customer_list = customers.objects.filter(email = request.session['Customer'].email,
                                                     pass_field = request.session['Customer'].pass_field,custenabled=1)
            if customer_list:
                request.session['IsLogin'] = True
                request.session['Customer'] = customer_list[0]
                success = True
            else:
                return HttpResponseRedirect('/logout')
            logging.info('Fetch Started::  %s', customer_list[0])
        else:
            return HttpResponseRedirect('/logout')
        return f(request, *args, **kwargs)
    return wrap


class LoginRequiredMixin(object):
    @method_decorator(checkuserlogin_dispatch)
    def dispatch(self,request, *args, **kwargs):
        #logging.info('Fetch Started::  %s', request.session['Customer'].email)
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

class CartConfirmClass(TemplateView):

  def get(self, request, *args, **kwargs):
    item_id = 0
    content = {}
    if "itemid" in request.GET:
      item_id = int(request.GET['itemid'])
    #product_category = ProductCategory.objects.all().filter(catalogid=request.GET['itemid'])
    #pcats =""
    #for pwcats in product_category:
    #    pcats += str(pwcats.categoryid)+", "
    #pcats = pcats[:-2]+''
    #logging.info('categoryid:: %s',pcats)
    #relateditems=Products.objects.raw('select * from product_category,products where products.catalogid!='+request.GET['itemid']+' and product_category.catalogid=products.catalogid and hide=0 and categoryid in ('+pcats+')')[:8]

    #del request.session['CartItems']
    if 'CartItems' in request.session:
      cart_dict = request.session['CartItems']
    cart_item = cart_dict[item_id]
    item_count = 0
    sub_total = 0
    html = "<h3>"
    for key, item in cart_dict.items():
      html += "%s =>" %key + str(item.quantity) + "<br>"
      item_count += item.quantity
      item.CalculateTotals()
      sub_total += item.subtotal

    #return HttpResponse(html)
#    item = Products.objects.filter(catalogid=item_id)[0]
#    if item.stock == 0:
#       # If quantity is out of stock, removing the item from the cart.
#       cart_items = request.session["CartItems"]
#       if cart_items: del cart_items[item_id]
#       request.session["CartItems"] = cart_items
#       return HttpResponse("<h3>Quantity is out of stock. Click <a href='productlist'>here</a> to continue shopping.</h3>")
#    else:
#      cart_items = request.session["CartItems"]
#      cart_items[item_id] += 1
#    
#    #cart_item = CartItems(item.catalogid, item.name, item.price,
#    #                      item.saleprice, 1, 0.0, 0.0, 0.0, 0.0, item.thumbnail,
#    #                      item.image1, item.image2, item.image3)
#    
#    cart_item = CartItem(item_id)
#    
#
#
#    # Calculating Sum for all the items.
#    if 'CartItems' in request.session:
#      cart_items = request.session["CartItems"]
#      item_count = 0
#      sub_total = 0
#      shipping_total = 0
#      fuelcharge_total = 0
#      tax_total = 0
#      promotions_total = 0
#      order_total = 0
#      
#      for key, qty in cart_items.items():
#        item_count += qty
##       sub_total += (cart_item.subtotal * qty)
##       shipping_total += (cart_item.shipping * qty)
##       tax_total += (cart_item.taxvalue * qty)
##       fuelcharge_total += (cart_item.fuelcharge * qty)
##       promotions_total += (cart_item.promotions * qty)
#    
#      #order_total = float(sub_total) + float(shipping_total) + float(fuelcharge_total) + float(tax_total) - float(promotions_total)
#    else:
#      content['ItemsHash'] = {}

    content['ItemCount'] = item_count
    content['OrderSubTotal'] = sub_total
    content['item'] = cart_item
    content['relateditems'] = relatedproditems(request.GET['itemid'],8)
    content.update(leftwidget(request))
    return render_template(request,'CartConfirmation.html', content)

from random import choice
class ViewCartViewClass(TemplateView):
  #Page Url: /viewcart
  #Last Modified: 2013-15-19 23:30

  def GetPromotionValue(self, session, item_id):
    if 'PromotionalDiscount' in session:
      discounts_hash = session['PromotionalDiscount']
      if item_id in discounts_hash:
          return discounts_hash[item_id]
      else:
          return 0
    else:
      return 0

  def get(self, request, *args, **kwargs):
    store_credit_id = 0 # Unique id of swf customer credits table
    store_credits = 0

    content = {}
    content = {'page_title': "My Cart"}
    
    next_page = "checkoutlogin"

    # Checking Store Credits
    if "Customer" in request.session:
      next_page = 'orderconfirmation'
      customer = request.session['Customer']    
      swf_custcredits_objects = SwfCustomerCreditsLog.objects.filter(customers_email_address = customer.email)
      if swf_custcredits_objects:
        store_credit_id = swf_custcredits_objects[0].id
        store_credits = swf_custcredits_objects[0].customers_credit
        
    cart_dict = {}
    if 'CartItems' in request.session:
      cart_dict = request.session['CartItems']

    # Cleaning up sessions when if cart is empty.
    if not cart_dict:
      if 'CartInfo' in request.session:
        del request.session['CartInfo']

      if 'StoreCredit' in request.session:
        del request.session['StoreCredit']

      if 'PaymentGateway' in request.session:
        del request.session['PaymentGateway']


    cart = CartInfo()
    shipping_items = cart.GetItemsByShippingCategory(cart_dict)

    shipping_method_hash = {}
    
    #if 'ShippingMethod' not in request.session:
    for item in shipping_items:
      if item.id not in shipping_method_hash:
        sc = ShippingCategory.objects.filter(id = item.id)[0]
        shipping_method_hash[item.id] = sc 

    request.session['ShippingMethod'] = shipping_method_hash

    if "StoreCredit" in request.session:
      sc = request.session['StoreCredit']
      cart.ApplyStoreCredit(sc)
      store_credits = cart.store_credit
    else:
      cart.store_credit = store_credits 


    request.session['CartInfo'] = cart
    
    content['MyCartItems'] =  shipping_items
    content['CartInfo'] = cart
    foo = ['3878', '3846', '2447', '2348', '1797']
    product_category = ProductCategory.objects.all().filter(catalogid=choice(foo))
    pcats =""
    for pwcats in product_category:
        pcats += str(pwcats.categoryid)+", "
    pcats = pcats[:-2]+''
    logging.info('categoryid:: %s',pcats)
    relateditems=Products.objects.raw('select * from product_category,products where products.catalogid!=3878 and product_category.catalogid=products.catalogid and hide=0 and categoryid in ('+pcats+')')[:3]
    content['NextPage'] = next_page
    content['relateditems'] = relateditems
    content['StoreCreditID'] = store_credit_id
    content['StoreCredit'] = store_credits
    content.update(csrf(request))
    content.update(leftwidget(request))
    logging.info('field name:: %s',cart_dict)
    return render_template(request,'ViewCart.html', content)


class ForgetPasswordClass(LoginRequiredMixin,TemplateView):

    @csrf_exempt
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value

    @csrf_exempt
    def post(self, request, *args, **kwargs):
      content = {'page_title': "Customer Forget Password"}
      form = ForgetPwdForm(request.POST)
      if form.is_valid():
          if form.cleaned_data['recaptcha'] == str(request.session['ReCaptcha']):
            customer_list = customers.objects.filter(email = form.cleaned_data['email'])
            if customer_list:
              customer = customer_list[0]
              success = True
             
              mail_body = 'Your password is %s' %customer.pass_field              
              mail.send_mail(sender="support@saltwaterfish.com",
              to=customer.email,
              subject="Saltwaterfish.com: Password request", body=mail_body)

            else:
              (success, error_msg) = (False, "Email-id is not found in our records.")
          else:
            (success, error_msg) = (False, "Human verification is failed.")
      else:
        (success, error_msg) = (False, "Incomplete or invalid form data")

      if  success:
        content = {'form': form, 'page_title': "Customer Forget Password"}
        content['recaptcha'] = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
        content['message'] = "Password has been sent to your EMail. Please check your inbox"
        content.update(csrf(request))
        return render_template(request,'login.htm', content)
      else:
        c = {'form': form, 'error_message': error_msg}


      c['recaptcha'] = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
      c.update(csrf(request))
      return render_to_response('login.htm', c)

class OrderConfirmationViewolder(TemplateView):

  @csrf_exempt
  def get(self, request, *args, **kwargs):
    data = {}
    content = {'page_title': "Order Confirmation"}
    is_login = False;
    is_guest = False;
    gateway = ''
    error_message = ''
    # Adding 3 days to the current date
    est_delivery_date = time.strftime("%m/%d/%Y", time.localtime(time.time() + 172800))
    
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
      del request.session['ErrorMessage']

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

    cart_items = request.session['CartItems']
    cart_info = request.session['CartInfo'] # Holds grand totals
    
    item_list = []
    
    for key, value in cart_items.items():
      item_list.append(value) 

    data = {}
    # Populating Customer Information if user is logged in.
    if is_login or 'Customer' in request.session:
      logging.info("Logged in or Customer info is found in the session")
      customer = request.session['Customer']
      data = {'contact_id':customer.contactid,
          'shipping_first_name':customer.shipping_firstname,
          'shipping_last_name':customer.shipping_lastname,
          'shipping_address1':customer.shipping_address,
          'shipping_address2':customer.shipping_address2,
          'shipping_city': customer.shipping_city,
          'shipping_state': customer.shipping_state,
          'shipping_zip': customer.shipping_zip,
          'shipping_country': customer.shipping_country,
          'shipping_company': customer.shipping_company,
          'shipping_phone_part1': customer.shipping_phone[0:3],
          'shipping_phone_part2': customer.shipping_phone[3:6],
          'shipping_phone_part3': customer.shipping_phone[6:],

          'billing_first_name':customer.billing_firstname,
          'billing_last_name':customer.billing_lastname,
          'billing_address1':customer.billing_address,
          'billing_address2':customer.billing_address2,
          'billing_city': customer.billing_city,
          'billing_state': customer.billing_state,
          'billing_zip': customer.billing_zip,
          'billing_country': customer.billing_country,
          'billing_company': customer.billing_company,
          'billing_phone_part1': customer.billing_phone[0:3],
          'billing_phone_part2': customer.billing_phone[3:6],
          'billing_phone_part3': customer.billing_phone[6:],
          #'billing_phone_ext': customer.billing_phone          

          }
      
      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)
    else:
      logging.info("Non Login traverse or No customer information in the session")
      data = {'contact_id':0,
          'username': request.session['GuestEMail']
          }

      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)

    if is_login:
      if gateway == 'paypal':
        form = PaypalOrderFormLoggedIn(initial=data)
      elif gateway == 'AUTHORIZENET':
        #address_form = BillingShippingAddressForm(initial=data, bstate='FL', shpstate='FL')              
        #form = AuthorizeNetFormLoggedIn(data, card_list = GetCreditCardList(customer.contactid))
        #form = AuthorizeNetFormLoggedIn(initial = data, 
        #                                card_list = GetCreditCardList(customer.contactid), 
        #                                bstate=customer.billing_state, 
                                        #bcountry='UK', 
        #                                shpstate=customer.shipping_state)
        form = AuthorizeNetFormLoggedIn(initial = data, card_list = GetCreditCardList(customer.contactid))
      else:
        form = NoGateWay(data)  

    elif is_guest:
      if gateway == 'paypal':
        form = PaypalOrderFormNoLogin(initial = data, card_list = [])
      elif gateway == 'AUTHORIZENET':
        form = AuthorizeNetFormNoLogin(initial = data, card_list = [])
        #form.fields['previous_cards'].choices = [('1', 'Account Ending in xxx - xxx - 2003'), ('2', 'Account Ending in xxx - xxx - 1099')]
      else:
        form = NoGateWay()

    index = 1
    shipping_method_list = []
    # Creating Linked List
    num_cats = len(request.session["ShippingMethod"])
    for key, value in request.session["ShippingMethod"].items():
      if num_cats > 1 and index <> num_cats: 
        shipping_method_list.append((index, value, index + 1))
      elif index == num_cats:
        shipping_method_list.append((index, value, 0))
      
      index += 1
        
      #  shipping_method_list.append((index, value, 0))
      #else:
      #  shipping_method_list.append((index, value, index + 1))
      #index+=1
      
 

    content['order_error_message'] = error_message
    #content['address_form'] = address_form
    content['form'] = form
    content['Items'] = item_list
    content['DeliveryDate'] = est_delivery_date
    content['ShippingMethodList'] = shipping_method_list
    content['cal'] = GenerateShippingCalander()
    content['Settings'] = settings
    
    content.update(csrf(request))
    content.update(leftwidget(request))
    return render_template(request,'OrderConfirmation.html', content)

class OrderConfirmationView(TemplateView):

  @csrf_exempt
  def get(self, request, *args, **kwargs):
    data = {}
    content = {'page_title': "Order Confirmation"}
    is_login = False;
    is_guest = False;
    gateway = ''
    error_message = ''
    # Adding 3 days to the current date
    est_delivery_date = time.strftime("%m/%d/%Y", time.localtime(time.time() + 172800))
    
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
      del request.session['ErrorMessage']

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

    cart_items = request.session['CartItems']
    cart_info = request.session['CartInfo'] # Holds grand totals
    
    item_list = []
    
    for key, value in cart_items.items():
      item_list.append(value) 

    data = {}
    # Populating Customer Information if user is logged in.
    if is_login or 'Customer' in request.session:
      logging.info("Logged in or Customer info is found in the session")
      customer = request.session['Customer']
      data = {'contact_id':customer.contactid,
          'shipping_first_name':customer.shipping_firstname,
          'shipping_last_name':customer.shipping_lastname,
          'shipping_address1':customer.shipping_address,
          'shipping_address2':customer.shipping_address2,
          'shipping_city': customer.shipping_city,
          'shipping_state': customer.shipping_state,
          'shipping_zip': customer.shipping_zip,
          'shipping_country': customer.shipping_country,
          'shipping_company': customer.shipping_company,
          'shipping_phone_part1': customer.shipping_phone[0:3],
          'shipping_phone_part2': customer.shipping_phone[3:6],
          'shipping_phone_part3': customer.shipping_phone[6:],

          'billing_first_name':customer.billing_firstname,
          'billing_last_name':customer.billing_lastname,
          'billing_address1':customer.billing_address,
          'billing_address2':customer.billing_address2,
          'billing_city': customer.billing_city,
          'billing_state': customer.billing_state,
          'billing_zip': customer.billing_zip,
          'billing_country': customer.billing_country,
          'billing_company': customer.billing_company,
          'billing_phone_part1': customer.billing_phone[0:3],
          'billing_phone_part2': customer.billing_phone[3:6],
          'billing_phone_part3': customer.billing_phone[6:],
          #'billing_phone_ext': customer.billing_phone          

          }
      
      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)
    else:
      logging.info("Non Login traverse or No customer information in the session")
      data = {'contact_id':0,
          'username': request.session['GuestEMail']
          }

      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)

    if is_login:
      if gateway == 'paypal':
        form = PaypalOrderFormLoggedIn(initial=data)
      elif gateway == 'AUTHORIZENET':
        #address_form = BillingShippingAddressForm(initial=data, bstate='FL', shpstate='FL')              
        #form = AuthorizeNetFormLoggedIn(data, card_list = GetCreditCardList(customer.contactid))
        #form = AuthorizeNetFormLoggedIn(initial = data, 
        #                                card_list = GetCreditCardList(customer.contactid), 
        #                                bstate=customer.billing_state, 
                                        #bcountry='UK', 
        #                                shpstate=customer.shipping_state)
        form = AuthorizeNetFormLoggedIn(initial = data, card_list = GetCreditCardList(customer.contactid))
      else:
        form = NoGateWay(data)  

    elif is_guest:
      if gateway == 'paypal':
        form = PaypalOrderFormNoLogin(initial = data, card_list = [])
      elif gateway == 'AUTHORIZENET':
        form = AuthorizeNetFormNoLogin(initial = data, card_list = [])
        #form.fields['previous_cards'].choices = [('1', 'Account Ending in xxx - xxx - 2003'), ('2', 'Account Ending in xxx - xxx - 1099')]
      else:
        form = NoGateWay()

    index = 1
    shipping_method_list = []
    # Creating Linked List
    num_cats = len(request.session["ShippingMethod"])
    for key, value in request.session["ShippingMethod"].items():
      if num_cats > 1 and index <> num_cats: 
        shipping_method_list.append((index, value, index + 1, key))
      elif index == num_cats:
        shipping_method_list.append((index, value, 0, key))
      
      index += 1
        
      #  shipping_method_list.append((index, value, 0))
      #else:
      #  shipping_method_list.append((index, value, index + 1))
      #index+=1
      
 

    content['order_error_message'] = error_message
    #content['address_form'] = address_form
    content['form'] = form
    content['Items'] = item_list
    content['DeliveryDate'] = est_delivery_date
    content['ShippingMethodList'] = shipping_method_list
    content['cal'] = GenerateShippingCalander(time.strftime("%m/%d/%Y", time.localtime()))
    content['Settings'] = settings
    
    content.update(csrf(request))
    content.update(leftwidget(request))
    return render_template(request,'OrderConfirmation.html', content)

#======================================================================

class CheckOutLoginViewClass(TemplateView):

  def GetRecaptcha(self, request):
      value = random.randrange(10000, 99999, 1)
      request.session['ReCaptcha'] = value
      return value

  def get(self, request, *args, **kwargs):
    error_message = ""
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
    
    if 'gateway' in request.GET:
      request.session['PaymentGateway'] = request.GET['gateway']    

    content = {'page_title': "Checkout Login",
               'LoginForm':LoginForm,
               'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
               'error_message': error_message,
              }
    content.update(leftwidget(request))
    return render_template(request,'CheckOutLogin.html', content)

def SaveOrder(request, transactionid):
    customer = request.session['Customer']
    cart_items = request.session['CartItems']

    if request.session['PaymentGateway'] != 'None':
      payment_method = PaymentMethods.objects.filter(payment_gateway=request.session['PaymentGateway'])[0].gateway_id
    else:
      payment_method = -1
    
    order = Orders()
    if customer.contactid == -1:
      # For guest login
      order.oemail = request.session['GuestEMail']
    else:
      # For customer login
      order.oemail = customer.email

    order.ocustomerid = customer.contactid
    order.ofirstname = customer.billing_firstname
    order.olastname = customer.billing_lastname
    order.oaddress = customer.billing_address
    order.oaddress2 = customer.billing_address2
    order.ocity = customer.billing_city
    order.ostate = customer.billing_state
    order.ocountry = customer.billing_country
    order.ozip = customer.billing_zip
    order.ophone = customer.billing_phone

    order.oshipfirstname = customer.shipping_firstname
    order.oshiplastname = customer.shipping_lastname
    order.oshipaddress = customer.shipping_address
    order.oshipaddress2 = customer.shipping_address2
    order.oshipcity = customer.shipping_city
    order.oshipstate = customer.shipping_state
    order.oshipcountry = customer.shipping_country
    order.oshipzip = customer.shipping_zip
    order.oshipphone = customer.shipping_phone

    order.opaymethod = payment_method
    order.odate = datetime.datetime.now()
    order.orderamount = request.session["CartInfo"].order_total
    order.otax = request.session["CartInfo"].tax_total
    order.ocomment = request.session['OrderComment']
    order.order_status = 1
    
    if request.session["PaymentGateway"] == 'AUTHORIZENET' and 'CreditCard' in request.session:
      card_dict = request.session['CreditCard']
      order.ocardno = card_dict['number'] 
      order.ocardname = card_dict['first_name'] + " " + card_dict['last_name'] 
      order.ocardexpiresmonth = card_dict['month']
      order.ocardexpiresyear = card_dict['year']
      order.ocardverification =  card_dict['code']
    
    if 'CouponCode' in request.session:
      order.coupon = request.session['CouponCode']
      order.coupondiscount = request.session["PromotionsTotal"]

    order.oprocessed = 0

    max_invoice =  Orders.objects.aggregate(Max('invoicenum'))['invoicenum__max']   
    
    order.invoicenum_prefix = 'SWF-'
    order.invoicenum = max_invoice + 1 
    
    order.save()
    obj = Orders.objects.all().latest('orderid')
    
    # Updating Transaction Details
    transaction = Transactions()
    transaction.orderid = obj.orderid # Recent order ID
    transaction.amount = order.orderamount
    transaction.transactionid = transactionid # Function Parameter
    transaction.paymenttype = order.opaymethod
    transaction.save()
    
    reward_points_total = 0 
    # Adding Items.    
    for item_id, item in cart_items.items():
      oitem = Oitems()
      oitem.orderid = obj.orderid # Recent order ID
      oitem.catalogid = item.catalog_id
      oitem.orderitemid = item.catalog_id
      oitem.itemname = item.item_name
      oitem.numitems = item.quantity
      
      reward_points_total += item.reward_points * item.quantity

      if item.saleprice > 0:
        oitem.unitprice = item.saleprice
      else:
        oitem.unitprice = item.price
        
      oitem.save()
      
      # Calculating Rewards and Adding to the customer_rewards tables
      customer_reward = CustomerRewards()
      customer_reward.contactid = customer.contactid
      customer_reward.orderid = obj.orderid
      customer_reward.points = reward_points_total
      customer_reward.datetime = datetime.datetime.now()
      customer_reward.giftcertid = 0
      
      customer_reward.save()
      
      if "ShippingMethod" in request.session:
        shipping_method_hash = request.session['ShippingMethod']
        for key, value in shipping_method_hash.items():
          shp_cat_id = key
          user_inputs = value
          for input_field, input_value in user_inputs.items():
            shipping_tupple = Shippingtuple()
            shipping_tupple.shippingcategoryid = shp_cat_id
            shipping_tupple.orderid = obj.orderid
            shipping_tupple.name =  input_field
            shipping_tupple.stringvalue = input_value
            
#             if input_field == "OverNightShipping":
#               shipping_tupple.stringvalue = input_value
#             if input_field == "HoldPackageAtFedex":
#               shipping_tupple.stringvalue = input_value
#             if input_field == "ReceiveDeliveryNotificationEMail":
#               shipping_tupple.stringvalue = input_value
#             if input_field == "ReceiveDeliveryNotificationSMS":
#               shipping_tupple.stringvalue = input_value

            shipping_tupple.save()
        del request.session['ShippingMethod']
      
      if 'StoreCredit' in request.session:
        cart_info = request.session['CartInfo']
        swf_cust_credit_obj = SwfCustomerCreditsLog.objects.filter(id = cart_info.store_credit_id)[0]
        swf_cust_credit_obj.customers_credit = cart_info.store_credit
        swf_cust_credit_obj.customers_credit_applied = datetime.datetime.now()
        swf_cust_credit_obj.save()
        del  request.session['CartInfo']
        del  request.session['StoreCredit']
        
      
      request.session["CartItems"]  = {}
      
    return obj.orderid


class CheckOutCallBackViewClass(TemplateView):

  @csrf_exempt
  def get(self, request, *args, **kwargs):
    error_message = ""

    tx = request.GET['tx']
    status = request.GET['st']
    amount = request.GET['amt']
    currency = request.GET['cc']
    item_number = request.GET['item_number']
    
    tran_list = Transactions.objects.filter(transactionid = tx)

    invoice_no = ""
    if not tran_list:
      order_id = SaveOrder(request, tx)
      oobj = Orders.objects.get(orderid = order_id)
      invoice_no = oobj.invoicenum_prefix + str(oobj.invoicenum)
    else:
      tran_obj = tran_list[0]
      order_id = tran_obj.orderid
      error_message = "Transaction is already recorded. Please find the order number below"  
    
    
    content = {'page_title': "Payment Confirmation",
               'tran_error_message': error_message,
               'tx': tx,
               'status': status,
               'amount': amount,
               'currency': currency,
               'item_number': item_number,
               'OrderID': invoice_no 
              }
    if 'StoreCredit' in request.session:
        del request.session['StoreCredit']

        
    return render_template(request,'PaypalPurchase.html', content)

class PaypalRedirectionViewClass(TemplateView):
  @csrf_exempt
  def get(self, request, *args, **kwargs):
    content = {'page_title': "Paypal Redirection", 'Settings': settings}
    return render_template(request, 'PaypalRedirection.html', content)

class MurthyTestViewCalss(TemplateView):

  def get(self, request, *args, **kwargs):
    html = "<h3>"
    cart_dict = {}
    cart = CartInfo()
    cart_dict = cart.Add(cart_dict, 186)
    if cart.IsError:
      html = "<font color='red'> 186 " + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Add(cart_dict, 249)
    if cart.IsError:
      html = "<font color='red'> 249" + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Add(cart_dict, 249)
    if cart.IsError:
      html = "<font color='red'> 249" + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Add(cart_dict, 423)
    if cart.IsError:
      html = "<font color='red'> 423" + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Update(cart_dict, 423, 5)
    if cart.IsError:
      html = "<font color='red'> 423" + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Add(cart_dict, 15)
    if cart.IsError:
      html = "<font color='red'> 4884" + cart.Error() +  "</font>"
      return HttpResponse(html)
    
    cart_dict = cart.Add(cart_dict, 16)
    if cart.IsError:
      html = "<font color='red'> 4884" + cart.Error() +  "</font>"
      return HttpResponse(html)

    cart_dict = cart.Add(cart_dict, 18)
    if cart.IsError:
      html = "<font color='red'> 4884" + cart.Error() +  "</font>"
      return HttpResponse(html)

    shipping_items = cart.GetItemsByShippingCategory(cart_dict)
    for myShipping in shipping_items:
      html += "<h3>%s</h3>" %myShipping.id
      if myShipping.shipping_items:
        for cart_item in myShipping.shipping_items:
          html += str(cart_item.catalog_id) + "=>" + cart_item.item_name + "=>" + str(cart_item.quantity) + "Shipping Category: %d<br>" %(cart_item.shipping_category)

    request.session['MyCartItems'] = shipping_items
    return HttpResponse(html)


class ShippingCalander(TemplateView):
  
  @csrf_exempt
  def get(self, request, *args, **kwargs):
    content = {}
    catid = int(request.GET['catid'])
    sc_obj = ShippingCategory.objects.get(id=catid)
    
    cartinfo = request.session["CartInfo"]
    (shipping_charge, fuel_charge, freeshipping_diff) = cartinfo.GetShippingCharge(catid, cartinfo.subtotal, 'FL', [])
    
    if 'dt'  in request.GET:
      dt = request.GET['dt']
    else:
      dt = time.strftime("%m/%d/%Y", time.localtime())
      
    if "prev" in request.GET:
      dt = DateSub(dt)
      
    if "next" in request.GET:
      dt = DateAdd(dt)
    
    next_day_shipping = 0
    if catid == 13:  
      next_day_shipping = 15
    else:
      next_day_shipping = 10
    
    second_day_shipping = shipping_charge # For considering same as Ground Shipping.
    
    shp_method_seq = int(request.GET['seq'])
    selected_month = time.strftime("%B %Y", time.strptime(dt, "%m/%d/%Y"))
    content['category_id'] = catid
    content['dt'] = dt
    content['selected_month'] = selected_month
    content['key'] = shp_method_seq 
    content['cal'] = GenerateShippingCalander(dt)
    content['GroundShipping'] = shipping_charge
    content['OverNightShipping'] = next_day_shipping
    content['SecondDayShipping'] = second_day_shipping
    content['SaturdayDelivey'] = sc_obj.saturday_delivery
 
     
    return render_template(request, 'ShippingDeliveryCal.html', content)

  @csrf_exempt
  def post(self, request, *args, **kwargs):
    cards_list = [('4111111111111111', 'Account ending in 2003'), ('378282246310005', 'Account ending in 2004'), ('4111111111111111', 'Account ending in 2005')]
    form = RadioForm(request.POST, choices=cards_list) 
    if form.is_valid():
      credit_card = form.cleaned_data['previous_cards']
      return HttpResponse("<h1>Form is Clean => %s</h1>" %credit_card)
    
    content = {}
    return render_template(request, 'RadioTest.html', content)

class RadioButtonTest(TemplateView):
  
  @csrf_exempt
  def get(self, request, *args, **kwargs):
    data = {}
    content = {}
    #data['previous_cards'] = (('4111111111111111', 'Account ending in 2003'), ('378282246310005', 'Account ending in 2004'), ('4111111111111111', 'Account ending in 2005'),)
    form = RadioForm()
    content['form'] = form
    return render_template(request, 'RadioTest.html', content)

  @csrf_exempt
  def post(self, request, *args, **kwargs):
    cards_list = [('4111111111111111', 'Account ending in 2003'), ('378282246310005', 'Account ending in 2004'), ('4111111111111111', 'Account ending in 2005')]
    form = RadioForm(request.POST, choices=cards_list) 
    if form.is_valid():
      credit_card = form.cleaned_data['previous_cards']
      return HttpResponse("<h1>Form is Clean => %s</h1>" %credit_card)
    
    content = {}
    return render_template(request, 'RadioTest.html', content)

class GiftCertificateView(TemplateView):
  #BuyGift
  
  @csrf_exempt
  def get(self, request, *args, **kwargs):
    data = {}
    content = {}
    #item_id = request.GET['item_id']
    #cart_item = CartItem(item_id)
    content["item_id"] = 11
    return render_template(request, 'BuyGift.html', content)
