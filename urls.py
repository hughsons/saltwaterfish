from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.defaults import *
from django.contrib import admin
from views import *
from auth_views import *
from user_actions import *
from admin.admin_actions import *
from admin.views import *
from murthy_views import *

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
	url(r'^mywishlist', MyWishListViewClass.as_view(), name='MyWishList'),
    url(r'^addtowatchlist', AddToWatchActionClass.as_view(), name='AddToWathList'),
    url(r'^deletewishlist', DeleteWishListActionClass.as_view(), name='AddToWathList'),
    url(r'^wishlistitems', WishListItemsViewClass.as_view(), name='WishListItems'),
    url(r'^deletecartitem', DeleteCartItemActionClass.as_view(), name='DeleteCartItem'),
	url(r'^checkoutlogin', CheckOutLoginViewClass.as_view(), name = 'CheckoutLogin'),
	url(r'^orderconfirmation', OrderConfirmationView.as_view(), name = 'OrderConfirmation'),

	url(r'^updateguestaddress', UpdateAddressInSession.as_view(), name='UpdateAddressInSession'),
	url(r'^commitorder', CommitOrderActionClass.as_view(), name = 'OommitOrder'),
	url(r'^guestlogin', GuestLoginActionClass.as_view(), name = 'GuestLogin'),
    url(r'^checkoutcallback', CheckOutCallBackViewClass.as_view(), name = 'PurchaseConfirmation'),
    url(r'^paypalredirection', PaypalRedirectionViewClass.as_view(), name = 'PaypalRedirection'),
    url(r'^applystorecredit', CartActionsClass.as_view(), name = 'ApplyStoreCredit'),
    url(r'^murthytest', MurthyTestViewCalss.as_view(), name = 'MurthyTest'),
    #url(r'^testradio', RadioButtonTest.as_view(), name='RadioButtonTest'),
    url(r'shippingcalander', ShippingCalander.as_view(), name="ShippingCalander"),
	url(r'buygift', GiftCertificateView.as_view(), name = 'GiftCertificateView'),
	url(r'AddReefPackages', AddReefPackagesActionClass.as_view(), name='AddReefPackages'),
	url(r'paypalcheckout', PaypalCheckoutAction.as_view(), name='checkout'),
	url(r'paypalcallback', PaypalCallBackView.as_view(), name='PaypalCallBack'),
	url(r'fedexlocations', FedexLocationsViewClass.as_view(), name='FedexLocations'),
	url(r'ordersummary', OrderSummaryViewClass.as_view(), name='OrderSummary'),
	url(r'updateshipping', UpdateShippingActionClass.as_view(), name='UpdateShippingCharge'),
	url(r'setshippingaddress', SetShippingActionClass.as_view(), name='SetShippingAddress'),
    

# Murthy URLS ENDS HERE	

# Simon URLS FRONT END HERE
	url(r'^quicklist', QuickListClass.as_view(), name='quicklist'),
	url(r'^category', ViewCategoryClass.as_view(), name='maincategory'),
	url(r'^pages', ViewPagesClass.as_view(), name='pages'),
	url(r'^productindex', ProductIndexClass.as_view(), name='ProductIndexClass'),
	url(r'^categoriesindex', CategoryIndexClass.as_view(), name='CategoryIndexClass'),
	url(r'^addrequest', AddRequestFormClass.as_view(), name='AddRequestFormClass'),
	url(r'^editrequestform', EditRequestFormClass.as_view(), name='EditRequestFormClass'),
	url(r'^generalactions', GeneralActionClass.as_view(), name='GeneralActionClass'),
	url(r'^freegeneralactions', FreeGeneralActionClass.as_view(), name='FreeGeneralActionClass'),
	url(r'^ordertracking', MyOrdersViewClass.as_view(), name='MyOrdersViewClass'),
	url(r'^orderstatus', MyOrdersViewClass.as_view(), name='MyOrdersViewClass'),
	url(r'^mytickets', MyTicketsViewClass.as_view(), name='MyTicketsViewClass'),
	url(r'^myreefs', MyRewardsViewClass.as_view(), name='MyRewardsViewClass'),
	url(r'^rmaservice', MyGuaranteedRequestsViewClass.as_view(), name='MyGuaranteedRequestsViewClass'),
	url(r'^contactus', ContactUsViewClass.as_view(), name='ContactUsViewClass'),
	url(r'^termsconditions', TermsConViewClass.as_view(), name='TermsConViewClass'),
	url(r'^reefpackages', ReefPackageViewClass.as_view(), name='ReefPackageViewClass'),
	url(r'^waitpopup', WaitingPopupViewClass.as_view(), name='WaitingPopupViewClass'),
	url(r'^emailfriendpopup', EmailFriendPopupViewClass.as_view(), name='EmailFriendPopupViewClass'),
	url(r'^product', ProductInfoViewClass.as_view(), name='ProductInfoViewClass'),
	url(r'^orderinfo', OrderInfoViewClass.as_view(), name='OrderInfoViewClass'),
	url(r'^printorder', PrintOrderInfoViewClass.as_view(), name='PrintOrderInfoViewClass'),
	url(r'^rmarequest', RMARequestViewClass.as_view(), name='RMARequestViewClass'),
	url(r'^addrma', RMARequestAddClass.as_view(), name='RMARequestAddClass'),
	url(r'^emailfriendpost', EmailToFriendActionClass.as_view(), name='EmailToFriendActionClass'),
	url(r'^onsale', ViewCategoryOnSaleClass.as_view(), name='onsalecats'),
	url(r'^giftcert', GiftCertViewClass.as_view(), name='GiftCertViewClass'),
	url(r'^sitemap', SitemapViewClass.as_view(), name='SitemapViewClass'),
	url(r'^search', SearchViewClass.as_view(), name='SearchViewClass'),
	url(r'^addressbook', AddressBookViewClass.as_view(), name='MyOrdersViewClass'),
	url(r'^addaddressbook', AddAddressBookViewClass.as_view(), name='AddAddressBookViewClass'),
	url(r'^fishschool', FishSchoolViewClass.as_view(), name='FishSchoolViewClass'),
	url(r'^dupeproduct', ProductDupeInfoViewClass.as_view(), name='ProductInfoViewClass'),
	url(r'^noimageproduct', ProductDupeimagesViewClass.as_view(), name='ProductInfoViewClass'),
	url(r'^fullimage', FullImagePopupViewClass.as_view(), name='FullImagePopupViewClass'),
	url(r'^subcats', SubCategoryIndexClass.as_view(), name='SubCategoryIndexClass'),
	url(r'^writereviewpopup', WriteReviewPopupViewClass.as_view(), name='writereviewpopup'),
# Simon URLS HERE

    url(r'^apanel', ApanelViewClass.as_view(), name='apanel'),
    url(r'^customers', CustomersViewClass.as_view(), name='customers'),
	url(r'^aproducts', ProductsViewClass.as_view(), name='customers'),
	url(r'^aproductinfo', ProductViewClass.as_view(), name='productinfo'),
	url(r'^aproductrelated', ProductRelatedClass.as_view(), name='productinfo'),
	url(r'^aproductoptions', ProductOptionEditViewClass.as_view(), name='ProductOptionEditViewClass'),
	url(r'^aproductarticles', ProductArticleViewClass.as_view(), name='productinfo'),
	url(r'^aproductreviews', ProductReviewsViewClass.as_view(), name='productinfo'),
    url(r'^admins$', StaffViewClass.as_view(), name='admins'),
	url(r'^addadminsform', AddAdminsFormClass.as_view(), name='AddAdminsFormClass'),
    url(r'^categories$', CategoryViewClass.as_view(), name='categories'),
    url(r'^bcustomersinfo', CustomerInfoClass.as_view(), name='customersinfo'),
	url(r'^baddcustomer', CustomerAddFormClass.as_view(), name='customersinfo'),
    url(r'^cmspages', CMSClass.as_view(), name='cmspages'),
	url(r'^titlesandcontent', TitlesContentClass.as_view(), name='cmspages'),
	url(r'^cmspageedit', CMSEditClass.as_view(), name='CMSEditClass'),
	url(r'^addcmsform', CMSAddFormClass.as_view(), name='addcmsform'),
	url(r'^aproduct_wish_list', ProductWishListClass.as_view(), name='product_wish_list'),
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
	url(r'^crmedit', CRMEditViewClass.as_view(), name='crmedit'),
	url(r'^crmactions', CRMActionClass.as_view(), name='CRMActionClass'),
	url(r'^aproductactions', ProductsctionClass.as_view(), name='ProductsctionClass'),
	url(r'^particleedit', ProductArticleEditViewClass.as_view(), name='ProductArticleEditViewClass'),
	url(r'^addprodarticle', ProductArticleAddFormClass.as_view(), name='ProductArticleAddFormClass'),
	url(r'^viewbanners', BannersViewClass.as_view(), name='BannersViewClass'),
	url(r'^editbanner', BannerEditViewClass.as_view(), name='BannerEditViewClass'),
	url(r'^addbannerform', BannersAddFormClass.as_view(), name='BannersAddFormClass'),
	url(r'^gcsfiles', GCSfilesClass.as_view(), name='BannersAddFormClass'),
	url(r'^couponmanager', CouponsViewClass.as_view(), name='CouponsViewClass'),
	url(r'^redreefs', ViewRedeemProductsClass.as_view(), name='ViewRedeemProductsClass'),
	url(r'^cuscreds', ViewRedeemProductsClass.as_view(), name='ViewRedeemProductsClass'),

    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
