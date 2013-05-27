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

def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return value

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

def cartwidget(request):
    selected_items = []
    if 'CartItems' in request.session:
        cart_items = request.session["CartItems"]
        item_list = cart_items.keys()
    
        mycart = Products.objects.filter(catalogid__in=item_list)
    
        tax_list = Tax.objects.filter(tax_country = 'US', tax_state = 'FL')
        if tax_list:
          tax = tax_list[0]
        else:
          tax = 0.0
        sub_total = 0
        for item in mycart:
          logging.info(item.saleprice)
          cart_item = CartItems(item.catalogid, item.name, item.price, item.saleprice,
                                cart_items[item.catalogid], 0.0, tax.tax_value1, 0.0, 0.0,
                                item.image1, item.image2, item.image3)

          sub_total += cart_item.subtotal
          selected_items.append(cart_item)
    
    return selected_items

class MyAccountWidget(TemplateView):
    def get(self, request):
        content = {'form':LoginForm,}
        return render_template( "myaccount_widget.htm", content)

class HomePageClass(TemplateView):
   
    def get(self, request, *args, **kwargs):
        
        error_message = ""
        if "ErrorMessage" in request.session:
          error_message = request.session["ErrorMessage"]
          del request.session["ErrorMessage"]
          
        if 'IsLogin' in request.session and request.session['IsLogin']:
            login_is = request.session['IsLogin']
        else:
            login_is = ""
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'login_is':login_is,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'error_message': error_message,
                   'banner_main': SiteBanners.objects.get(banner_type="TopMain"),
                   'cartsitems':cartwidget(request),'total_fines':total_fines,
                   }
        return render_template(request, "front.htm", content)
   
class RegistrationViewClass(TemplateView):
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
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'message': message,
                   'error_message': error_message
                   }
        return render_template(request, "registration.htm", content)

class QuickListClass(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'cat' in request.GET:
            cat=request.GET['cat']
        else:
            cat = 15
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'title': "Quick List",
                   'cat': cat,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'cartsitems':cartwidget(request),'total_fines':total_fines,
                    }
        return render_template(request, "quick_list.htm", content)

class ViewCategoryClass(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'id' in request.GET:
            cat=request.GET['id']
        else:
            cat = ""
        category = Category.objects.get(id=cat)
        content = {'title': "Quick List",
                   'cat': category,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                    }
        return render_template(request, "category.htm", content)

class ViewPagesClass(TemplateView):

    def get(self, request, *args, **kwargs):
        pageid = request.GET['pageid']
        allpages = Extrapages.objects.get(id=pageid)
        content = {'page_title': "Summary",
                   'allpages':allpages,
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   }
        return render_template(request, "pages.htm", content)


class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile"}
        #content['customerorders'] = Orders.objects.filter(ocustomerid=customer.contactid).all(),
        crms = Crm.objects.all().filter(custid=request.session['Customer'].contactid)
        content = {'page_title': "Summary",
                   'customer':request.session['Customer'],
                   'form':LoginForm,
                   'crms':crms,
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

class CartItems(object):

  def __init__(self, id, name, price, saleprice, quantity, shipping, tax, fuelcharge, promotions, image1, image2, image3, extra_field_3=""):
      self.id = id
      self.name = name
      self.quantity = quantity
      self.price = price
      self.saleprice = saleprice
      self.fuelcharge = fuelcharge
      self.promotions = promotions
      if saleprice <= 0 :
          self.subtotal = price * quantity
      else:
          self.subtotal = saleprice * quantity
      
      self.shipping = shipping
      self.tax = tax
      self.taxvalue = float(self.subtotal) * float(tax)/float(100)
      self.total = float(self.subtotal) + float(shipping) + self.taxvalue
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
                          item.saleprice, 1, 0.0, 0.0, 0.0, 0.0,
                            item.image1, item.image2, item.image3)

    # Calculating Sum for all the items.
    if 'CartItems' in request.session:
      cart_items = request.session["CartItems"]
      item_count = 0
      sub_total = 0
      shipping_total = 0
      fuelcharge_total = 0
      tax_total = 0
      promotions_total = 0
      order_total = 0
      
      for key, qty in cart_items.items():
        if key == item_id:
          item_count += qty
          sub_total += (cart_item.subtotal * qty)
          shipping_total += (cart_item.shipping * qty)
          tax_total += (cart_item.taxvalue * qty)
          fuelcharge_total += (cart_item.fuelcharge * qty)
          promotions_total += (cart_item.promotions * qty)
    
      order_total = float(sub_total) + float(shipping_total) + float(fuelcharge_total) + float(tax_total) - float(promotions_total)
    else:
      content['ItemsHash'] = {}

    content['ItemCount'] = item_count
    content['OrderSubTotal'] = order_total

    content['item'] = cart_item
    
    return render_template(request,'CartConfirmation.html', content)

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



class ProductIndexClass(TemplateView):
    def get(self, request, *args, **kwargs):
        temp = ""
        count = Products.objects.filter(catalogid__gt=1, stock__gt=0).count()
        
        if "page" in request.GET and  request.GET['page'] >=1:
            page_num = request.GET['page']
        else:
            page_num = 1
            
        page_num = int(page_num)
        offset = page_num * 100
        allitems = Products.objects.all().filter(catalogid__gt=1, stock__gt=0).order_by('name')[offset-100:offset]
        totalpages = count/100
        for pages in range(totalpages):
            pages=pages+1
            temp+= '<a href="/productindex?page='+str(pages)+'">'+str(pages)+'</a> | '
        temp+= '<a href="/productindex?page='+str(totalpages+1)+'">'+str(totalpages+1)+'</a>'
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'banner_main': SiteBanners.objects.get(banner_type="TopMain"),
                   'count': temp,
                   'allitems': allitems,
                   'cartsitems':cartwidget(request),'total_fines':total_fines,
                   }
        return render_template(request, "productindext.htm", content)

class CategoryIndexClass(TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
         
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'banner_main': SiteBanners.objects.get(banner_type="TopMain"),
                   'allitems': allitems,
                   'cartsitems':cartwidget(request),'total_fines':total_fines,}
        return render_template(request, "categoryindex.htm", content)

class AddRequestFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
        department = CrmDepartment.objects.all().filter(visible=1) 
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'banner_main': SiteBanners.objects.get(banner_type="TopMain"),
                   'allitems': allitems,'department': department,
                   'cartsitems':cartwidget(request),'total_fines':total_fines,}
        return render_template(request, "addrequestform.htm", content)

class EditRequestFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
        department = Crm.objects.all().filter(id=request.GET['crmid'], custid=request.session['Customer'].contactid)
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",
                   'form':LoginForm,
                   'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
                   'banner_main': SiteBanners.objects.get(banner_type="TopMain"),
                   'allitems': allitems,'department': department,
                   'cartsitems':cartwidget(request),'total_fines':total_fines,}
        return render_template(request, "editrequestform.htm", content)

#======================================================================

class CheckOutLoginViewClass(TemplateView):
   def get(self, request, *args, **kwargs):
    total_fines = sum([item.price for item in cartwidget(request)])
    error_message = ""
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
        
    content = {'page_title': "Checkout Login",
               'form':LoginForm,
               'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request),
               'error_message': error_message,
               'cartsitems':cartwidget(request),'total_fines':total_fines,
              }
    return render_template(request,'CheckOutLogin.html', content)

class OrderConfirmationView(TemplateView):

  def get(self, request, *args, **kwargs):
    data = {}
    content = {'page_title': "Order Confirmation"}
    is_login = False;
    is_guest = False;

    if 'IsLogin' in request.session:
      if request.session['IsLogin']:
        is_login = True;

    if 'IsGuest' in request.session:
      if request.session['IsGuest']:
        is_guest = True;
        
    # If there is no login and no guest, then redirect to checkoutlogin page.
    if not is_login and not is_guest:
      return HttpResponseRedirect('/checkoutlogin')

    if 'gateway' in request.GET:
        request.session['PaymentGateway'] = request.GET['gateway']

    cart_items = request.session['MyCartItems']
    is_login = False
    if 'IsLogin' in request.session:
        if request.session['IsLogin'] == True:
            is_login = True
        else:
            is_login = False
        
    data = {}
    # Populating Customer Information if user is logged in.
    if is_login:
      customer = request.session['Customer']
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

class ViewCartViewClass(TemplateView):
  #Page Url: /viewcart
  #Last Modified: 2013-15-19 23:30

  def get(self, request, *args, **kwargs):
    sub_total = 0
    shipping_total = 0
    fuelcharge_total = 0
    tax_total = 0
    promotions_total = 0
    order_total = 0

    content = {}
    content = {'page_title': "My Cart"}
    if 'CartItems' in request.session:
      cart_items = request.session["CartItems"]
      content['ItemsHash'] = request.session["CartItems"]
    else:
      cart_items = {}
      content['ItemsHash'] = {}
      request.session["CartItems"] = cart_items

    logging.info("\n\n\n\nIn View: %s\n\n\n\n" %str(cart_items))
    item_list = cart_items.keys()
    mycart = Products.objects.filter(catalogid__in=item_list)

    # Executing custom query to get the product categories
    #cursor = connection.cursor()
    #cursor.execute("SELECT catalogid, category_name from product_category PC inner join category C on (PC.categoryid = c.id) where PC.catalogid in (%s) order by catalogid", ", ".join([str(x) for x in item_list]))
    #cursor.close()

   

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
                            cart_items[item.catalogid], 0.0, tax.tax_value1, 0.0, 0.0,
                            item.thumbnail, item.image1, item.image2, item.image3)

      sub_total += cart_item.subtotal
      shipping_total += cart_item.shipping
      fuelcharge_total += cart_item.fuelcharge
      tax_total += cart_item.taxvalue
      promotions_total += cart_item.promotions
      selected_items.append(cart_item)
      
    request.session['MyCartItems'] = selected_items
    content['MyCartItems'] = selected_items

    #content['ItemCount'] = item_count
    content['SubTotal'] = sub_total
    content['ShippingTotal'] = shipping_total
    content['FuelTotal'] = fuelcharge_total
    content['TaxTotal'] = tax_total
    content['PromotionsTotal'] = promotions_total
    content['OrderTotal'] = float(sub_total) + float(shipping_total) + float(fuelcharge_total) + float(tax_total) + float(promotions_total)
    
    request.session['SubTotal'] = sub_total
    request.session['ShippingTotal'] = shipping_total
    request.session['FuelTotal'] = fuelcharge_total
    request.session['TaxTotal'] = tax_total
    request.session['PromotionsTotal'] = promotions_total
    request.session['OrderTotal'] = float(sub_total) + float(shipping_total) + float(fuelcharge_total) + float(tax_total) + float(promotions_total)
    total_fines = sum([item.price for item in cartwidget(request)])
    content['total_fines'] = total_fines
    content['cartsitems'] = cartwidget(request)


    content.update(csrf(request))
    return render_template(request,'ViewCart.html', content)
