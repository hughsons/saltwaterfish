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
from models import customers, Products
import random, logging
import functools
from functools import wraps
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
        content = {'title': "User Registration",
                   'form':RegistrationForm,
                   'loginform':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
                   }
        return render_template(request, "registration.htm", content)


class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile"}
        if request.session["IsLogin"] == False: return HttpResponseRedirect('/')
        customer = request.session['Customer']
        content['customer'] = request.session['Customer']
        #content['customerorders'] = Orders.objects.filter(ocustomerid=customer.contactid).all(),
        return render_to_response("myaccount.html", content)

    def post(self, request, *args, **kwargs):
        pass

class ProductListViewClass(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    product_list = Products.objects.all()[:50]
    content['product_list'] = product_list 
    return render_to_response('productlist.html', content)

    
class CartItems(object):

  def __init__(self, id, name, price, quantity, shipping, tax, image1, image2, image3):
      self.id = id
      self.name = name
      self.quantity = quantity
      self.price = price
      self.subtotal = price * quantity
      self.shipping = shipping
      self.tax = tax
      self.total = float(self.subtotal) + float(shipping) + (float(self.subtotal) * float(tax)/100.0)

      self.image1 = image1
      self.image2 = image2
      self.image3 = image3

class CartConfirmClass(TemplateView):

  def get(self, request, *args, **kwargs):
    id = 0
    content = {}
    if "itemid" in request.GET:
      id = int(request.GET['itemid'])
    
    item = Products.objects.filter(catalogid=id)[0]
    cart_item = CartItems(item.catalogid, item.name, item.price,
                            1, 0.0, 0.0,
                            item.image1, item.image2, item.image3)

    if 'CartItems' in request.session:
      cart_items = request.session["CartItems"]
      item_count = 0
      sub_total = 0
      for key, value in cart_items.items():
        if key == id:
          item_count += value
          sub_total = sub_total + (cart_item.subtotal * value)
                          
      content['ItemCount'] = item_count
      content['subtotal'] = sub_total
      
    else:
      content['ItemsHash'] = {}

    content['item'] = cart_item
    
    return render_to_response('CartConfirmation.html', content)


class ViewCartViewClass(TemplateView):
  #Page Url: /viewcart

  def get(self, request, *args, **kwargs):
    content = {}
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
    for item in mycart:
      cart_item = CartItems(item.catalogid, item.name, item.price,
                            cart_items[item.catalogid], 0.0, 0.0,
                            item.image1, item.image2, item.image3)
      selected_items.append(cart_item)
      
    content['MyCart'] = selected_items
    return render_to_response('ViewCart.html', content)

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
        return render_to_response('login.htm', content)
      else:
        c = {'form': form, 'error_message': error_msg}


      c['recaptcha'] = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request)
      c.update(csrf(request))
      return render_to_response('login.htm', c)




