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
          cart_item = CartItems(item.catalogid, item.name, item.price,
                                item.saleprice, 1, 0.0, 0.0, 0.0, 0.0, item.reward_disable,
                                item.reward_points, item.thumbnail,
                                item.image1, item.image2, item.image3)

          sub_total += cart_item.subtotal
          selected_items.append(cart_item)
    
    return selected_items

def leftwidget(request):
    error_message = ""
    message = ""
    if 'Message' in request.session:
          message = request.session['Message']
          del request.session['Message']
    if "ErrorMessage" in request.session:
        error_message = request.session["ErrorMessage"]
        del request.session["ErrorMessage"]
    if 'IsLogin' in request.session and request.session['IsLogin']:
        login_is = request.session['IsLogin']
    else:
        login_is = ""
    total_fines = sum([item.price for item in cartwidget(request)])
    contents = {'LoginForm':LoginForm,
                'login_is':login_is,
                'recaptcha': GetRecaptcha(request),
                'error_message': error_message,
                'message': message,
                'banner_main': SiteBanners.objects.filter(banner_status=1),
                'cartsitems':cartwidget(request),'total_fines':total_fines,}
    return contents

class HomePageClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Reef Fish, Marine Fish, Coral, Aquarium Supplies & more - Saltwaterfish.com",}
        content.update(leftwidget(request))
        return render_template(request, "front.htm", content)
   
class RegistrationViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'title': "User Registration",
                   'form':RegistrationForm,}
        content.update(leftwidget(request))
        return render_template(request, "registration.htm", content)

class QuickListClass(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'cat' in request.GET:
            cat=request.GET['cat']
        else:
            cat = 15
        content = {'title': "Quick List",'cat': cat,}
        content.update(leftwidget(request))
        return render_template(request, "quick_list.htm", content)

class ViewCategoryClass(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'id' in request.GET:
            cat=request.GET['id']
        else:
            cat = ""
        category = Category.objects.get(id=cat)
        content = {'title': "Quick List",
                   'cat': category,}
        content.update(leftwidget(request))
        return render_template(request, "category.htm", content)

class ViewPagesClass(TemplateView):
    def get(self, request, *args, **kwargs):
        pageid = request.GET['pageid']
        allpages = Extrapages.objects.get(id=pageid)
        content = {'page_title': "Summary",
                   'allpages':allpages,}
        content.update(leftwidget(request))
        return render_template(request, "pages.htm", content)


class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile"}
        #content['customerorders'] = Orders.objects.filter(ocustomerid=customer.contactid).all(),
        crms = Crm.objects.all().filter(custid=request.session['Customer'].contactid)
        content = {'page_title': "Summary",
                   'customer':request.session['Customer'],
                   'crms':crms,
                   }
        object_list = ProductWaitinglist.objects.filter(userid = request.session['Customer'].contactid).count()
        content['wish_list_length'] = object_list
        content.update(leftwidget(request))
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
          
          error_message = request.session["ErrorMessage"]
          del request.session["ErrorMessage"]

        
        customer = request.session['Customer']
        prefill_data = {'username':customer.email}
        form = ChangePwdForm(prefill_data)
        content = {'page_title': "Summary",'customer':request.session['Customer'],'form':form}
        content.update(leftwidget(request))
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

class MyWishListViewClass(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    message = ""
    wish_list_master = ProductWaitinglist.objects.filter(userid = request.session['Customer'].contactid)
    catalog_list = []
    for item in wish_list_master:
        catalog_list.append(item.catalogid)
    product_list = Products.objects.filter(catalogid__in=catalog_list)
    content = {'page_title': "My Wish List"}
    content['product_list'] = product_list
    content.update(leftwidget(request))
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
        content = {'page_title': "Summary",'count': temp,'allitems': allitems,}
        content.update(leftwidget(request))
        return render_template(request, "productindext.htm", content)

class CategoryIndexClass(TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",'allitems': allitems,}
        content.update(leftwidget(request))
        return render_template(request, "categoryindex.htm", content)

class AddRequestFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
        department = CrmDepartment.objects.all().filter(visible=1) 
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",'allitems': allitems,'department': department,}
        content.update(leftwidget(request))
        return render_template(request, "addrequestform.htm", content)

class EditRequestFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Category.objects.all().filter(category_parent=1).order_by('category_parent')
        department = Crm.objects.all().filter(id=request.GET['crmid'], custid=request.session['Customer'].contactid)
        total_fines = sum([item.price for item in cartwidget(request)])
        content = {'page_title': "Summary",'allitems': allitems,'department': department,}
        content.update(leftwidget(request))
        return render_template(request, "editrequestform.htm", content)

class MyOrdersViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        order_status_links = OrderStatus.objects.all().filter(visible='1')
        product_list = Orders.objects.filter(ocustomerid=request.session['Customer'].contactid).order_by('-orderid')
        content = {'page_title': "My Orders",'order_links':order_status_links,'product_list':product_list,}
        content.update(leftwidget(request))
        return render_template(request, 'orders.htm', content)

class MyTicketsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        product_list = Crm.objects.all().filter(custid=request.session['Customer'].contactid)
        content = {'page_title': "My Support Requests",'product_list':product_list,}
        content.update(leftwidget(request))
        return render_template(request, 'tickets.htm', content)

class MyRewardsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        cid = request.session['Customer'].contactid
        product_list = CustomerRewards.objects.all().filter(contactid=cid).order_by('-id')
        totalrewards = CustomerRewards.objects.filter(contactid=cid).aggregate(Sum('points'))
        htmltext = Html.objects.get(id=24)
        content = {'page_title': "My Support Requests",'product_list':product_list,'htmltext':htmltext,
                   'totalrewards':totalrewards,}
        content.update(leftwidget(request))
        return render_template(request, 'reefrewards.htm', content)

class MyGuaranteedRequestsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        orderitems = Orders.objects.filter(ocustomerid = request.session['Customer'].contactid)
        catalog_list = []
        for item in orderitems:
            catalog_list.append(item.orderid)
        product_list = Rma.objects.filter(orderid__in=catalog_list)
        content = {'page_title': "My Support Requests",'product_list':product_list,}
        content.update(leftwidget(request))
        return render_template(request, 'rma.htm', content)

class ContactUsViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "My Support Requests",}
        content.update(leftwidget(request))
        return render_template(request, 'contactus.htm', content)

class TermsConViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "My Support Requests",}
        content.update(leftwidget(request))
        return render_template(request, 'termscon.htm', content)

class WaitingPopupViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        product_list = Products.objects.all().get(catalogid=request.GET['itemid'])
        content = {'page_title': "My Support Requests","products":product_list}
        content.update(leftwidget(request))
        return render_template(request, 'waitinglist_popup.htm', content)

class ReefPackageViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'title': "Quick List",}
        content.update(leftwidget(request))
        return render_template(request, "reefpackage.htm", content)

class ProductInfoViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        product_list = Products.objects.get(catalogid=request.GET['pid'])
        content = {'page_title': product_list.name,"products":product_list}
        content.update(leftwidget(request))
        return render_template(request, 'product.htm', content)

class OrderInfoViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        oid = request.GET['oid']
        product_list = Orders.objects.get(orderid=oid,
                                          ocustomerid = request.session['Customer'].contactid)
        alloiitems = Oitems.objects.all().filter(orderid=oid)
        content = {'page_title': 'Orders Page',"item":product_list,'alloiitems':alloiitems,}
        content.update(leftwidget(request))
        return render_template(request, 'orderinfo.htm', content)

#======================================================================
class CartItems(object):

  def GetParentCategory(self, category_id):
    #SELECT category_name, category_parent from category where id = 4
    cursor = connection.cursor()
    parent_id = 99999
    levels = 0
    while (parent_id > 0 and levels < 100):
      cursor.execute("SELECT id, category_name, category_parent from category where id = %d" %category_id)
      row = cursor.fetchone()
      category_id = row[0]
      category_name = row[1]
      parent_id = row[2]
      category_id = parent_id
      levels += 1

    return (category_id, category_name, parent_id)

  def GetShippingCharge(self, category_name, sub_total):
      shipping_charge = 0.0
      free_shipping_min_value = -1
      if category_name.__contains__('Marine Life'):
        free_shipping_min_value = 199
        if sub_total >= 00.01 and sub_total <= 98.99:
          shipping_charge = 34.99
        elif sub_total >= 99.00 and sub_total <= 198.99:
          shipping_charge = 24.99
        else:
          shipping_charge = 0
            
      elif category_name.__contains__('Live Goods'):
        free_shipping_min_value = 199          
        if sub_total >= 00.01 and sub_total <= 98.99:
          shipping_charge = 34.99
        elif sub_total >= 99.00 and sub_total <= 198.99:
          shipping_charge = 24.99
        else:
          shipping_charge = 0

      elif category_name.__contains__('Live Rock & Sand'):
        free_shipping_min_value = 0
        if sub_total >= 00.01 and sub_total <= 98.99:
          shipping_charge = 4.99
        elif sub_total >= 99.00 and sub_total <= 198.99:
          shipping_charge = 4.99
        else:
          shipping_charge = 4.99

      elif category_name.__contains__('FastTrack Supplies'):
        free_shipping_min_value = 0
        if sub_total >= 00.01 and sub_total <= 98.99:
          shipping_charge = 4.99
        elif sub_total >= 99.00 and sub_total <= 198.99:
          shipping_charge = 4.99
        else:
          shipping_charge = 4.99

      elif category_name.__contains__('Aquarium Supplies On Sale'):
        free_shipping_min_value = 0
        if sub_total >= 00.01 and sub_total <= 98.99:
          shipping_charge = 4.99
        elif sub_total >= 99.00 and sub_total <= 198.99:
          shipping_charge = 4.99
        else:
          shipping_charge = 4.99

      return (shipping_charge, free_shipping_min_value)

  def __init__(self, id, name, price, saleprice, quantity, shipping, tax, fuelcharge, promotions, 
               reward_disable, reward_points, thumbnail, image1, image2, image3, 
               extra_field_3=""):
      self.id = id
      self.name = name
      self.quantity = quantity
      self.price = price
      self.saleprice = saleprice
      #self.fuelcharge = fuelcharge
      self.fuelcharge = 2.99 * quantity
      self.promotions = promotions
      if saleprice <= 0 :
          self.subtotal = price * quantity
      else:
          self.subtotal = saleprice * quantity
      
      self.shipping = shipping
      self.tax = tax
      self.taxvalue = float(self.subtotal) * float(tax)/float(100)
      self.total = float(self.subtotal) + float(shipping) + self.taxvalue + self.fuelcharge - self.promotions
      self.thumbnail = thumbnail
      self.image1 = image1
      self.image2 = image2
      self.image3 = image3
      self.extra_field_3 = extra_field_3
      
      if reward_disable == 0:
        self.reward_points = reward_points
      else:
        self.reward_points = 0   
           
      product_category_list = ProductCategory.objects.filter(catalogid = id)

      logging.info(product_category_list[0].id)
      if product_category_list:
        category_id, category_name, parent_id = self.GetParentCategory(product_category_list[0].categoryid)

      (self.shipping, free_shipping_min_value) = self.GetShippingCharge(category_name, self.subtotal)
      self.free_shipping_suggestion_val = free_shipping_min_value - self.subtotal


      self.category_id = 0

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
                          item.saleprice, 1, 0.0, 0.0, 0.0, 0.0, item.reward_disable, 
                          item.reward_points, item.thumbnail,
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
    content.update(leftwidget(request))
    return render_template(request,'CartConfirmation.html', content)



class CheckOutLoginViewClass(TemplateView):
   def get(self, request, *args, **kwargs):
    total_fines = sum([item.price for item in cartwidget(request)])
    error_message = ""
    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
    
    content = {'page_title': "Checkout Login",}
    content.update(leftwidget(request))
    return render_template(request,'CheckOutLogin.html', content)

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

    cart_items = request.session['MyCartItems']
        
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

    subtotal = 0
    estimated_shipping = 0
    fuel_charge = 0
    order_total = 0
    promotions = 0

    for item in cart_items:
      subtotal += item.subtotal
      estimated_shipping += item.shipping

    order_total = float(subtotal) + float(estimated_shipping)
    
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

    elif is_guest:
      if gateway == 'paypal':
        form = PaypalOrderFormNoLogin(data)
      elif gateway == 'AUTHORIZENET':
        form = AuthorizeNetFormNoLogin(data)
        #form.fields['previous_cards'].choices = [('1', 'Account Ending in xxx - xxx - 2003'), ('2', 'Account Ending in xxx - xxx - 1099')]

    content['order_error_message'] = error_message
    content['form'] = form
    content['SubTotal'] = subtotal
    content['EstimatedShipping'] = estimated_shipping
    content['FuelSurCharge'] = fuel_charge
    content['OrderTotal'] = order_total
    content['Settings'] = settings
    content.update(csrf(request))
    content.update(leftwidget(request))
    return render_template(request,'OrderConfirmation.html', content)

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
    error_message = ''

    if 'ErrorMessage' in request.session:
      error_message = request.session['ErrorMessage']
      content['error_message'] = error_message
      del request.session['ErrorMessage']
        
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
      promotion_value = self.GetPromotionValue(request.session, item.catalogid)
      cart_item = CartItems(item.catalogid, item.name, item.price, item.saleprice,
                            cart_items[item.catalogid], 0.0, tax.tax_value1, 0.0, promotion_value,
                            item.reward_disable, item.reward_points,item.thumbnail, 
                            item.image1, item.image2, item.image3)

      sub_total += cart_item.subtotal
      shipping_total += cart_item.shipping
      fuelcharge_total += cart_item.fuelcharge
      tax_total += cart_item.taxvalue
      promotions_total += cart_item.promotions
      selected_items.append(cart_item)


    # If no promotions are applied on any product, Getting common promotion value
    # for the Cart.
    if promotions_total == 0 and sub_total > 0:
        promotions_total = self.GetPromotionValue(request.session, -1)
      
    request.session['MyCartItems'] = selected_items
    content['MyCartItems'] = selected_items

    #content['ItemCount'] = item_count
    order_total = float(sub_total) + float(shipping_total) + float(fuelcharge_total) + float(tax_total) - float(promotions_total)
    content['SubTotal'] = sub_total
    content['ShippingTotal'] = shipping_total
    content['FuelTotal'] = fuelcharge_total
    content['TaxTotal'] = tax_total
    content['PromotionsTotal'] = promotions_total
    content['OrderTotal'] = order_total
    
    request.session['SubTotal'] = sub_total
    request.session['ShippingTotal'] = shipping_total
    request.session['FuelTotal'] = fuelcharge_total
    request.session['TaxTotal'] = tax_total
    request.session['PromotionsTotal'] = promotions_total
    request.session['OrderTotal'] = order_total


    content.update(csrf(request))
    content.update(leftwidget(request))
    return render_template(request,'ViewCart.html', content)

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
               'form':LoginForm,
               'recaptcha':"https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %self.GetRecaptcha(request),
               'error_message': error_message,
              }
    return render_template(request,'CheckOutLogin.html', content)


def SaveOrder(request, transactionid):
    customer = request.session['Customer']
    cart_items = request.session['MyCartItems']

    payment_method = PaymentMethods.objects.filter(payment_gateway=request.session['PaymentGateway'])[0].gateway_id
    
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
    order.orderamount = request.session["OrderTotal"]
    order.otax = request.session['TaxTotal']
    order.ocomment = request.session['OrderComment']
    
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
    for item in cart_items:
      oitem = Oitems()
      oitem.orderid = obj.orderid # Recent order ID
      oitem.catalogid = item.id
      oitem.orderitemid = item.id
      oitem.itemname = item.name
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
      request.session['MyCartItems'] = {}
      
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
    return render_template(request,'PaypalPurchase.html', content)


class PaypalRedirectionViewClass(TemplateView):
  @csrf_exempt
  def get(self, request, *args, **kwargs):
    content = {'page_title': "Paypal Redirection", 'Settings': settings}
    return render_template(request, 'PaypalRedirection.html', content)

