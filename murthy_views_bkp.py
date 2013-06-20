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
    product_category = ProductCategory.objects.all().filter(catalogid=request.GET['itemid'])
    pcats =""
    for pwcats in product_category:
        pcats += str(pwcats.categoryid)+", "
    pcats = pcats[:-2]+''
    logging.info('categoryid:: %s',pcats)
    relateditems=Products.objects.raw('select * from product_category,products where products.catalogid!='+request.GET['itemid']+' and product_category.catalogid=products.catalogid and hide=0 and categoryid in ('+pcats+')')[:3]

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
    content['relateditems'] = relateditems
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
    sub_total = 0
    shipping_total = 0
    fuelcharge_total = 0
    tax_total = 0
    promotions_total = 0
    order_total = 0

    content = {}
    content = {'page_title': "My Cart"}

    cart_dict = {}
    if 'CartItems' in request.session:
      cart_dict = request.session['CartItems']
    cart = CartInfo()
    shipping_items = cart.GetItemsByShippingCategory(cart_dict)
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
    content['relateditems'] = relateditems
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

class OrderConfirmationView(TemplateView):

  @csrf_exempt
  def get(self, request, *args, **kwargs):
    data = {}
    content = {'page_title': "Order Confirmation"}
    is_login = False;
    is_guest = False;
    gateway = ''
    error_message = ''
    
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
          'first_name':customer.shipping_firstname,
          'last_name':customer.shipping_lastname,
          'address1':customer.shipping_address,
          'address2':customer.shipping_address2,
          'city': customer.shipping_city,
          'state': customer.shipping_state,
          'zip': customer.shipping_zip,
          'country': customer.shipping_country,
          'company': customer.shipping_company,
          'phone': customer.shipping_phone,
          'address_type': 'shipping'}
      
      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)
    else:
      logging.info("Non Login traverse or No customer information in the session")
      data = {'contact_id':0,
          'address_type': 'shipping',
          'username': request.session['GuestEMail']
          }

      temp_data = {'card_holder_name':'John Doe', 'card_number': '4111111111111111', 
                   'card_type':'Master', 'card_expdate':'10/20', 'card_cvn':'123'}
      data.update(temp_data)


    if is_login:
      if gateway == 'paypal':
        form = PaypalOrderFormLoggedIn(data)
      elif gateway == 'AUTHORIZENET':
        orders = Orders.objects.all().filter(ocustomerid = customer.contactid)
        cards_hash = {}
        #for order in orders:
        #  if len(order.ocardno.strip()) > 0:
        #    if order.ocardno not in cards_hash:
        #      cards_hash[order.ocardno] = 1
               
        cards_list = [('4111111111111111', 'Account ending in 2003'), ('378282246310005', 'Account ending in 2004'), ('4111111111111111', 'Account ending in 2005')]
        #cards_list = []
        #for cardno in cards_hash.keys():
        #  cards_list.append((cardno,  'Account Ending in xxx - xxx - %s' %cardno[-4:]))

        data['previous_cards'] = cards_list
        form = AuthorizeNetFormLoggedIn(data)
      else:
        form = NoGateWay(data)  

    elif is_guest:
      if gateway == 'paypal':
        form = PaypalOrderFormNoLogin(data)
      elif gateway == 'AUTHORIZENET':
        form = AuthorizeNetFormNoLogin(data)
        #form.fields['previous_cards'].choices = [('1', 'Account Ending in xxx - xxx - 2003'), ('2', 'Account Ending in xxx - xxx - 1099')]
      else:
        form = NoGateWay()  

    content['order_error_message'] = error_message
    content['form'] = form
    content['Items'] = item_list
    content['Settings'] = settings
    
    content.update(csrf(request))
    content.update(leftwidget(request))
    return render_template(request,'OrderConfirmation.html', content)

#======================================================================

class CheckOutLoginViewClasses(TemplateView):

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
               'form':LoginForm,
               'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
               'error_message': error_message,
              }
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

    if not tran_list:
      order_id = SaveOrder(request, tx)
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
               'OrderID': order_id
              }
    if 'StoreCredit' in request.session:
        del request.session['StoreCredit']
        del request.session['StoreCreditObject']
        
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
