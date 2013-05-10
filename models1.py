# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Customers(models.Model):
    contactid = models.IntegerField(primary_key=True)
    billing_firstname = models.CharField(max_length=150, blank=True)
    billing_lastname = models.CharField(max_length=150, blank=True)
    billing_address = models.CharField(max_length=765, blank=True)
    billing_address2 = models.CharField(max_length=150, blank=True)
    billing_city = models.CharField(max_length=300, blank=True)
    billing_state = models.CharField(max_length=300, blank=True)
    billing_zip = models.CharField(max_length=60, blank=True)
    billing_country = models.CharField(max_length=300, blank=True)
    billing_company = models.CharField(max_length=765, blank=True)
    billing_phone = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=300, blank=True)
    shipping_firstname = models.CharField(max_length=150, blank=True)
    shipping_lastname = models.CharField(max_length=150, blank=True)
    shipping_address = models.CharField(max_length=765, blank=True)
    shipping_address2 = models.CharField(max_length=150, blank=True)
    shipping_city = models.CharField(max_length=300, blank=True)
    shipping_state = models.CharField(max_length=300, blank=True)
    shipping_zip = models.CharField(max_length=60, blank=True)
    shipping_country = models.CharField(max_length=300, blank=True)
    shipping_company = models.CharField(max_length=765, blank=True)
    shipping_phone = models.CharField(max_length=150, blank=True)
    comments = models.CharField(max_length=765, blank=True)
    lastlogindate = models.DateTimeField(null=True, blank=True)
    website = models.CharField(max_length=600, blank=True)
    pass_field = models.CharField(max_length=150, db_column='pass', blank=True) # Field renamed because it was a Python reserved word.
    discount = models.FloatField(null=True, blank=True)
    custother1 = models.CharField(max_length=300, blank=True)
    accountno = models.CharField(max_length=150, blank=True)
    maillist = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    custenabled = models.IntegerField(null=True, blank=True)
    additional_field1 = models.CharField(max_length=750, blank=True)
    additional_field2 = models.CharField(max_length=750, blank=True)
    additional_field3 = models.CharField(max_length=450, blank=True)
    additional_field4 = models.CharField(max_length=450, blank=True)
    alt_contactid = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'_customers'

class SwfCreditPromotionsReconciliation(models.Model):
    last_run = models.DateTimeField(primary_key=True, db_column='Last_Run') # Field name made lowercase.
    class Meta:
        db_table = u'_swf_credit_promotions_reconciliation'

class SwfPromotionsForCleanup(models.Model):
    id = models.FloatField(null=True, blank=True)
    promotion_name = models.CharField(max_length=765, blank=True)
    promotion_description = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'_swf_promotions_for_cleanup'

class Adminpages(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.CharField(max_length=150, db_column='Page', blank=True) # Field name made lowercase.
    action = models.CharField(max_length=75, db_column='Action', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'adminpages'

class Adminpermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.IntegerField(null=True, blank=True)
    permission = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'adminpermissions'

class Admins(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150, blank=True)
    pass_field = models.CharField(max_length=150, db_column='pass', blank=True) # Field renamed because it was a Python reserved word.
    userlevel = models.IntegerField(null=True, blank=True)
    permissions = models.TextField(blank=True)
    ip_restricted = models.CharField(max_length=150, blank=True)
    lastlogin = models.DateTimeField(null=True, blank=True)
    lastchange = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=765, blank=True)
    usersession = models.CharField(max_length=96, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    terms_accepted = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=150, blank=True)
    resetpasskey = models.CharField(max_length=150, blank=True)
    resetpassexp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'admins'

class Adminsrma(models.Model):
    id = models.IntegerField(primary_key=True)
    vpassword = models.CharField(max_length=192, db_column='vPassword') # Field name made lowercase.
    dcreated = models.DateTimeField(db_column='dCreated') # Field name made lowercase.
    class Meta:
        db_table = u'adminsrma'

class AffAffiliates(models.Model):
    aff_id = models.IntegerField(primary_key=True, db_column='AFF_Id') # Field name made lowercase.
    aff_customerid = models.IntegerField(db_column='AFF_CustomerID') # Field name made lowercase.
    aff_commission = models.DecimalField(decimal_places=2, max_digits=7, db_column='AFF_Commission') # Field name made lowercase.
    aff_siteurl = models.CharField(max_length=600, db_column='AFF_SiteUrl', blank=True) # Field name made lowercase.
    aff_active = models.IntegerField(db_column='AFF_Active') # Field name made lowercase.
    aff_registerdate = models.DateTimeField(db_column='AFF_RegisterDate') # Field name made lowercase.
    aff_comments = models.TextField(db_column='AFF_Comments', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'aff_affiliates'

class AfpAffiliatespayments(models.Model):
    afp_id = models.IntegerField(primary_key=True, db_column='AFP_Id') # Field name made lowercase.
    aff_id = models.IntegerField(null=True, db_column='AFF_Id', blank=True) # Field name made lowercase.
    afp_date = models.DateTimeField(db_column='AFP_Date') # Field name made lowercase.
    afp_amount = models.DecimalField(decimal_places=2, max_digits=10, db_column='AFP_Amount') # Field name made lowercase.
    afp_checknum = models.CharField(max_length=150, db_column='AFP_CheckNum', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'afp_affiliatespayments'

class ApiSettings(models.Model):
    enabled = models.IntegerField(null=True, blank=True)
    userkey = models.CharField(max_length=150, blank=True)
    adminid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'api_settings'

class ApiSettingsIp(models.Model):
    id = models.IntegerField(primary_key=True)
    ipaddress = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'api_settings_ip'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=240, unique=True)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type = models.ForeignKey(DjangoContentType)
    codename = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=90, unique=True)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    idxf_username_l_iexact = models.CharField(max_length=90, blank=True)
    idxf_email_l_iexact = models.CharField(max_length=225, blank=True)
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_user_user_permissions'

class Autoemail(models.Model):
    id = models.IntegerField(primary_key=True)
    enabled = models.CharField(max_length=150, blank=True)
    sendtime = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=765, blank=True)
    message = models.TextField(blank=True)
    html = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'autoemail'

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=450, blank=True)
    category_description = models.TextField(blank=True)
    category_main = models.IntegerField()
    category_parent = models.IntegerField(null=True, blank=True)
    category_header = models.TextField(blank=True)
    category_footer = models.TextField(blank=True)
    category_title = models.TextField(blank=True)
    category_meta = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    numtolist = models.IntegerField(null=True, blank=True)
    displaytype = models.IntegerField(null=True, blank=True)
    columnum = models.IntegerField(null=True, blank=True)
    iconimage = models.CharField(max_length=300, blank=True)
    special_numtolist = models.IntegerField(null=True, blank=True)
    special_displaytype = models.IntegerField(null=True, blank=True)
    special_columnum = models.IntegerField(null=True, blank=True)
    category_columnum = models.IntegerField(null=True, blank=True)
    category_displaytype = models.IntegerField(null=True, blank=True)
    related_displaytype = models.IntegerField(null=True, blank=True)
    related_columnum = models.IntegerField(null=True, blank=True)
    listing_displaytype = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    category_defaultsorting = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    itemicon = models.IntegerField(null=True, blank=True)
    redirectto = models.CharField(max_length=450, blank=True)
    accessgroup = models.CharField(max_length=750, blank=True)
    link = models.TextField(blank=True)
    link_target = models.CharField(max_length=150, blank=True)
    upsellitems_displaytype = models.IntegerField(null=True, blank=True)
    upsellitems_columnum = models.IntegerField(null=True, blank=True)
    filename = models.CharField(max_length=765, blank=True)
    isfilter = models.IntegerField(null=True, db_column='isFilter', blank=True) # Field name made lowercase.
    keywords = models.TextField(blank=True)
    class Meta:
        db_table = u'category'

class CategoryFilter(models.Model):
    categoryid = models.IntegerField(primary_key=True)
    categoryfilterid = models.IntegerField(primary_key=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'category_filter'

class CategorySorting(models.Model):
    id = models.IntegerField(primary_key=True)
    sortingid = models.IntegerField(null=True, blank=True)
    sortingdefinition = models.CharField(max_length=150, blank=True)
    sortingtext = models.CharField(max_length=150, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    sortingorder = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'category_sorting'

class CheckoutQuestions(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.TextField(db_column='Question', blank=True) # Field name made lowercase.
    answers = models.TextField(db_column='Answers', blank=True) # Field name made lowercase.
    qtype = models.CharField(max_length=30, blank=True)
    featurerequired = models.IntegerField(null=True, blank=True)
    checkoutstep = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'checkout_questions'

class CompanyInfo(models.Model):
    email = models.CharField(max_length=750, blank=True)
    company = models.TextField(blank=True)
    address1 = models.CharField(max_length=765, blank=True)
    address2 = models.CharField(max_length=765, blank=True)
    city = models.CharField(max_length=600, blank=True)
    state = models.CharField(max_length=150, blank=True)
    zip = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    phone1 = models.CharField(max_length=150, blank=True)
    phone2 = models.CharField(max_length=150, blank=True)
    fax = models.CharField(max_length=150, blank=True)
    url = models.TextField(blank=True)
    invoice_terms = models.TextField(blank=True)
    invoicelogo = models.TextField(blank=True)
    wizard = models.IntegerField(null=True, blank=True)
    last_recurring_check = models.DateTimeField(null=True, blank=True)
    advopt_limit = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'company_info'

class Creditcards(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'creditcards'

class DiscountGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    groupname = models.CharField(max_length=450, db_column='GroupName', blank=True) # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True) # Field name made lowercase.
    value = models.IntegerField(null=True, db_column='Value', blank=True) # Field name made lowercase.
    ispercent = models.IntegerField(null=True, db_column='Ispercent', blank=True) # Field name made lowercase.
    minimumorder = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    link = models.CharField(max_length=750, blank=True)
    group_field1 = models.CharField(max_length=450, blank=True)
    group_field2 = models.CharField(max_length=450, blank=True)
    group_field3 = models.CharField(max_length=450, blank=True)
    price_level = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    allow_registration = models.IntegerField(null=True, blank=True)
    registration_message = models.TextField(blank=True)
    autoapprove = models.IntegerField(null=True, blank=True)
    thankyoupage = models.CharField(max_length=750, blank=True)
    emailto = models.CharField(max_length=450, blank=True)
    email_message = models.TextField(blank=True)
    registration_form = models.IntegerField(null=True, blank=True)
    nontaxable = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'discount_group'

class Distributor(models.Model):
    id = models.IntegerField(primary_key=True)
    company = models.CharField(max_length=150, blank=True)
    contact = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=150, blank=True)
    address2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    zip = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=150, blank=True)
    fax = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=765, blank=True)
    comments = models.TextField(blank=True)
    isdropshipper = models.IntegerField(null=True, blank=True)
    emailsubject = models.CharField(max_length=750, blank=True)
    emailmessage = models.TextField(blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    iswarehouse = models.IntegerField(null=True, blank=True)
    generateslabel = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'distributor'

class DistributorShiptolist(models.Model):
    id = models.IntegerField(primary_key=True)
    distributorid = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=6, blank=True)
    statecode = models.CharField(max_length=150, blank=True)
    statename = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'distributor_shiptolist'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey(DjangoContentType, null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    idxf_object_id_l_exact = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(max_length=300, unique=True)
    model = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class Emails(models.Model):
    id = models.IntegerField()
    etype = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    to = models.CharField(max_length=150, blank=True)
    order_status = models.IntegerField(null=True, blank=True)
    body_html = models.TextField(blank=True)
    from_email = models.CharField(max_length=765, blank=True)
    reply_email = models.CharField(max_length=765, blank=True)
    bcc_email = models.CharField(max_length=765, blank=True)
    section = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'emails'

class EproductLogins(models.Model):
    id = models.IntegerField(primary_key=True)
    productid = models.IntegerField(null=True, blank=True)
    pass_field = models.CharField(max_length=150, db_column='pass', blank=True) # Field renamed because it was a Python reserved word.
    expiration = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'eproduct_logins'

class EproductSerial(models.Model):
    id = models.IntegerField(primary_key=True)
    productid = models.IntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=150, blank=True)
    oitemid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eproduct_serial'

class ErrorMessages(models.Model):
    id = models.IntegerField(primary_key=True)
    error_name = models.CharField(max_length=150, blank=True)
    error_message = models.TextField(blank=True)
    error_number = models.IntegerField(null=True, blank=True)
    error_returnpage = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'error_messages'

class Extrapages(models.Model):
    id = models.IntegerField()
    htmlpage = models.CharField(max_length=750, blank=True)
    title = models.TextField(blank=True)
    meta = models.TextField(blank=True)
    content = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    link = models.TextField(blank=True)
    link_target = models.CharField(max_length=150, blank=True)
    page_parent = models.IntegerField(null=True, blank=True)
    isdatabase = models.IntegerField(null=True, blank=True)
    recordsperpage = models.IntegerField(null=True, blank=True)
    page_displaytype = models.IntegerField(null=True, blank=True)
    showindex = models.IntegerField(null=True, blank=True)
    showrss = models.IntegerField(null=True, blank=True)
    feed_sorting = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    accessgroup = models.IntegerField(null=True, blank=True)
    redirectto = models.CharField(max_length=450, blank=True)
    filename = models.CharField(max_length=765, blank=True)
    hide_left = models.IntegerField(null=True, blank=True)
    hide_right = models.IntegerField(null=True, blank=True)
    frame_displaytype = models.IntegerField(null=True, blank=True)
    keywords = models.TextField(blank=True)
    class Meta:
        db_table = u'extrapages'

class SwfCustomerCreditsTracking(models.Model):
    id = models.IntegerField()
    customers_email_address = models.CharField(max_length=765)
    customers_credit = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    customers_promocode = models.CharField(max_length=765, blank=True)
    customers_credit_type = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'swf_customer_credits_tracking'

class SwfProductSortTemp(models.Model):
    id = models.IntegerField(primary_key=True)
    product_category_id = models.IntegerField()
    product_category_sorting = models.IntegerField()
    class Meta:
        db_table = u'swf_product_sort_temp'

class Tax(models.Model):
    id = models.IntegerField(primary_key=True)
    tax_country = models.CharField(max_length=150, blank=True)
    tax_state = models.CharField(max_length=150, blank=True)
    tax_value1 = models.FloatField(null=True, blank=True)
    tax_value2 = models.FloatField(null=True, blank=True)
    tax_value3 = models.FloatField(null=True, blank=True)
    tax_shipping = models.IntegerField(null=True, blank=True)
    tax_discount = models.IntegerField(null=True, blank=True)
    tax_code = models.CharField(max_length=9, blank=True)
    tax_zip_low = models.IntegerField(null=True, blank=True)
    tax_zip_high = models.IntegerField(null=True, blank=True)
    tax2includeprev = models.IntegerField(null=True, blank=True)
    tax3includeprev = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'tax'

class Template(models.Model):
    template = models.CharField(max_length=150, blank=True)
    stylesheet = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'template'

class Transactions(models.Model):
    id = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    ttype = models.CharField(max_length=30, blank=True)
    transactionid = models.CharField(max_length=150, blank=True)
    cvv2 = models.CharField(max_length=765, blank=True)
    avs = models.CharField(max_length=765, blank=True)
    responsetext = models.TextField(blank=True)
    approvalcode = models.CharField(max_length=150, blank=True)
    responsecode = models.CharField(max_length=150, blank=True)
    amount = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    gwid = models.IntegerField(null=True, blank=True)
    captured = models.IntegerField(null=True, blank=True)
    paymenttype = models.CharField(max_length=765, blank=True)
    reference = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'transactions'

class WshWishlist(models.Model):
    wsh_id = models.IntegerField(primary_key=True, db_column='WSH_Id') # Field name made lowercase.
    customerid = models.IntegerField()
    wsh_name = models.CharField(max_length=150, db_column='WSH_Name', blank=True) # Field name made lowercase.
    wsh_created = models.DateTimeField(db_column='WSH_Created') # Field name made lowercase.
    wsh_lastmod = models.DateTimeField(null=True, db_column='WSH_LastMod', blank=True) # Field name made lowercase.
    wsh_expiration = models.DateTimeField(null=True, db_column='WSH_Expiration', blank=True) # Field name made lowercase.
    wsh_eventdate = models.DateTimeField(null=True, db_column='WSH_EventDate', blank=True) # Field name made lowercase.
    wsh_password = models.CharField(max_length=30, db_column='WSH_Password', blank=True) # Field name made lowercase.
    wsh_message = models.TextField(db_column='WSH_Message', blank=True) # Field name made lowercase.
    wsh_shipmyaddress = models.IntegerField(null=True, db_column='WSH_ShipMyAddress', blank=True) # Field name made lowercase.
    customeraddressid = models.IntegerField(null=True, db_column='CustomerAddressId', blank=True) # Field name made lowercase.
    wsh_giftregistry = models.IntegerField(null=True, db_column='WSH_GiftRegistry', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'wsh_wishlist'

