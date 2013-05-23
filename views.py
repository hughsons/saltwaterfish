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
import random, logging
import functools
from functools import wraps
from django.core.context_processors import csrf
PERPAGE=50
class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

def checkuserlogin_dispatch(f):
    def wrap(request, *args, **kwargs):
        if 'IsLogin' in request.session and request.session['IsLogin'] and request.session['Customer'].email !="":
            customer_list = customers.objects.filter(email = request.session['Customer'].email, pass_field = request.session['Customer'].pass_field,custenabled=1)
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

class MyAccountWidget(TemplateView):
    def get(self, request):
        content = {'form':LoginForm,}
        return render_template( "myaccount_widget.htm", content)

class HomePageClass(TemplateView):
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value
    def get(self, request, *args, **kwargs):
        error_message = ""
        if "ErrorMessage" in request.session:
          error_message = request.session["ErrorMessage"]
          del request.session["ErrorMessage"]
          
        if 'IsLogin' in request.session and request.session['IsLogin']:
            login_is = request.session['IsLogin']
        else:
            login_is = ""
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'login_is':login_is,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
                   'error_message': error_message,
                   }
        return render_template(request, "front.htm", content)
   
class RegistrationViewClass(TemplateView):
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value
    def get(self, request, *args, **kwargs):
        message = ""
        error_message = ""
        if 'Message' in request.session:
          message = request.session['Message']
          del request.session['Message']

        if 'ErrorMessage' in request.session:
          error_message = request.session['ErrorMessage']
          del request.session['ErrorMessage']
            
        content = {'title': "User Registration",
                   'form':RegistrationForm,
                   'loginform':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
                   'message': message,
                   'error_message': error_message
                   }
        return render_template(request, "registration.htm", content)

class QuickListClass(TemplateView):
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value

    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'cat' in request.GET:
            cat=request.GET['cat']
        else:
            cat = 15
        content = {'title': "Quick List",
                   'cat': cat,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
                    }
        return render_template(request, "quick_list.htm", content)

class ViewCategoryClass(TemplateView):
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value

    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'id' in request.GET:
            cat=request.GET['id']
        else:
            cat = ""
        category = Category.objects.get(id=cat)
        content = {'title': "Quick List",
                   'cat': category,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
                    }
        return render_template(request, "category.htm", content)

class ViewPagesClass(TemplateView):
    def GetRecaptcha(self, request):
        value = random.randrange(10000, 99999, 1)
        request.session['ReCaptcha'] = value
        return value

    def get(self, request, *args, **kwargs):
        pageid = request.GET['pageid']
        allpages = Extrapages.objects.get(id=pageid)
        content = {'page_title': "Summary",
                   'allpages':allpages,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
                   }
        return render_template(request, "pages.htm", content)


class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile"}
        #content['customerorders'] = Orders.objects.filter(ocustomerid=customer.contactid).all(),
        content = {'page_title': "Summary",
                   'customer':request.session['Customer'],
                   'form':LoginForm,
                   }
        object_list = ProductWaitinglist.objects.filter(userid = request.session['Customer'].contactid).count()
        content['wish_list_length'] = object_list
        return render_template(request, "myaccount.html", content)
    def post(self, request, *args, **kwargs):
        pass

class ProductListViewClass(TemplateView):

  def get(self, request, *args, **kwargs):
    content = {}
    error_message = ''
    message = ''
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
      del request.session['ErrorMessage']

    if 'Message' in request.session:
      message = request.session['Message']
      del request.session['Message']
      
    content['error_message'] = error_message
    content['message'] = message
    
    product_list = Products.objects.all()[:50]
    content['product_list'] = product_list 
    return render_to_response('productlist.html', content)

class ChangePwdViewClass(LoginRequiredMixin, TemplateView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile - Password Change"}

        error_message = ""
        if "ErrorMessage" in request.session:
          logging.info("\n\nErrors on page submit\n\n")
          error_message = request.session["ErrorMessage"]
          del request.session["ErrorMessage"]

        if request.session["IsLogin"] == False: return HttpResponseRedirect('/')
        customer = request.session['Customer']
        prefill_data = {'username':customer.email}
        form = ChangePwdForm(prefill_data)
        content = {'page_title': "Summary",
                   'customer':request.session['Customer'],
                   'form':form,
                   'error_message':error_message,
                   }
        return render_template(request, "ChangePwd.html", content)
        #content['form'] = form
        #content['error_message'] = error_message     
        #content.update(csrf(request))
        #return render_to_response("ChangePwd.html", content)

class AddressFormViewClass(LoginRequiredMixin,TemplateView):
    """ Page Name: /GetAddress """
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.session["IsLogin"] == False: return HttpResponseRedirect('/')
        address_type = request.GET['address_type']
        customer = request.session['Customer']
        d = {}
        if address_type == 'billing':
          d = {'contact_id':customer.contactid,
               'first_name':customer.billing_firstname,
               'last_name':customer.billing_lastname,
               'address1':customer.billing_address,
               'address2':customer.billing_address2,
               'city': customer.billing_city,
               'state': customer.billing_state,
               'zip': customer.billing_zip,
               'country': customer.billing_country,
               'company': customer.billing_company,
               'phone': customer.billing_phone,
               'address_type': 'billing'}
        elif address_type == 'shipping':
          d = {'contact_id':customer.contactid,
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

            
        content = {}
        content['customer'] = customer
        form = AddressForm(d)

        content['form'] = form
        content.update(csrf(request))
        return render_to_response("AddressForm.html", content)
    
class CartItems(object):

  def __init__(self, id, name, price, saleprice, quantity, shipping, tax, image1, image2, image3, extra_field_3=""):
      self.id = id
      self.name = name
      self.quantity = quantity
      self.price = price
      self.saleprice = saleprice,
      if saleprice <= 0 :
          self.subtotal = price * quantity
      else:
          self.subtotal = saleprice * quantity
      
      self.shipping = shipping
      self.tax = tax
      self.total = float(self.subtotal) + float(shipping) + (float(self.subtotal) * float(tax)/100.0)

      self.image1 = image1
      self.image2 = image2
      self.image3 = image3
      self.extra_field_3 = extra_field_3

class CartConfirmClass(TemplateView):

  def get(self, request, *args, **kwargs):
    item_id = 0
    content = {}
    if "itemid" in request.GET:
      item_id = int(request.GET['itemid'])
    
    item = Products.objects.filter(catalogid=item_id)[0]
    if item.stock == 0:
       # If quantity is out of stock, removing the item from the cart.
       cart_items = request.session["CartItems"]
       if cart_items: del cart_items[item_id]
       request.session["CartItems"] = cart_items
       return HttpResponse("<h3>Quantity is out of stock. Click <a href='productlist'>here</a> to continue shopping.</h3>")
    
    cart_item = CartItems(item.catalogid, item.name, item.price,
                          item.saleprice, 1, 0.0, 0.0,
                            item.image1, item.image2, item.image3)

    if 'CartItems' in request.session:
      cart_items = request.session["CartItems"]
      item_count = 0
      sub_total = 0
      for key, value in cart_items.items():
        if key == item_id:
          item_count += value
          sub_total = sub_total + (cart_item.subtotal * value)
                          
      content['ItemCount'] = item_count
      content['subtotal'] = sub_total
      
    else:
      content['ItemsHash'] = {}

    content['item'] = cart_item
    
    return render_template(request,'CartConfirmation.html', content)


class ViewCartViewClass(TemplateView):
  #Page Url: /viewcart
  #Last Modified: 2013-15-19 23:30

  def get(self, request, *args, **kwargs):
    content = {}
    content = {'page_title': "My Cart"}
    if 'CartItems' in request.session:
      cart_items = request.session["CartItems"]
      content['ItemsHash'] = request.session["CartItems"]
    else:
      cart_items = {}
      content['ItemsHash'] = {}

    item_list = cart_items.keys()
    mycart = Products.objects.filter(catalogid__in=item_list)

    #Preparing result to render in html page.
    selected_items = []

    tax_list = Tax.objects.filter(tax_country = 'US', tax_state = 'FL')
    if tax_list:
      tax = tax_list[0]
    else:
      tax = 0.0
    
    for item in mycart:
      logging.info(item.saleprice)
      cart_item = CartItems(item.catalogid, item.name, item.price, item.saleprice,
                            cart_items[item.catalogid], 0.0, tax.tax_value1,
                            item.image1, item.image2, item.image3)

      selected_items.append(cart_item)
      
    request.session['MyCartItems'] = selected_items
    content['MyCartItems'] = selected_items
    content['form'] = LoginForm
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

class MyWishListViewClass(LoginRequiredMixin,TemplateView):

  def get(self, request, *args, **kwargs):
    message = ""
    wish_list_items = []
    content = {'page_title': "My Wish List"}
    customer = request.session['Customer']

    if 'Message' in request.session:
      message = request.session['Message']
      content['message'] = message
      del request.session['Message']

    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
      content['error_message'] = error_message
      del request.session['ErrorMessage']

    #wish_list_master = WshWishlist.objects.filter(customerid = customer.contactid)
    wish_list_master = ProductWaitinglist.objects.filter(userid = request.session['Customer'].contactid)

    catalog_list = []
    for item in wish_list_master:
        catalog_list.append(item.catalogid)

    product_list = Products.objects.filter(catalogid__in=catalog_list)
    content['product_list'] = product_list
    return render_template(request, 'wishlistitems.html', content)

class WishListItemsViewClass(LoginRequiredMixin,TemplateView):

  def get(self, request, *args, **kwargs):
    message = ""
    content = {'page_title': "My Watch List"}
    id = int(request.GET['wsh_id'])
    customer = request.session['Customer']
    if 'Message' in request.session:
        message = request.session['Message']
        del request.session['Message']
        
    wish_list_items = WsiWishlistitems.objects.filter(wsh_id = id).order_by('id')
    catalog_list = []
    for item in wish_list_items:
      catalog_list.append(item.catalogid) 

    product_list = Products.objects.filter(catalogid__in=catalog_list)

    content['wsh_id'] = id
    content['product_list'] = product_list
    content['message'] = message
    return render_template(request, 'wishlistitems.html', content)


class OrderConfirmationView(TemplateView):

  def get(self, request, *args, **kwargs):
    data = {}
    content = {'page_title': "Order Confirmation"}

    cart_items = request.session['MyCartItems']
    customer = request.session['Customer']
    data = {}
    data = {'contact_id':customer.contactid,
        'first_name':customer.billing_firstname,
        'last_name':customer.billing_lastname,
        'address1':customer.billing_address,
        'address2':customer.billing_address2,
        'city': customer.billing_city,
        'state': customer.billing_state,
        'zip': customer.billing_zip,
        'country': customer.billing_country,
        'company': customer.billing_company,
        'phone': customer.billing_phone,
        'address_type': 'shipping'}

    subtotal = 0
    estimated_shipping = 0
    fuel_charge = 0
    order_total = 0
    promotions = 0

    for item in cart_items:
      subtotal += item.subtotal
      estimated_shipping += item.shipping

    order_total = float(subtotal) + float(estimated_shipping)

    content['form'] = AddressForm(data)
    content['SubTotal'] = subtotal
    content['EstimatedShipping'] = estimated_shipping
    content['FuelSurCharge'] = fuel_charge
    content['OrderTotal'] = order_total

    return render_template(request,'OrderConfirmation.html', content)
