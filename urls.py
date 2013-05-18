from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.defaults import *
from django.contrib import admin
from views import *
from auth_views import *
from user_actions import *
from admin.admin_actions import *
from admin.views import *

handler500 = 'djangotoolbox.errorviews.server_error'
admin.autodiscover()
urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^$', HomePageClass.as_view(),name='Home'),
    url(r'^accounts/login/$','auth_views.loginpage',name='login'),
	(r'^login$', 'auth_views.loginpage'),
	(r'^adminlogin$', 'auth_views.AdminLoginClass'),
    (r'^alogin$', 'auth_views.Adminloginpage'),
    (r'^logout/$', 'auth_views.logout_view'),
	url(r'^custlogin', 'auth_views.CustomerLoginClass', name='custlogin'),
    url(r'^admin/', include(admin.site.urls)),

# Murthy URLS STARTS HERE	
    url(r'^myaccount', MyaccountViewClass.as_view(), name='myaccount'),
	url(r'^registration', RegistrationViewClass.as_view(), name='registration'),
	url(r'^registeruser', RegistrationActionClass.as_view(), name='registeruser'),
	url(r'^forgetpassword', ForgetPasswordClass.as_view(), name='forgetpassword'),
	url(r'^sendpassword', ForgetPasswordActionClass.as_view(), name='sendpassword'),
    url(r'^productlist$', ProductListViewClass.as_view(), name='ProductList'),
    url(r'^addtocart', AddToCartActionClass.as_view(), name='AddToCart'),
    url(r'^viewcart', ViewCartViewClass.as_view(), name='viewcart'),
    url(r'^cartaction', CartActionsClass.as_view(), name='CartAction'),
    url(r'^cartconfirmation', CartConfirmClass.as_view(), name='CartConfirmation'),
    url(r'^getaddress', AddressFormViewClass.as_view(), name='GetAddress'),
    url(r'^updateaddress', UpdateAddressActionClass.as_view(), name='GetAddress'),
    url(r'^changepwd', ChangePwdViewClass.as_view(), name='GetAddress'),
    url(r'^setnewpassword', ChangePwdActionClass.as_view(), name='GetAddress'),

# Murthy URLS ENDS HERE	

# Simon URLS FRONT END HERE
	url(r'^quicklist', QuickListClass.as_view(), name='quicklist'),
	url(r'^category', ViewCategoryClass.as_view(), name='maincategory'),
	url(r'^pages', ViewPagesClass.as_view(), name='pages'),
# Simon URLS HERE

    url(r'^apanel', ApanelViewClass.as_view(), name='apanel'),
    url(r'^customers', CustomersViewClass.as_view(), name='customers'),
	url(r'^products', ProductsViewClass.as_view(), name='customers'),
	url(r'^productinfo', ProductViewClass.as_view(), name='productinfo'),
	url(r'^productrelated', ProductRelatedClass.as_view(), name='productinfo'),
	url(r'^productoptions', ProductViewClass.as_view(), name='productinfo'),
	url(r'^productarticles', ProductViewClass.as_view(), name='productinfo'),
	url(r'^productreviews', ProductViewClass.as_view(), name='productinfo'),
    url(r'^admins$', StaffViewClass.as_view(), name='admins'),
	url(r'^addadminsform', AddAdminsFormClass.as_view(), name='AddAdminsFormClass'),
    url(r'^categories$', CategoryViewClass.as_view(), name='categories'),
    url(r'^bcustomersinfo', CustomerInfoClass.as_view(), name='customersinfo'),
	url(r'^baddcustomer', CustomerAddFormClass.as_view(), name='customersinfo'),
    url(r'^cmspages', CMSClass.as_view(), name='cmspages'),
	url(r'^titlesandcontent', TitlesContentClass.as_view(), name='cmspages'),
	url(r'^cmspageedit', CMSEditClass.as_view(), name='CMSEditClass'),
	url(r'^addcmsform', CMSAddFormClass.as_view(), name='addcmsform'),
	url(r'^product_wish_list', ProductWishListClass.as_view(), name='product_wish_list'),
	url(r'^productwish_list_view', ProductWishViewClass.as_view(), name='product_wish_list_view'),
	url(r'^reviews-edit-2-edit', ProductsReviewEditFormClass.as_view(), name='product_wish_list_view'),
	#url(r'^products-7-reviews', ReviewProductsClass.as_view(), name='products-7-reviews'),
	url(r'^all_product_reviews$', ReviewAllClass.as_view(), name='all_product_reviews'),
	url(r'^reviews-edit-all', ProductsReviewsViewClass.as_view(), name='products-7-reviews'),
	url(r'^productimages', ProductsImagesViewClass.as_view(), name='products-7-reviews'),
	url(r'^vieworders', ApanelViewOrdersClass.as_view(), name='ApanelViewOrdersClass'),
	url(r'^ordersstatus', ApanelViewOrdersStatusClass.as_view(), name='ApanelViewOrdersClass'),
	url(r'^giftcertificates', GiftCertificatesViewClass.as_view(), name='ApanelViewOrdersClass'),
	url(r'^editgiftcertificates', EditGiftCertificateClass.as_view(), name='EditGiftCertificateClass'),
	url(r'^orderpage', OrderPageClass.as_view(), name='OrderPageClass'),
	url(r'^rmapages', RmaPagesClass.as_view(), name='RmaPagesClass'),
	url(r'^rmaview', RmaViewClass.as_view(), name='RmaViewClass'),
	url(r'^adminshippingmanager', ShippingManagerViewClass.as_view(), name='RmaViewClass'),
	url(r'^addshippingmanager', ShippingManagerActionClass.as_view(), name='RmaViewClass'),
	url(r'^taxmanager', TaxManagerViewClass.as_view(), name='TaxManagerViewClass'),
	url(r'^actiontaxmanager', TaxManagerActionClass.as_view(), name='TaxManagerActionClass'),
	url(r'^actioncmsmanager', CMSManagerActionClass.as_view(), name='CMSManagerActionClass'),
	url(r'^emailpages', EmailViewClass.as_view(), name='emailpages'),
	url(r'^emailpageedit', EmailEditClass.as_view(), name='EmailEditClass'),
	url(r'^actionemailmanager', EmailManagerActionClass.as_view(), name='EmailManagerActionClass'),
	url(r'^actiongiftmanager', GiftManagerActionClass.as_view(), name='GiftManagerActionClass'),
	url(r'^actionosmanager', OrderStatusActionClass.as_view(), name='OrderStatusActionClass'),
	url(r'^adminactions', StaffActionClass.as_view(), name='StaffActionClass'),
	url(r'^saveadmin', StaffActionClass.as_view(), name='StaffActionClass'),
	url(r'^changeadminpass', StaffActionClass.as_view(), name='StaffActionClass'),
	url(r'^deletecustomer', CustomerActionClass.as_view(), name='CustomerActionClass'),
	url(r'^editcustomer', CustomerActionClass.as_view(), name='CustomerActionClass'),
	url(r'^addcustomer', CustomerActionClass.as_view(), name='CustomerActionClass'),
	url(r'^addrewards', CustomerActionClass.as_view(), name='CustomerActionClass'),
	url(r'^deletereward', CustomerActionClass.as_view(), name='CustomerActionClass'),
	url(r'^acrm', CRMViewClass.as_view(), name='crm'),



    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
