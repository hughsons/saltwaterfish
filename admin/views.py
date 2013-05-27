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
import logging
import hashlib
from google.appengine.api import files

try:
    files.gs
except AttributeError:
    import gs
    files.gs = gs

PERPAGE=50

def checkadminlogin_dispatch(f):
    def wrap(request, *args, **kwargs):
        if 'IsLogin' in request.session and request.session['IsLogin'] and 'Staff' in request.session and request.session['Staff'].username !="":
            staff_list = Admins.objects.filter(username = request.session['Staff_username'], pass_field = hashlib.md5(request.session['Staff_password']).hexdigest())
            if staff_list:
                request.session['IsLogin'] = True
                request.session['Staff'] = staff_list[0]
                success = True
            else:
                return HttpResponseRedirect('/logout')
            logging.info('Fetch Started::  %s', staff_list[0])
        else:
            return HttpResponseRedirect('/logout')
        return f(request, *args, **kwargs)
    return wrap


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

class LoginRequiredMixin(object):
    @method_decorator(checkadminlogin_dispatch)
    def dispatch(self,request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

class CMSClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        count = Extrapages.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allpages = Extrapages.objects.all()[offset-100:offset]
        content = {'page_title': "Summary",
                   'allpages':allpages,
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "cms_pages.htm", content)

class CMSEditClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
         
        pageid = request.GET['pageid']
        allpages = Extrapages.objects.get(id=pageid)
        content = {'page_title': "Summary",
                   'allpages':allpages,
                    
                   }
        return render_template(request, "cms_pages_edit.htm", content)

class EmailViewClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        count = Emails.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allpages = Emails.objects.all()[offset-100:offset]
        content = {'page_title': "Admin :: Email List",
                   'allpages':allpages,
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "email_pages.htm", content)

class EmailEditClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        pageid = request.GET['id']
        allpages = Emails.objects.get(id=pageid)
        content = {'page_title': "Admin::Email Edit",
                   'allpages':allpages,
                   }
        return render_template(request, "email_pages_edit.htm", content)


class CMSAddFormClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Summary",}
        return render_template(request, "cms_pages_add.htm", content)

class TitlesContentClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        count = Html.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allpages = Html.objects.all()[offset-100:offset]
        content = {'page_title': "Summary",
                   'allpages':allpages,
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "titles_content.htm", content)

class ProductWishListClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        #allitems = ProductWaitinglist.objects.annotate(dcount=Count('catalogid')).values('catalogid',
        #                                                                                 'current_stock',
        #                                                                                 'products__catalogid').all()[offset-100:offset]
        allitems = ProductWaitinglist.objects.raw('select count(*) as dcount,product_waitinglist.catalogid,products.id,name,current_stock from product_waitinglist,products where product_waitinglist.catalogid=products.catalogid group by catalogid')[offset-100:offset]
        count = ProductWaitinglist.objects.values('catalogid').annotate(dcount=Count('catalogid')).count()
        #return HttpResponse(allitems)
        content = {'page_title': "Summary",
                   'allitems':allitems,
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "products_wish_list.htm", content)

class ProductWishViewClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        itemid = request.GET['itemid']
        allitems = ProductWaitinglist.objects.filter(catalogid=itemid).all()[offset-100:offset]
       
        count = ProductWaitinglist.objects.filter(catalogid=itemid).all().count()
        #return HttpResponse(allitems)
        content = {'page_title': "Summary",
                   'allitems':allitems,
                   'count':count,
                   'page_num':page_num,
                   'itemid':itemid,
                   }
        return render_template(request, "products_wish_list_view_list.htm", content)

class ReviewAllClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        
        allitems = ProductReview.objects.raw('select count(*) as dcount,product_review.catalogid,products.id,name,thumbnail from product_review, products where product_review.catalogid=products.catalogid group by catalogid')[offset-100:offset]
        count = ProductReview.objects.values('catalogid').annotate(dcount=Count('catalogid')).count()
        #return HttpResponse(allitems)
        content = {'page_title': "Summary",
                   'allitems':allitems,
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "products_7_reviews.htm", content)

class ProductsReviewsViewClass(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
         
        itemid = request.GET['itemid']
        allitems = ProductReview.objects.filter(catalogid=itemid).all()
       
        count = ProductReview.objects.filter(catalogid=itemid).all().count()
        #return HttpResponse(allitems)
        content = {'page_title': "Summary",
                   'allitems':allitems,
                   'count':count,                   
                   'itemid':itemid,
                   }
        return render_template(request, "products_review_view_list.htm", content)


class ProductsReviewEditFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        itemid = request.GET['itemid']
        allitems = ProductReview.objects.get(id=itemid)
        content = {'page_title': "Summary",
                   'allitems':allitems,
                   #'count':count,
                   #'page_num':page_num,
                   'itemid':itemid,
                   }
        return render_template(request, "products_7_reviews_edit_2_edit.htm", content)
 

class ApanelViewClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile",}
        return render_template(request, "home-page-admin.htm", content)

class CustomersViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        count = customers.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        content = {'page_title': "Profile",
                   'customers':customers.objects.all()[offset-100:offset],
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "customers.htm", content)

class CRMViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        
        if request.GET['page'] == "":
            page_num = 1
        else:
            page_num = request.GET['page']
        if 'status' in request.GET and request.GET['status'] != "":
            status = request.GET['status']
        else:
            status = 1
        count = Crm.objects.filter(status=status).count()
        page_num = int(page_num)
        offset = page_num * 100
        content = {'page_title': "Profile",
                   'allitems':Crm.objects.all().filter(status=status)[offset-100:offset],
                   'count':count,
                   'page_num':page_num,
                   }
        return render_template(request, "crm.htm", content)

class CRMEditViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        crmid = request.GET['id']
        allitems = Crm.objects.get(id=crmid)
        categories = ProductCategory.objects.all()
        content = {'page_title': "Profile",
                   'allitems':allitems,
                   'manufacturers':Manufacturer.objects.all(),
                   'categories': categories,}
        return render_template(request, "crm_edit.htm", content)

class StaffViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Site Staff",
                   'customers':Admins.objects.all()[:100],
                   'count':Admins.objects.count(),}
        return render_template(request, "admins.htm", content)

class CategoryViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        count = Category.objects.count()
        if request.GET['page'] == "":
            page_num = 1
            
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        content = {'page_title': "Profile",
                   'customers':Category.objects.all()[offset-100:offset],
                   'count':count,
                   'page_num':page_num,}
        return render_template(request, "categories.htm", content)

class CustomerAddFormClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'title': "Add Customer",}
        return render_template(request, "customer_add.htm", content)

class CustomerInfoClass(LoginRequiredMixin,TemplateView):
    #summary = Customers.objects.all()
    def get(self, request, *args, **kwargs):
        cid = request.GET['id']
        customer = customers.objects.get(contactid=cid)
        customeremail= customer.email
        customerrewards = CustomerRewards.objects.filter(contactid=cid).all()
        totalrewards = CustomerRewards.objects.filter(contactid=cid).aggregate(Sum('points'))
        #customers_promocode = SwfCustomerCreditsLog.objects.values_list('customers_promocode', flat=True) 
        #customers_promocode = customers_promocode['customers_promocode']
        #storerewards = SwfCustomerCreditsLog.objects.filter(customers_email_address=customeremail)
        storerewards = SwfCustomerCreditsLog.objects.raw('select *,swf_customer_credits_log.id as sid from swf_customer_credits_log , promotions where customers_promocode = coupon AND customers_email_address="'+customeremail+'" AND customers_promocode != ""')
        fulldata = list(storerewards)
        try:
            wish_id = WshWishlist.objects.get(customerid=cid)
            wishitems = WsiWishlistitems.objects.filter(wsh_id=wish_id.wsh_id)
        except Exception as e:
            wishitems = ""
            
                    
        content = {'page_title': "Customers Info",
                   'customer': customer,
                   'customerorders':Orders.objects.filter(ocustomerid=cid).all(),
                   'wishlists':wishitems,
                   'customerrewards':customerrewards,
                   'totalrewards':totalrewards,
                   'storerewards':fulldata,                   
                   }
                   #'count':Admins.objects.count(),}
        return render_template(request, "customers_info.htm", content)

class ProductsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        count = Products.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        content = {'page_title': "Profile",
                   'allitems':Products.objects.all()[offset-100:offset],
                   'count':count,
                   'page_num':page_num,}
        return render_template(request, "products.htm", content)


class ProductViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        allitems = Products.objects.get(catalogid=pid)
        categories = ProductCategory.objects.all().filter(catalogid=pid)
        content = {'page_title': "Profile",
                   'allitems':allitems,
                   'manufacturers':Manufacturer.objects.all(),
                   'categories': categories,}
        return render_template(request, "productedit.htm", content)

class ProductRelatedClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        allitems = Products.objects.get(catalogid=pid)
        categories = ProductCategory.objects.all().filter(catalogid=pid)
        content = {'page_title': "Profile",
                   'allitems':allitems,
                   'manufacturers':Manufacturer.objects.all(),
                   'categories': categories,}
        return render_template(request, "productrelated.htm", content)

class ProductsImagesViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        allitems = Products.objects.get(catalogid=pid)
        categories = ProductCategory.objects.all().filter(catalogid=pid)
        content = {'page_title': "Profile",
                   'allitems':allitems,
                   'manufacturers':Manufacturer.objects.all(),
                   'categories': categories,}
        return render_template(request, "images_products.htm", content)

class ApanelViewOrdersClass(LoginRequiredMixin,TemplateView):
        
    def get(self, request, *args, **kwargs):
        order_status = request.GET['order_status']
        if order_status < 1:
            order_status = 1
        else:
            order_status = order_status
        count = Orders.objects.filter(order_status=order_status).count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allitems = Orders.objects.all().filter(order_status=order_status)[offset-100:offset]
        order_status_links = OrderStatus.objects.all().filter(visible='1')
        #crm_messages=CrmMessages.objects.select_related(crmid__orderid='8623')
        
        #return HttpResponse(crm_messages)
        content = {'page_title': "Orders",
                   'allitems':allitems,
                   'count':count,
                   'page_num':page_num,
                   'order_status':order_status,
                   'order_links':order_status_links,}
        return render_template(request, "vieworders.htm", content)

class ApanelViewOrdersStatusClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = OrderStatus.objects.all()
        content = {'page_title': "Orders Status",
                   'allitems':allitems,
                   'order_links':OrderStatus.objects.all().filter(visible='1'),}
        return render_template(request, "orders_status.htm", content)


class OrderPageClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        oid = request.GET['oid']
        order_status_links = OrderStatus.objects.all().filter(visible='1')
        allitems = Orders.objects.get(orderid=oid)
        try:
            transactions = Transactions.objects.get(orderid=oid)
            amount = transactions.amount
            totalamt = Oitems.objects.filter(orderid=oid).aggregate(Sum('unitprice'))
            totalamt = totalamt['unitprice__sum']
        except Exception as e:
            transactions = ""
            totalamt = 0
            amount = 0
        alloiitems = Oitems.objects.all().filter(orderid=oid)
        finaltotal = (totalamt + int(allitems.oshipcost)) - allitems.coupondiscount
        balance = finaltotal - amount
        content = {'page_title': "Orders Status",
                   'allitems':allitems,
                   'alloiitems':alloiitems,
                   'order_links':order_status_links,
                   'totalamt':totalamt,
                   'finaltotal':finaltotal,
                   'paidamt':finaltotal,
                   'transactions':transactions,
                   'balance':balance,
                   }
        return render_template(request, "orderpage.htm", content)

class AddAdminsFormClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        allitems = Admins.objects.all()
        if "mode" in request.GET:
            mode = request.GET['mode']
        else:
            mode = ""
            allitems = ""
        if "id" in request.GET:
            allitems = Admins.objects.get(id=request.GET['id'])
        else:
             allitems = ""
        content = {'page_title': "Add User",
                   'allitems':allitems,
                   'mode':mode,}
        return render_template(request, "admins_add.htm", content)

class RmaPagesClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        count = Rma.objects.count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allitems = Rma.objects.all()[offset-100:offset]
        content = {'page_title': "Orders Status",
                   'allitems':allitems,
                   'count':count,}
        return render_template(request, "rma_pages.htm", content)

class RmaViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        rmaid=request.GET['rmaid']
        allitems = Rma.objects.get(idrma=rmaid)
        content = {'page_title': "View RMA",
                   'allitems':allitems,}
        return render_template(request, "rmaview.htm", content)

class ShippingManagerViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        if "mode" in request.GET:
            mode = request.GET['mode']
        else:
            mode = ""
        allitems = ShippingCategory.objects.all()
        content = {'page_title': "Admin: Shipping Manager View",
                   'allitems':allitems,
                   'mode':mode,}
        return render_template(request, "adminshippingmanager.htm", content)

class TaxManagerViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        if "mode" in request.GET:
            mode = request.GET['mode']
        else:
            mode = ""
        allitems = Tax.objects.all()
        content = {'page_title': "Admin: Tax Manager View",
                   'allitems':allitems,
                   'mode':mode,}
        return render_template(request, "taxmanager.htm", content)

class GiftCertificatesViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        count = GiftCertificates.objects.all().count()
        if request.GET['page'] == "":
            page_num = 1
        else:
            #pages = count/100
            page_num = request.GET['page']
        page_num = int(page_num)
        offset = page_num * 100
        allitems = GiftCertificates.objects.all()[offset-100:offset]
        content = {'page_title': "Admin: Gift Certificate View",
                   'allitems':allitems,
                   'page_num':page_num,
                   'count':count,
                   'order_links':OrderStatus.objects.all().filter(visible='1'),}
        return render_template(request, "giftcertificate_pages.htm", content)

class EditGiftCertificateClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        giftid=request.GET['id']
        allitems = GiftCertificates.objects.get(id=giftid)
        total = allitems.certificate_amount + allitems.certificate_expenses
        content = {'page_title': "Admin :: Edit Gift Certificate",
                   'allitems':allitems,
                   'order_links':OrderStatus.objects.all().filter(visible='1'),
                   'total':total}
        return render_template(request, "edit_giftcertificate.htm", content)

class ProductArticleViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        prod = Products.objects.get(catalogid=pid)
        allitems = ProductArticle.objects.all().filter(catalogid=pid)
        count = allitems.count()
        content = {'page_title': "Admin: Product Articles",
                   'allitems':allitems,
                   'prod':prod,
                   'count':count,
                   }
        return render_template(request, "product_articles.htm", content)

class ProductArticleEditViewClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['id']
        allpages = ProductArticle.objects.get(id=pid)
        content = {'page_title': "Admin :: Edit Article",
                   'allpages':allpages,}
        return render_template(request, "product_article_edit.htm", content)

class ProductArticleAddFormClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        content = {'page_title': "Admin :: Add Article",
                   'pid':pid,}
        return render_template(request, "product_article_add.htm", content)

class ProductReviewsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        prod = Products.objects.get(catalogid=pid)
        allitems = ProductReview.objects.filter(catalogid=pid).all()
        count = allitems.count()
        content = {'page_title': "Admin: Product Articles",
                   'allitems':allitems,
                   'prod':prod,
                   'count':count,
                   }
        return render_template(request, "product_reviews.htm", content)

class ProductOptionEditViewClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET['pid']
        allpages = Products.objects.get(catalogid=pid)
        content = {'page_title': "Admin :: Edit Options",
                   'allpages':allpages,
                   'prod':pid,}
        return render_template(request, "product_options_edit.htm", content)

class BannersViewClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        allpages = SiteBanners.objects.all()
        content = {'page_title': "Admin :: Banner Managements",
                   'allitems':allpages,}
        return render_template(request, "viewbanners.htm", content)

class BannerEditViewClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        bid = request.GET['bid']
        filename = "/gs/swf_product_images/banner/banner5.png"
        allpages = SiteBanners.objects.get(id=bid)
        content = {'page_title': "Admin :: Edit banner",
                   'allpages':allpages,
                   'bannerpath':filename,}
        return render_template(request, "editbanner.htm", content)

class BannersAddFormClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Admin :: Add Banner Managements",}
        return render_template(request, "addbanner.htm", content)

class GCSfilesClass(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Admin :: Add Banner Managements",}
        file_list = files.listdir('/gs/swf_product_images')
        for file_name in file_list:
          if not file_name.__contains__('$folder$'):
            self.response.write('<a href="https://storage.cloud.google.com/%s">%s<a><br>' %(file_name[4:], file_name[4:]))
        #return render_template(request, "gcsfiles.htm", content)
