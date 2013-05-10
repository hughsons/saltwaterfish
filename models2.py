# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

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
        db_table = u'_admins'

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
        db_table = u'_category'

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

class Crm(models.Model):
    id = models.IntegerField(primary_key=True)
    custid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    productid = models.IntegerField(null=True, blank=True)
    custemail = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=450, blank=True)
    datentime = models.DateTimeField(null=True, blank=True)
    assignedto = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    customer = models.CharField(max_length=150, blank=True)
    lastactiondatentime = models.DateTimeField(null=True, blank=True)
    messagekey = models.CharField(max_length=150, blank=True)
    departmentid = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'crm'

class CrmDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=150, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'crm_department'

class CrmMessages(models.Model):
    id = models.IntegerField(primary_key=True)
    crmid = models.IntegerField(null=True, blank=True)
    datentime = models.DateTimeField(null=True, blank=True)
    message = models.TextField(blank=True)
    sender = models.IntegerField(null=True, blank=True)
    sendername = models.CharField(max_length=150, blank=True)
    senderemail = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'crm_messages'

class CrmStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    statusid = models.IntegerField(null=True, blank=True)
    statustext = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'crm_status'

class CustomerRewards(models.Model):
    id = models.IntegerField(primary_key=True)
    contactid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    reference = models.CharField(max_length=150, blank=True)
    datentime = models.DateTimeField(null=True, blank=True)
    giftcertid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'customer_rewards'

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

class FileEditor(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.CharField(max_length=765, blank=True)
    datentime = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True)
    userid = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'file_editor'

class GcMapping(models.Model):
    id = models.IntegerField(primary_key=True)
    number_3did = models.IntegerField(null=True, db_column=u'3did', blank=True) # Field renamed because it wasn't a valid Python identifier.
    number_3dname = models.CharField(max_length=750, db_column=u'3dname', blank=True) # Field renamed because it wasn't a valid Python identifier.
    enabled = models.FloatField(null=True, blank=True)
    base_cost = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'gc_mapping'

class GiftCertUses(models.Model):
    id = models.IntegerField(primary_key=True)
    certificate_id = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    certificate_expense = models.FloatField(null=True, blank=True)
    used = models.IntegerField(null=True, blank=True)
    datentime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'gift_cert_uses'

class GiftCertificates(models.Model):
    id = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    certificate_name = models.CharField(max_length=450, blank=True)
    certificate_amount = models.FloatField(null=True, blank=True)
    certificate_expenses = models.FloatField(null=True, blank=True)
    certificate_balance = models.FloatField(null=True, blank=True)
    certificate_to = models.CharField(max_length=150, blank=True)
    certificate_message = models.TextField(blank=True)
    certificate_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'gift_certificates'

class HandlingRanges(models.Model):
    id = models.IntegerField(primary_key=True)
    range1 = models.FloatField(null=True, blank=True)
    range2 = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    ispercentage = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'handling_ranges'

class Html(models.Model):
    id = models.IntegerField()
    htmlpage = models.CharField(max_length=150, blank=True)
    title = models.TextField(blank=True)
    meta = models.TextField(blank=True)
    header = models.TextField(blank=True)
    footer = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    hide_left = models.IntegerField(null=True, blank=True)
    hide_right = models.IntegerField(null=True, blank=True)
    keywords = models.TextField(blank=True)
    class Meta:
        db_table = u'html'

class Icart(models.Model):
    icartversion = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'icart'

class ImportExport(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=150, blank=True)
    section = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    file = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'import_export'

class ImportExportFields(models.Model):
    id = models.IntegerField(primary_key=True)
    exportset = models.IntegerField(null=True, db_column='ExportSet', blank=True) # Field name made lowercase.
    fieldname = models.CharField(max_length=150, db_column='FieldName', blank=True) # Field name made lowercase.
    fieldalias = models.CharField(max_length=150, db_column='FieldAlias', blank=True) # Field name made lowercase.
    fieldprefix = models.CharField(max_length=450, db_column='FieldPrefix', blank=True) # Field name made lowercase.
    fieldsuffix = models.CharField(max_length=450, db_column='FieldSuffix', blank=True) # Field name made lowercase.
    fieldsorting = models.IntegerField(null=True, db_column='FieldSorting', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'import_export_fields'

class ImportExportSet(models.Model):
    id = models.IntegerField(primary_key=True)
    setname = models.CharField(max_length=150, db_column='SetName', blank=True) # Field name made lowercase.
    exporttype = models.IntegerField(null=True, db_column='ExportType', blank=True) # Field name made lowercase.
    paymentfilter = models.IntegerField(null=True, db_column='PaymentFilter', blank=True) # Field name made lowercase.
    shippingfilter = models.CharField(max_length=150, db_column='ShippingFilter', blank=True) # Field name made lowercase.
    datemodified = models.DateTimeField(null=True, db_column='DateModified', blank=True) # Field name made lowercase.
    usermodified = models.CharField(max_length=150, db_column='UserModified', blank=True) # Field name made lowercase.
    manufilter = models.IntegerField(null=True, db_column='ManuFilter', blank=True) # Field name made lowercase.
    distfilter = models.IntegerField(null=True, db_column='DistFilter', blank=True) # Field name made lowercase.
    catefilter = models.IntegerField(null=True, db_column='CateFilter', blank=True) # Field name made lowercase.
    delimiter = models.CharField(max_length=45, db_column='Delimiter', blank=True) # Field name made lowercase.
    catedelim = models.CharField(max_length=15, db_column='CateDelim', blank=True) # Field name made lowercase.
    hide = models.IntegerField(db_column='Hide') # Field name made lowercase.
    class Meta:
        db_table = u'import_export_set'

class InsuranceRanges(models.Model):
    id = models.IntegerField(primary_key=True)
    range1 = models.FloatField(null=True, blank=True)
    range2 = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    ispercentage = models.IntegerField(null=True, blank=True)
    required = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'insurance_ranges'

class InventoryLog(models.Model):
    id = models.IntegerField(primary_key=True)
    productid = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    prev_stock = models.IntegerField(null=True, blank=True)
    transaction_type = models.CharField(max_length=150, blank=True)
    log_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'inventory_log'

class Invoicenum(models.Model):
    invoicenum = models.IntegerField(null=True, blank=True)
    invoiceprefix = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'invoicenum'

class IpSecurity(models.Model):
    id = models.IntegerField(primary_key=True)
    range1 = models.CharField(max_length=48, blank=True)
    range2 = models.CharField(max_length=48, blank=True)
    class Meta:
        db_table = u'ip_security'

class Itemstemp(models.Model):
    oid = models.IntegerField()
    orderitemid = models.IntegerField()
    returned = models.IntegerField()
    class Meta:
        db_table = u'itemstemp'

class MailGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=150, blank=True)
    group_type = models.CharField(max_length=150, blank=True)
    table1 = models.TextField(blank=True)
    field1 = models.CharField(max_length=150, blank=True)
    comp1 = models.CharField(max_length=150, blank=True)
    value1 = models.CharField(max_length=150, blank=True)
    type1 = models.CharField(max_length=150, blank=True)
    field2 = models.CharField(max_length=150, blank=True)
    comp2 = models.CharField(max_length=150, blank=True)
    value2 = models.CharField(max_length=150, blank=True)
    type2 = models.CharField(max_length=150, blank=True)
    field3 = models.CharField(max_length=150, blank=True)
    comp3 = models.CharField(max_length=150, blank=True)
    value3 = models.CharField(max_length=150, blank=True)
    type3 = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'mail_groups'

class Manufacturer(models.Model):
    id = models.IntegerField(primary_key=True)
    manufacturer = models.CharField(max_length=150, blank=True)
    logo = models.CharField(max_length=150, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    header = models.TextField(blank=True)
    website = models.CharField(max_length=150, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'manufacturer'

class Menulinks(models.Model):
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
        db_table = u'menulinks'

class Newsletter(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=300, blank=True)
    datereg = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    zip = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    additional_field1 = models.CharField(max_length=750, blank=True)
    additional_field2 = models.CharField(max_length=750, blank=True)
    additional_field3 = models.CharField(max_length=750, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'newsletter'

class NewsletterBl(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=300, blank=True)
    datereg = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'newsletter_bl'

class NewsletterEmails(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    textmessage = models.TextField(blank=True)
    group = models.TextField(blank=True)
    class Meta:
        db_table = u'newsletter_emails'

class NewsletterGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    groupname = models.CharField(max_length=150, blank=True)
    groupdescription = models.TextField(blank=True)
    class Meta:
        db_table = u'newsletter_groups'

class Newsletters(models.Model):
    id = models.IntegerField(primary_key=True)
    newslettername = models.CharField(max_length=150, blank=True)
    newsletterbody = models.TextField(blank=True)
    newslettertext = models.TextField(blank=True)
    newslettersubject = models.CharField(max_length=765, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    newsletterreplyto = models.CharField(max_length=765, blank=True)
    newsletterfrom = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'newsletters'

class OfflinePayments(models.Model):
    id = models.IntegerField()
    payment_type = models.CharField(max_length=150, blank=True)
    payment_description = models.TextField(blank=True)
    payment_cost_modification = models.IntegerField(null=True, blank=True)
    payment_confirmation_message = models.TextField(blank=True)
    payment_hide = models.IntegerField(null=True, blank=True)
    payment_sort = models.IntegerField(null=True, blank=True)
    discountgroup = models.IntegerField(null=True, blank=True)
    lowerol = models.IntegerField(null=True, db_column='LowerOL', blank=True) # Field name made lowercase.
    upperol = models.IntegerField(null=True, db_column='UpperOL', blank=True) # Field name made lowercase.
    paymentcountry = models.CharField(max_length=150, db_column='PaymentCountry', blank=True) # Field name made lowercase.
    paymentstate = models.CharField(max_length=150, db_column='PaymentState', blank=True) # Field name made lowercase.
    payment_status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'offline_payments'

class OfflinePaymentsFields(models.Model):
    id = models.IntegerField(primary_key=True)
    payment_id = models.IntegerField()
    inputname = models.CharField(max_length=150, db_column='InputName') # Field name made lowercase.
    inputlength = models.IntegerField(db_column='InputLength') # Field name made lowercase.
    required = models.IntegerField(db_column='Required') # Field name made lowercase.
    hide = models.IntegerField(db_column='Hide') # Field name made lowercase.
    sortorder = models.IntegerField(db_column='SortOrder') # Field name made lowercase.
    inputremotename = models.CharField(max_length=150, db_column='InputRemoteName') # Field name made lowercase.
    inputdefault = models.CharField(max_length=300, db_column='InputDefault') # Field name made lowercase.
    inputtype = models.CharField(max_length=150, db_column='InputType') # Field name made lowercase.
    class Meta:
        db_table = u'offline_payments_fields'

class Oitems(models.Model):
    orderitemid = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    itemid = models.CharField(max_length=450, blank=True)
    itemname = models.TextField(blank=True)
    numitems = models.FloatField(null=True, blank=True)
    unitprice = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    options = models.TextField(blank=True)
    optionprice = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    additional_field1 = models.CharField(max_length=150, blank=True)
    additional_field2 = models.CharField(max_length=150, blank=True)
    additional_field3 = models.CharField(max_length=150, blank=True)
    shipment_id = models.IntegerField(null=True, blank=True)
    catoptions = models.CharField(max_length=765, blank=True)
    catalogidoptions = models.CharField(max_length=765, blank=True)
    warehouseid = models.IntegerField(null=True, db_column='warehouseID', blank=True) # Field name made lowercase.
    unitcost = models.FloatField(null=True, blank=True)
    unitstock = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    page_added = models.CharField(max_length=765, blank=True)
    itemdescription = models.CharField(max_length=450, blank=True)
    reminder = models.IntegerField(null=True, blank=True)
    recurrent = models.IntegerField(null=True, blank=True)
    wsh_id = models.IntegerField(null=True, blank=True)
    wsi_id = models.IntegerField(null=True, blank=True)
    depends_on_item = models.IntegerField(null=True, blank=True)
    recurring_order_frequency = models.IntegerField(null=True, blank=True)
    item_type = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'oitems'

class OitemsGiftcertificates(models.Model):
    id = models.IntegerField(primary_key=True)
    orderitemid = models.IntegerField(null=True, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    gc_toname = models.CharField(max_length=765, blank=True)
    gc_toemail = models.CharField(max_length=765, blank=True)
    gc_tomessage = models.TextField(blank=True)
    gc_fromname = models.CharField(max_length=765, blank=True)
    gc_id = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'oitems_giftcertificates'

class OnlinePayments(models.Model):
    id = models.IntegerField()
    payment_id = models.IntegerField(null=True, blank=True)
    payment_description = models.TextField(blank=True)
    payment_confirmation_message = models.TextField(blank=True)
    payment_hide = models.IntegerField(null=True, blank=True)
    payment_sort = models.IntegerField(null=True, blank=True)
    payment_login = models.CharField(max_length=150, blank=True)
    payment_password = models.CharField(max_length=765, blank=True)
    payment_url = models.CharField(max_length=150, blank=True)
    authorizeonly = models.IntegerField(null=True, blank=True)
    lowerol = models.IntegerField(null=True, db_column='LowerOL', blank=True) # Field name made lowercase.
    upperol = models.IntegerField(null=True, db_column='UpperOL', blank=True) # Field name made lowercase.
    enabled = models.IntegerField(null=True, db_column='Enabled', blank=True) # Field name made lowercase.
    usage = models.IntegerField(null=True, blank=True)
    paymentcountry = models.CharField(max_length=150, db_column='PaymentCountry', blank=True) # Field name made lowercase.
    paymentstate = models.CharField(max_length=150, db_column='PaymentState', blank=True) # Field name made lowercase.
    discountgroup = models.IntegerField(null=True, blank=True)
    payment_description_message = models.TextField(blank=True)
    payment_status = models.IntegerField(null=True, blank=True)
    payment_signature = models.CharField(max_length=765, blank=True)
    testmode = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'online_payments'

class OnlineShipping(models.Model):
    id = models.IntegerField()
    ups = models.IntegerField(null=True, blank=True)
    fedex = models.IntegerField(null=True, blank=True)
    dhl = models.IntegerField(null=True, blank=True)
    usps = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'online_shipping'

class OptionsAdvanced(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    productid = models.IntegerField(null=True, db_column='ProductID', blank=True) # Field name made lowercase.
    ao_code = models.CharField(max_length=150, db_column='AO_Code', blank=True) # Field name made lowercase.
    ao_sufix = models.CharField(max_length=150, db_column='AO_Sufix', blank=True) # Field name made lowercase.
    ao_name = models.TextField(db_column='AO_Name', blank=True) # Field name made lowercase.
    ao_cost = models.FloatField(null=True, db_column='AO_Cost', blank=True) # Field name made lowercase.
    ao_stock = models.FloatField(null=True, db_column='AO_Stock', blank=True) # Field name made lowercase.
    ao_weight = models.FloatField(null=True, db_column='AO_Weight', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'options_advanced'

class Optionstemplate(models.Model):
    id = models.IntegerField(primary_key=True)
    featurename = models.CharField(max_length=150, blank=True)
    featurecaption = models.CharField(max_length=150, blank=True)
    featuretype = models.CharField(max_length=30, blank=True)
    featurerequired = models.IntegerField(null=True, blank=True)
    optionname = models.CharField(max_length=150, blank=True)
    optionprice = models.IntegerField(null=True, blank=True)
    optionsorting = models.IntegerField(null=True, blank=True)
    optionspartnum = models.CharField(max_length=60, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'optionstemplate'

class OrderDiscounts(models.Model):
    id = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    discount_id = models.IntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    discount_freeship = models.IntegerField(null=True, blank=True)
    discount_freeprod = models.CharField(max_length=150, blank=True)
    coupon = models.CharField(max_length=150, blank=True)
    freeprod = models.IntegerField(null=True, blank=True)
    giftcert = models.IntegerField(null=True, blank=True)
    applied = models.DateTimeField(null=True, blank=True)
    promo_amount = models.FloatField(null=True, blank=True)
    promo_qty = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'order_discounts'

class OrderQuestions(models.Model):
    id = models.IntegerField(primary_key=True)
    questionid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    answer = models.TextField(blank=True)
    class Meta:
        db_table = u'order_questions'

class OrderStatus(models.Model):
    id = models.IntegerField()
    statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) # Field name made lowercase.
    statusdefinition = models.CharField(max_length=150, db_column='StatusDefinition', blank=True) # Field name made lowercase.
    statustext = models.CharField(max_length=150, db_column='StatusText', blank=True) # Field name made lowercase.
    visible = models.IntegerField(null=True, db_column='Visible', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'order_status'

class Orders(models.Model):
    orderid = models.IntegerField(primary_key=True)
    ocustomerid = models.IntegerField(null=True, blank=True)
    odate = models.DateTimeField(null=True, blank=True)
    orderamount = models.FloatField(null=True, blank=True)
    ofirstname = models.CharField(max_length=300, blank=True)
    olastname = models.CharField(max_length=300, blank=True)
    oemail = models.CharField(max_length=300, blank=True)
    oaddress = models.CharField(max_length=600, blank=True)
    oaddress2 = models.CharField(max_length=150, blank=True)
    ocity = models.CharField(max_length=300, blank=True)
    ozip = models.CharField(max_length=45, blank=True)
    ostate = models.CharField(max_length=300, blank=True)
    ocountry = models.CharField(max_length=150, blank=True)
    ophone = models.CharField(max_length=90, blank=True)
    ofax = models.CharField(max_length=90, blank=True)
    ocompany = models.CharField(max_length=765, blank=True)
    ocardtype = models.CharField(max_length=150, blank=True)
    ocardno = models.CharField(max_length=765, blank=True)
    ocardname = models.CharField(max_length=600, blank=True)
    ocardexpiresmonth = models.CharField(max_length=30, blank=True)
    ocardexpiresyear = models.CharField(max_length=30, blank=True)
    ocardissuenum = models.CharField(max_length=30, blank=True)
    ocardstartmonth = models.CharField(max_length=30, blank=True)
    ocardstartyear = models.CharField(max_length=30, blank=True)
    ocardaddress = models.CharField(max_length=450, blank=True)
    ocardverification = models.CharField(max_length=150, blank=True)
    oprocessed = models.IntegerField()
    ocomment = models.TextField(blank=True)
    otax = models.FloatField(null=True, blank=True)
    otax2 = models.FloatField(null=True, blank=True)
    otax3 = models.FloatField(null=True, blank=True)
    ointernalcomment = models.TextField(blank=True)
    oexternalcomment = models.CharField(max_length=150, blank=True)
    oshippeddate = models.CharField(max_length=150, blank=True)
    oshipmethod = models.CharField(max_length=450, blank=True)
    oshipcost = models.FloatField(null=True, blank=True)
    oshipfirstname = models.CharField(max_length=300, blank=True)
    oshiplastname = models.CharField(max_length=150, blank=True)
    oshipcompany = models.CharField(max_length=600, blank=True)
    oshipemail = models.CharField(max_length=300, blank=True)
    oshipaddress = models.CharField(max_length=765, blank=True)
    oshipaddress2 = models.CharField(max_length=150, blank=True)
    oshipcity = models.CharField(max_length=150, blank=True)
    oshipzip = models.CharField(max_length=60, blank=True)
    oshipstate = models.CharField(max_length=150, blank=True)
    oshipcountry = models.CharField(max_length=150, blank=True)
    oshipphone = models.CharField(max_length=150, blank=True)
    opaymethod = models.IntegerField(null=True, blank=True)
    opaymethodinfo = models.TextField(blank=True)
    status = models.IntegerField(null=True, blank=True)
    other2 = models.CharField(max_length=150, blank=True)
    otime = models.DateTimeField(null=True, blank=True)
    oauthorization = models.CharField(max_length=765, blank=True)
    oerrors = models.CharField(max_length=765, blank=True)
    odiscount = models.FloatField(null=True, blank=True)
    ostatus = models.CharField(max_length=765, blank=True)
    ohandling = models.FloatField(null=True, blank=True)
    coupon = models.CharField(max_length=300, blank=True)
    coupondiscount = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    coupondiscountdual = models.FloatField(null=True, blank=True)
    giftcertificate = models.CharField(max_length=300, blank=True)
    giftamountused = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    giftamountuseddual = models.FloatField(null=True, blank=True)
    trackingcode = models.CharField(max_length=300, blank=True)
    invoicenum_prefix = models.CharField(max_length=150, blank=True)
    invoicenum = models.IntegerField(null=True, blank=True)
    order_status = models.IntegerField(null=True, blank=True)
    referer = models.TextField(blank=True)
    salesperson = models.CharField(max_length=150, blank=True)
    ip = models.CharField(max_length=48, blank=True)
    date_started = models.DateTimeField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    last_auto_email = models.IntegerField(null=True, blank=True)
    oweight = models.FloatField(null=True, blank=True)
    oboxes = models.IntegerField(null=True, blank=True)
    orderkey = models.CharField(max_length=48, blank=True)
    ostep = models.CharField(max_length=150, blank=True)
    shipmethodid = models.IntegerField(null=True, blank=True)
    insured = models.IntegerField(null=True, blank=True)
    alt_orderid = models.CharField(max_length=150, blank=True)
    affiliate_id = models.IntegerField(null=True, blank=True)
    affiliate_commission = models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)
    affiliate_approved = models.IntegerField(null=True, blank=True)
    affiliate_approvedreason = models.CharField(max_length=150, blank=True)
    shipping_id = models.IntegerField(null=True, blank=True)
    buysafe = models.IntegerField(null=True, blank=True)
    checktype = models.CharField(max_length=24, blank=True)
    checkacctype = models.CharField(max_length=24, blank=True)
    checkrouting = models.CharField(max_length=150, blank=True)
    checkaccount = models.CharField(max_length=150, blank=True)
    oshipaddresstype = models.IntegerField(null=True, blank=True)
    isrecurrent = models.IntegerField(null=True, blank=True)
    recurrent_frequency = models.IntegerField(null=True, blank=True)
    parent_orderid = models.IntegerField(null=True, blank=True)
    last_order = models.DateTimeField(null=True, blank=True)
    next_order = models.DateTimeField(null=True, blank=True)
    customer_pmntprofileid = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'orders'

class OrdersLog(models.Model):
    id = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    log_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = u'orders_log'

class OrdersShipments(models.Model):
    id = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    address_id = models.IntegerField(null=True, blank=True)
    oshippeddate = models.CharField(max_length=150, blank=True)
    oshipmethod = models.CharField(max_length=450, blank=True)
    oshipmethodid = models.IntegerField(null=True, blank=True)
    oshipcost = models.FloatField(null=True, blank=True)
    trackingcode = models.CharField(max_length=300, blank=True)
    oshipalias = models.CharField(max_length=300, blank=True)
    oshipfirstname = models.CharField(max_length=300, blank=True)
    oshiplastname = models.CharField(max_length=150, blank=True)
    oshipcompany = models.CharField(max_length=600, blank=True)
    oshipemail = models.CharField(max_length=300, blank=True)
    oshipaddress = models.CharField(max_length=765, blank=True)
    oshipaddress2 = models.CharField(max_length=150, blank=True)
    oshipcity = models.CharField(max_length=150, blank=True)
    oshipzip = models.CharField(max_length=60, blank=True)
    oshipstate = models.CharField(max_length=150, blank=True)
    oshipcountry = models.CharField(max_length=150, blank=True)
    oshipphone = models.CharField(max_length=150, blank=True)
    order_status = models.IntegerField(null=True, blank=True)
    distributor_id = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    oweight = models.FloatField(null=True, blank=True)
    oboxes = models.IntegerField(null=True, blank=True)
    otax = models.FloatField(null=True, blank=True)
    ointernalcomment = models.TextField(blank=True)
    shipping_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'orders_shipments'

class OslOrdersshiplabel(models.Model):
    osl_id = models.IntegerField(primary_key=True, db_column='OSL_Id') # Field name made lowercase.
    orderid = models.IntegerField(db_column='OrderID') # Field name made lowercase.
    ordershipid = models.IntegerField(null=True, db_column='OrderShipId', blank=True) # Field name made lowercase.
    osl_carrier = models.CharField(max_length=30, db_column='OSL_Carrier') # Field name made lowercase.
    osl_tracking = models.CharField(max_length=150, db_column='OSL_Tracking') # Field name made lowercase.
    osl_imgtype = models.CharField(max_length=9, db_column='OSL_ImgType', blank=True) # Field name made lowercase.
    osl_date = models.DateTimeField(db_column='OSL_Date') # Field name made lowercase.
    osl_time = models.DateTimeField(db_column='OSL_Time') # Field name made lowercase.
    osl_voided = models.IntegerField(db_column='OSL_Voided') # Field name made lowercase.
    osl_voiddate = models.DateTimeField(null=True, db_column='OSL_VoidDate', blank=True) # Field name made lowercase.
    osl_voidtime = models.DateTimeField(null=True, db_column='OSL_VoidTime', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'osl_ordersshiplabel'

class PageMap(models.Model):
    id = models.IntegerField(primary_key=True)
    old_url = models.CharField(max_length=750, blank=True)
    new_url = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = u'page_map'

class PasteErrors(models.Model):
    id = models.IntegerField(null=True, blank=True)
    exportset = models.IntegerField(null=True, db_column='ExportSet', blank=True) # Field name made lowercase.
    fieldname = models.CharField(max_length=765, db_column='FieldName', blank=True) # Field name made lowercase.
    fieldalias = models.CharField(max_length=765, db_column='FieldAlias', blank=True) # Field name made lowercase.
    fieldprefix = models.CharField(max_length=765, db_column='FieldPrefix', blank=True) # Field name made lowercase.
    fieldsuffix = models.CharField(max_length=765, db_column='FieldSuffix', blank=True) # Field name made lowercase.
    fieldsorting = models.IntegerField(null=True, db_column='FieldSorting', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'paste errors'

class PaymentExcludelist(models.Model):
    id = models.IntegerField(primary_key=True)
    paymentid = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    online = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'payment_excludelist'

class PaymentFields(models.Model):
    id = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    input_id = models.IntegerField(null=True, blank=True)
    input_value = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = u'payment_fields'

class PaymentMethods(models.Model):
    id = models.IntegerField()
    gateway_id = models.IntegerField(null=True, db_column='gateway_ID', blank=True) # Field name made lowercase.
    payment_gateway = models.CharField(max_length=150, blank=True)
    ccgateway = models.IntegerField(null=True, db_column='CCGateway', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'payment_methods'

class Pickuptype(models.Model):
    idpickuptype = models.IntegerField(primary_key=True, db_column='idPickupType') # Field name made lowercase.
    pickuptype = models.CharField(max_length=150, db_column='PickupType', blank=True) # Field name made lowercase.
    pickuptypecode = models.IntegerField(null=True, db_column='PickupTypeCode', blank=True) # Field name made lowercase.
    shipid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pickuptype'

class PriceRange(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150, blank=True)
    low_range = models.FloatField(null=True, blank=True)
    high_range = models.FloatField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'price_range'

class Pricing(models.Model):
    id = models.IntegerField(primary_key=True)
    prod_id = models.IntegerField(null=True, blank=True)
    lowbound = models.IntegerField(null=True, blank=True)
    upbound = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    percentage = models.IntegerField()
    price_level = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pricing'

class ProdAddfeatures(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    productid = models.IntegerField(null=True, db_column='ProductID', blank=True) # Field name made lowercase.
    prodfeature = models.TextField(db_column='ProdFeature', blank=True) # Field name made lowercase.
    prodfeaturetitle = models.CharField(max_length=450, db_column='ProdFeatureTitle', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'prod_addfeatures'

class Prodfeatures(models.Model):
    id = models.IntegerField(primary_key=True)
    featurename = models.CharField(max_length=765, blank=True)
    featurecaption = models.CharField(max_length=765, blank=True)
    featuretype = models.CharField(max_length=30, blank=True)
    featuremulti = models.CharField(max_length=30, blank=True)
    featurerequired = models.IntegerField(null=True, blank=True)
    item_id = models.IntegerField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    template_id = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    url = models.TextField(blank=True)
    info = models.TextField(blank=True)
    class Meta:
        db_table = u'prodfeatures'

class ProdfeaturesOptions(models.Model):
    id = models.IntegerField(primary_key=True)
    caption_id = models.IntegerField(null=True, blank=True)
    featurename = models.CharField(max_length=765, blank=True)
    featureprice = models.FloatField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    partnumber = models.CharField(max_length=150, blank=True)
    imagepath = models.CharField(max_length=765, blank=True)
    selected = models.IntegerField(null=True, blank=True)
    hidden = models.IntegerField(null=True, blank=True)
    optcatalogid = models.IntegerField(null=True, blank=True)
    advopt_code = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'prodfeatures_options'

class ProductAccessories(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    accessory_id = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_accessories'

class ProductBoxes(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_boxes'

class ProductCategory(models.Model):
    id = models.IntegerField()
    catalogid = models.IntegerField(null=True, blank=True)
    categoryid = models.IntegerField(null=True, blank=True)
    ismain = models.CharField(max_length=150, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_category'

class ProductDistributor(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    distributorid = models.IntegerField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    itemid = models.CharField(max_length=150, blank=True)
    stockid = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_distributor'

class ProductEmailfriend(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=150, blank=True)
    user_email = models.CharField(max_length=150, blank=True)
    friend_name = models.CharField(max_length=150, blank=True)
    friend_email = models.CharField(max_length=450, blank=True)
    message = models.TextField(blank=True)
    record_date = models.DateTimeField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_emailfriend'

class ProductImages(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    image = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_images'

class ProductMap(models.Model):
    itemid = models.IntegerField(primary_key=True)
    oldid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_map'

class ProductRelated(models.Model):
    id = models.IntegerField()
    catalogid = models.IntegerField(null=True, blank=True)
    related_id = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_related'

class ProductReview(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=150, blank=True)
    user_email = models.CharField(max_length=150, blank=True)
    user_city = models.CharField(max_length=150, blank=True)
    short_review = models.CharField(max_length=450, blank=True)
    long_review = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    approved = models.IntegerField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_review'

class ProductShipping(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    shipcarriermethodid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_shipping'

class ProductWaitinglist(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=150, blank=True)
    user_email = models.CharField(max_length=150, blank=True)
    user_phone = models.CharField(max_length=150, blank=True)
    record_date = models.DateTimeField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    current_stock = models.IntegerField(null=True, blank=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'product_waitinglist'

class Products(models.Model):
    catalogid = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=765, blank=True)
    categoriesaaa = models.CharField(max_length=300, blank=True)
    mfgid = models.CharField(max_length=150, blank=True)
    manufacturer = models.IntegerField(null=True, blank=True)
    distributor = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price2 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price3 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    saleprice = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    onsale = models.IntegerField(null=True, blank=True)
    stock = models.FloatField(null=True, blank=True)
    stock_alert = models.IntegerField(null=True, blank=True)
    display_stock = models.CharField(max_length=150, blank=True)
    weight = models.FloatField(null=True, blank=True)
    minimumorder = models.FloatField(null=True, blank=True)
    maximumorder = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    extended_description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    thumbnail = models.CharField(max_length=765, blank=True)
    image1 = models.CharField(max_length=765, blank=True)
    image2 = models.CharField(max_length=765, blank=True)
    image3 = models.CharField(max_length=765, blank=True)
    image4 = models.CharField(max_length=765, blank=True)
    realmedia = models.CharField(max_length=765, blank=True)
    related = models.CharField(max_length=150, blank=True)
    shipcost = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    imagecaption1 = models.TextField(blank=True)
    imagecaption2 = models.TextField(blank=True)
    imagecaption3 = models.TextField(blank=True)
    imagecaption4 = models.TextField(blank=True)
    title = models.CharField(max_length=450, blank=True)
    metatags = models.TextField(blank=True)
    displaytext = models.CharField(max_length=150, blank=True)
    eproduct_password = models.CharField(max_length=45, blank=True)
    eproduct_random = models.IntegerField(null=True, blank=True)
    eproduct_expire = models.IntegerField(null=True, blank=True)
    eproduct_path = models.TextField(blank=True)
    eproduct_serial = models.IntegerField(null=True, blank=True)
    eproduct_instructions = models.TextField(blank=True)
    homespecial = models.IntegerField(null=True, blank=True)
    categoryspecial = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    free_shipping = models.IntegerField(null=True, blank=True)
    nontax = models.IntegerField(null=True, blank=True)
    notforsale = models.IntegerField(null=True, blank=True)
    giftcertificate = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    extra_field_1 = models.CharField(max_length=450, blank=True)
    extra_field_2 = models.CharField(max_length=450, blank=True)
    extra_field_3 = models.CharField(max_length=450, blank=True)
    extra_field_4 = models.CharField(max_length=450, blank=True)
    extra_field_5 = models.CharField(max_length=450, blank=True)
    extra_field_6 = models.TextField(blank=True)
    extra_field_7 = models.TextField(blank=True)
    extra_field_8 = models.TextField(blank=True)
    extra_field_9 = models.TextField(blank=True)
    extra_field_10 = models.TextField(blank=True)
    usecatoptions = models.IntegerField(null=True, blank=True)
    qtyoptions = models.CharField(max_length=750, blank=True)
    price_1 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_2 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_3 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_4 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_5 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_6 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_7 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_8 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_9 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    price_10 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    hide_1 = models.IntegerField(null=True, blank=True)
    hide_2 = models.IntegerField(null=True, blank=True)
    hide_3 = models.IntegerField(null=True, blank=True)
    hide_4 = models.IntegerField(null=True, blank=True)
    hide_5 = models.IntegerField(null=True, blank=True)
    hide_6 = models.IntegerField(null=True, blank=True)
    hide_7 = models.IntegerField(null=True, blank=True)
    hide_8 = models.IntegerField(null=True, blank=True)
    hide_9 = models.IntegerField(null=True, blank=True)
    hide_10 = models.IntegerField(null=True, blank=True)
    minorderpkg = models.IntegerField(null=True, blank=True)
    listing_displaytype = models.IntegerField(null=True, blank=True)
    show_out_stock = models.IntegerField(null=True, blank=True)
    pricing_groupopt = models.IntegerField(null=True, blank=True)
    qtydiscount_opt = models.IntegerField(null=True, blank=True)
    loginlevel = models.IntegerField(null=True, blank=True)
    redirectto = models.CharField(max_length=450, blank=True)
    accessgroup = models.CharField(max_length=750, blank=True)
    self_ship = models.IntegerField(null=True, blank=True)
    tax_code = models.CharField(max_length=9, blank=True)
    eproduct_reuseserial = models.FloatField(null=True, blank=True)
    nonsearchable = models.IntegerField(null=True, blank=True)
    instock_message = models.CharField(max_length=450, blank=True)
    outofstock_message = models.CharField(max_length=450, blank=True)
    backorder_message = models.CharField(max_length=450, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    reward_points = models.IntegerField(null=True, blank=True)
    reward_disable = models.IntegerField(null=True, blank=True)
    reward_redeem = models.IntegerField(null=True, blank=True)
    filename = models.CharField(max_length=765, blank=True)
    rma_maxperiod = models.IntegerField(null=True, blank=True)
    recurring_order = models.IntegerField(null=True, blank=True)
    fractional_qty = models.IntegerField(null=True, blank=True)
    reminders_enabled = models.IntegerField(null=True, blank=True)
    reminders_frequency = models.IntegerField(null=True, blank=True)
    review_average = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'products'

class Promotions(models.Model):
    id = models.IntegerField(primary_key=True)
    promotion_name = models.CharField(max_length=450, blank=True)
    promotion_description = models.TextField(blank=True)
    promotion_start = models.DateTimeField(null=True, blank=True)
    promotion_end = models.DateTimeField(null=True, blank=True)
    promotion_enabled = models.IntegerField(null=True, blank=True)
    by_amount = models.IntegerField(null=True, blank=True)
    chk_byamount = models.IntegerField(null=True, blank=True)
    by_quantity = models.IntegerField(null=True, blank=True)
    chk_byquantity = models.IntegerField(null=True, blank=True)
    by_product = models.IntegerField(null=True, blank=True)
    by_category = models.TextField(blank=True)
    promotion_amount = models.FloatField(null=True, blank=True)
    promotion_percentage = models.IntegerField(null=True, blank=True)
    promotion_peritem = models.IntegerField(null=True, blank=True)
    promotion_category = models.TextField(blank=True)
    promotion_product = models.CharField(max_length=450, blank=True)
    promotion_freeshipping = models.IntegerField(null=True, blank=True)
    promotion_freeproduct = models.CharField(max_length=450, blank=True)
    prod1_id = models.IntegerField(null=True, blank=True)
    prod1_qty = models.IntegerField(null=True, blank=True)
    prod2_id = models.IntegerField(null=True, blank=True)
    prod2_qty = models.IntegerField(null=True, blank=True)
    prod3_id = models.IntegerField(null=True, blank=True)
    prod3_qty = models.IntegerField(null=True, blank=True)
    prod4_id = models.IntegerField(null=True, blank=True)
    prod4_qty = models.IntegerField(null=True, blank=True)
    coupon = models.CharField(max_length=150, blank=True)
    promotion_uses = models.IntegerField(null=True, blank=True)
    promotion_maxuses = models.IntegerField(null=True, blank=True)
    promotion_usespercust = models.IntegerField(null=True, blank=True)
    coupon_group = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    by_amount2 = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    by_quantity2 = models.FloatField(null=True, blank=True)
    promotion_country = models.CharField(max_length=150, blank=True)
    promotion_state = models.CharField(max_length=150, blank=True)
    nonstackable = models.IntegerField(null=True, blank=True)
    rules_retailprice = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'promotions'

class RecurrentOitems(models.Model):
    orderitemid = models.IntegerField(primary_key=True)
    orderid = models.IntegerField(null=True, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    itemid = models.CharField(max_length=450, blank=True)
    itemname = models.TextField(blank=True)
    numitems = models.IntegerField(null=True, blank=True)
    unitprice = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    options = models.TextField(blank=True)
    optionprice = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    additional_field1 = models.CharField(max_length=150, blank=True)
    additional_field2 = models.CharField(max_length=150, blank=True)
    additional_field3 = models.CharField(max_length=150, blank=True)
    shipment_id = models.IntegerField(null=True, blank=True)
    catoptions = models.CharField(max_length=765, blank=True)
    catalogidoptions = models.CharField(max_length=765, blank=True)
    warehouseid = models.IntegerField(null=True, db_column='warehouseID', blank=True) # Field name made lowercase.
    unitcost = models.FloatField(null=True, blank=True)
    unitstock = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    page_added = models.CharField(max_length=765, blank=True)
    itemdescription = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'recurrent_oitems'

class RecurrentOrders(models.Model):
    orderid = models.IntegerField(primary_key=True)
    parent_orderid = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    last_order = models.DateTimeField(null=True, blank=True)
    next_order = models.DateTimeField(null=True, blank=True)
    ocustomerid = models.IntegerField(null=True, blank=True)
    odate = models.DateTimeField(null=True, blank=True)
    orderamount = models.FloatField(null=True, blank=True)
    ofirstname = models.CharField(max_length=300, blank=True)
    olastname = models.CharField(max_length=300, blank=True)
    oemail = models.CharField(max_length=300, blank=True)
    oaddress = models.CharField(max_length=600, blank=True)
    oaddress2 = models.CharField(max_length=150, blank=True)
    ocity = models.CharField(max_length=300, blank=True)
    ozip = models.CharField(max_length=45, blank=True)
    ostate = models.CharField(max_length=300, blank=True)
    ocountry = models.CharField(max_length=150, blank=True)
    ophone = models.CharField(max_length=90, blank=True)
    ofax = models.CharField(max_length=90, blank=True)
    ocompany = models.CharField(max_length=765, blank=True)
    ocardtype = models.CharField(max_length=150, blank=True)
    ocardno = models.CharField(max_length=765, blank=True)
    ocardname = models.CharField(max_length=600, blank=True)
    ocardexpiresmonth = models.CharField(max_length=30, blank=True)
    ocardexpiresyear = models.CharField(max_length=30, blank=True)
    ocardaddress = models.CharField(max_length=450, blank=True)
    ocardverification = models.CharField(max_length=150, blank=True)
    oprocessed = models.IntegerField()
    ocomment = models.TextField(blank=True)
    otax = models.FloatField(null=True, blank=True)
    otax2 = models.FloatField(null=True, blank=True)
    otax3 = models.FloatField(null=True, blank=True)
    ointernalcomment = models.TextField(blank=True)
    oexternalcomment = models.CharField(max_length=150, blank=True)
    oshippeddate = models.CharField(max_length=150, blank=True)
    oshipmethod = models.CharField(max_length=450, blank=True)
    oshipcost = models.FloatField(null=True, blank=True)
    oshipfirstname = models.CharField(max_length=300, blank=True)
    oshiplastname = models.CharField(max_length=150, blank=True)
    oshipcompany = models.CharField(max_length=600, blank=True)
    oshipemail = models.CharField(max_length=300, blank=True)
    oshipaddress = models.CharField(max_length=765, blank=True)
    oshipaddress2 = models.CharField(max_length=150, blank=True)
    oshipcity = models.CharField(max_length=150, blank=True)
    oshipzip = models.CharField(max_length=60, blank=True)
    oshipstate = models.CharField(max_length=150, blank=True)
    oshipcountry = models.CharField(max_length=150, blank=True)
    oshipphone = models.CharField(max_length=150, blank=True)
    opaymethod = models.IntegerField(null=True, blank=True)
    opaymethodinfo = models.TextField(blank=True)
    status = models.IntegerField(null=True, blank=True)
    other2 = models.CharField(max_length=150, blank=True)
    otime = models.DateTimeField(null=True, blank=True)
    oauthorization = models.CharField(max_length=765, blank=True)
    oerrors = models.CharField(max_length=765, blank=True)
    odiscount = models.FloatField(null=True, blank=True)
    ostatus = models.CharField(max_length=765, blank=True)
    affiliate_id = models.IntegerField(null=True, blank=True)
    ohandling = models.FloatField(null=True, blank=True)
    coupon = models.CharField(max_length=300, blank=True)
    coupondiscount = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    coupondiscountdual = models.FloatField(null=True, blank=True)
    giftcertificate = models.CharField(max_length=300, blank=True)
    giftamountused = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    giftamountuseddual = models.FloatField(null=True, blank=True)
    trackingcode = models.CharField(max_length=300, blank=True)
    invoicenum_prefix = models.CharField(max_length=150, blank=True)
    invoicenum = models.IntegerField(null=True, blank=True)
    order_status = models.IntegerField(null=True, blank=True)
    referer = models.TextField(blank=True)
    salesperson = models.CharField(max_length=150, blank=True)
    ip = models.CharField(max_length=48, blank=True)
    date_started = models.DateTimeField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    last_auto_email = models.IntegerField(null=True, blank=True)
    oweight = models.IntegerField(null=True, blank=True)
    oboxes = models.IntegerField(null=True, blank=True)
    orderkey = models.CharField(max_length=48, blank=True)
    ostep = models.CharField(max_length=150, blank=True)
    affiliate_approved = models.IntegerField(null=True, blank=True)
    affiliate_approvedreason = models.CharField(max_length=150, blank=True)
    shipmethodid = models.IntegerField(null=True, blank=True)
    insured = models.IntegerField(null=True, blank=True)
    alt_orderid = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'recurrent_orders'

class Reminders(models.Model):
    id = models.IntegerField(primary_key=True)
    contactid = models.IntegerField(null=True, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    itemid = models.CharField(max_length=450, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    lastchange = models.DateTimeField(null=True, blank=True)
    nextchange = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'reminders'

class RemindersFrequency(models.Model):
    id = models.IntegerField(primary_key=True)
    frequency_name = models.CharField(max_length=150, blank=True)
    frequency_days = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'reminders_frequency'

class ReportNewsletterEmails(models.Model):
    id = models.IntegerField(primary_key=True)
    newsletterid = models.IntegerField(null=True, blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    textmessage = models.TextField(blank=True)
    group = models.TextField(blank=True)
    maildate = models.DateTimeField(null=True, blank=True)
    mailusers = models.IntegerField(null=True, blank=True)
    totalusers = models.IntegerField(null=True, blank=True)
    sent = models.IntegerField(null=True, blank=True)
    opened = models.IntegerField(null=True, blank=True)
    fromemail = models.CharField(max_length=765, blank=True)
    replyemail = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'report_newsletter_emails'

class Rma(models.Model):
    idrma = models.IntegerField(primary_key=True, db_column='idRma') # Field name made lowercase.
    rmadate = models.DateTimeField(null=True, db_column='RmaDate', blank=True) # Field name made lowercase.
    orderid = models.IntegerField(null=True, blank=True)
    idrmareason = models.IntegerField(null=True, db_column='idRmaReason', blank=True) # Field name made lowercase.
    qty_received = models.IntegerField(null=True, blank=True)
    qty_restock = models.IntegerField(null=True, blank=True)
    idrmamethod = models.IntegerField(null=True, db_column='idRmaMethod', blank=True) # Field name made lowercase.
    idrmastatus = models.IntegerField(null=True, db_column='idRmaStatus', blank=True) # Field name made lowercase.
    idrmaaction = models.IntegerField(db_column='idRmaAction') # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True) # Field name made lowercase.
    intcomments = models.TextField(db_column='intComments', blank=True) # Field name made lowercase.
    staffcomments = models.TextField(db_column='staffComments', blank=True) # Field name made lowercase.
    filename = models.CharField(max_length=150, blank=True)
    filename2 = models.CharField(max_length=150, blank=True)
    filename3 = models.CharField(max_length=150, blank=True)
    filename4 = models.CharField(max_length=150, blank=True)
    filename5 = models.CharField(max_length=150, blank=True)
    filename6 = models.CharField(max_length=150, blank=True)
    filename7 = models.CharField(max_length=150, blank=True)
    filename8 = models.CharField(max_length=150, blank=True)
    filename9 = models.CharField(max_length=150, blank=True)
    filename10 = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'rma'

class RmaImagesTemp(models.Model):
    orderid = models.IntegerField()
    image1 = models.CharField(max_length=150)
    image2 = models.CharField(max_length=150)
    image3 = models.CharField(max_length=150)
    image4 = models.CharField(max_length=150)
    image5 = models.CharField(max_length=150)
    image6 = models.CharField(max_length=150)
    image7 = models.CharField(max_length=150)
    image8 = models.CharField(max_length=150)
    image9 = models.CharField(max_length=150)
    image10 = models.CharField(max_length=150)
    class Meta:
        db_table = u'rma_images_temp'

class RmaOitem(models.Model):
    idrma = models.IntegerField(null=True, db_column='idRma', blank=True) # Field name made lowercase.
    orderitemid = models.IntegerField(null=True, blank=True)
    qty_return = models.IntegerField(null=True, blank=True)
    qty_received = models.IntegerField(null=True, blank=True)
    qty_restock = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'rma_oitem'

class Rmaaction(models.Model):
    idrmaaction = models.IntegerField(primary_key=True, db_column='idRMAAction') # Field name made lowercase.
    rmaaction = models.CharField(max_length=192, db_column='RMAAction') # Field name made lowercase.
    class Meta:
        db_table = u'rmaaction'

class Rmahistory(models.Model):
    idrmahistory = models.IntegerField(primary_key=True, db_column='idRmaHistory') # Field name made lowercase.
    idrma = models.IntegerField(null=True, db_column='idRma', blank=True) # Field name made lowercase.
    orderitemid = models.IntegerField(null=True, blank=True)
    qty_return = models.IntegerField(null=True, blank=True)
    qty_received = models.IntegerField(null=True, blank=True)
    qty_restock = models.IntegerField(null=True, blank=True)
    idrmastatus = models.IntegerField(null=True, db_column='idRmaStatus', blank=True) # Field name made lowercase.
    statusdate = models.DateTimeField(null=True, db_column='StatusDate', blank=True) # Field name made lowercase.
    userid = models.CharField(max_length=150, db_column='UserId', blank=True) # Field name made lowercase.
    last_update = models.DateTimeField(null=True, db_column='Last_update', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'rmahistory'

class Rmamethod(models.Model):
    idrmamethod = models.IntegerField(primary_key=True, db_column='IdRmaMethod') # Field name made lowercase.
    rmamethod = models.CharField(max_length=765, db_column='RmaMethod', blank=True) # Field name made lowercase.
    visible = models.IntegerField(null=True, db_column='Visible', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'rmamethod'

class Rmareason(models.Model):
    idrmareason = models.IntegerField(primary_key=True, db_column='IdRmaReason') # Field name made lowercase.
    rmareason = models.CharField(max_length=765, db_column='RmaReason', blank=True) # Field name made lowercase.
    visible = models.IntegerField(null=True, db_column='Visible', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'rmareason'

class Rmastatus(models.Model):
    idrmastatus = models.IntegerField(primary_key=True, db_column='IdRmaStatus') # Field name made lowercase.
    rmastatus = models.CharField(max_length=150, db_column='RmaStatus', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'rmastatus'

class Searchs(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=150, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    results = models.IntegerField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'searchs'

class Serials(models.Model):
    id = models.IntegerField(primary_key=True)
    serial = models.CharField(max_length=150, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    used = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'serials'

class SerialsUsed(models.Model):
    id = models.IntegerField(primary_key=True)
    serial = models.CharField(max_length=150, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    orderitemid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'serials_used'

class Shipfrom(models.Model):
    id = models.IntegerField()
    country = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    zip = models.CharField(max_length=150, blank=True)
    diffaddenabled = models.IntegerField(null=True, db_column='DiffAddEnabled', blank=True) # Field name made lowercase.
    ups = models.IntegerField(null=True, blank=True)
    fedex = models.IntegerField(null=True, blank=True)
    dhl = models.IntegerField(null=True, blank=True)
    usps = models.IntegerField(null=True, blank=True)
    charge_ups = models.IntegerField(null=True, blank=True)
    charge_fedex = models.IntegerField(null=True, blank=True)
    charge_dhl = models.IntegerField(null=True, blank=True)
    charge_usps = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipfrom'

class Shipping(models.Model):
    shipid = models.IntegerField(primary_key=True)
    ship_name = models.CharField(max_length=450, blank=True)
    ship_type = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    ship_handling_charge = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    ship_charge = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    enabled = models.IntegerField(null=True, blank=True)
    lower = models.IntegerField(null=True, blank=True)
    upper = models.IntegerField(null=True, blank=True)
    markup = models.IntegerField(null=True, blank=True)
    ispercentage = models.IntegerField(null=True, blank=True)
    domestic = models.IntegerField(null=True, blank=True)
    international = models.IntegerField(null=True, db_column='International', blank=True) # Field name made lowercase.
    online = models.IntegerField(null=True, blank=True)
    credential1 = models.TextField(blank=True)
    credential2 = models.TextField(blank=True)
    credential3 = models.TextField(blank=True)
    credential4 = models.TextField(blank=True)
    setting1 = models.IntegerField(null=True, blank=True)
    options = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = u'shipping'

class ShippingCountries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name-short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    enabled_billing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_countries'

class ShippingExcludelist(models.Model):
    id = models.IntegerField(primary_key=True)
    shipid = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'shipping_excludelist'

class ShippingMethods(models.Model):
    shipcarriermethod_id = models.IntegerField(primary_key=True, db_column='SHIPCARRIERMETHOD_ID') # Field name made lowercase.
    method_name = models.CharField(max_length=765, db_column='METHOD_NAME', blank=True) # Field name made lowercase.
    shippingcarrierid = models.IntegerField(db_column='SHIPPINGCARRIERID') # Field name made lowercase.
    methodcode = models.CharField(max_length=36, db_column='MethodCode', blank=True) # Field name made lowercase.
    domestic = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_methods'

class ShippingOptions(models.Model):
    id = models.IntegerField(primary_key=True, db_column='Id') # Field name made lowercase.
    shippingmethod = models.IntegerField(null=True, db_column='ShippingMethod', blank=True) # Field name made lowercase.
    shippingcaption = models.CharField(max_length=210, db_column='ShippingCaption', blank=True) # Field name made lowercase.
    enabled = models.IntegerField(null=True, db_column='Enabled', blank=True) # Field name made lowercase.
    shippingcountry = models.CharField(max_length=150, db_column='ShippingCountry') # Field name made lowercase.
    shippingstate = models.CharField(max_length=150, db_column='ShippingState', blank=True) # Field name made lowercase.
    lowerwl = models.FloatField(null=True, db_column='LowerWL', blank=True) # Field name made lowercase.
    upperwl = models.FloatField(null=True, db_column='UpperWL', blank=True) # Field name made lowercase.
    markup = models.FloatField(null=True, db_column='Markup', blank=True) # Field name made lowercase.
    markupispercentage = models.IntegerField(null=True, db_column='MarkupIsPercentage', blank=True) # Field name made lowercase.
    discountgroup = models.FloatField(null=True, blank=True)
    freeship = models.IntegerField(null=True, blank=True)
    minimum = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_options'

class ShippingRanges(models.Model):
    id = models.IntegerField(primary_key=True)
    range1 = models.FloatField(null=True, blank=True)
    range2 = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    ispercentage = models.IntegerField(null=True, blank=True)
    stype = models.IntegerField(null=True, blank=True)
    costper = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_ranges'

class ShippingStates(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name-short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_states'

class ShippingZips(models.Model):
    id = models.IntegerField(primary_key=True)
    zipcode = models.CharField(max_length=150, blank=True)
    price = models.FloatField(null=True, blank=True)
    ispercentage = models.IntegerField(null=True, blank=True)
    stype = models.IntegerField(null=True, blank=True)
    costper = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_zips'

class Shippingerrors(models.Model):
    id = models.IntegerField(primary_key=True)
    shipper = models.CharField(max_length=765, blank=True)
    errorseverity = models.CharField(max_length=765, blank=True)
    errorcode = models.CharField(max_length=765, blank=True)
    errordescription = models.TextField(blank=True)
    errordate = models.DateTimeField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shippingerrors'

class Shorcuts(models.Model):
    id = models.IntegerField(primary_key=True)
    shorcut = models.CharField(max_length=150, blank=True)
    link = models.CharField(max_length=450, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shorcuts'

class Sitetext(models.Model):
    id = models.IntegerField(primary_key=True)
    varname = models.CharField(max_length=150, blank=True)
    varvalue = models.TextField(blank=True)
    vartype = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sitetext'

class StoreCloseIp(models.Model):
    id = models.IntegerField(primary_key=True)
    ipaddress = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'store_close_ip'

class StoreSettings2(models.Model):
    id = models.IntegerField()
    varname = models.CharField(max_length=150, blank=True)
    varvalue = models.TextField(blank=True)
    class Meta:
        db_table = u'store_settings2'

class SwfCustomerCreditsLog(models.Model):
    id = models.IntegerField()
    customers_email_address = models.CharField(max_length=765)
    customers_credit = models.FloatField(null=True, blank=True)
    customers_promocode = models.CharField(max_length=765, blank=True)
    customers_credit_type = models.CharField(max_length=765, blank=True)
    customers_credit_applied = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'swf_customer_credits_log'

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

class WsiWishlistitems(models.Model):
    wsi_id = models.IntegerField(primary_key=True, db_column='WSI_Id') # Field name made lowercase.
    wsh_id = models.IntegerField(null=True, blank=True)
    catalogid = models.IntegerField(null=True, blank=True)
    itemid = models.CharField(max_length=450, blank=True)
    itemname = models.TextField(blank=True)
    numitems = models.IntegerField(null=True, blank=True)
    unitprice = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    options = models.TextField(blank=True)
    optionprice = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    additional_field1 = models.CharField(max_length=150, blank=True)
    additional_field2 = models.CharField(max_length=150, blank=True)
    additional_field3 = models.CharField(max_length=150, blank=True)
    shipment_id = models.IntegerField(null=True, blank=True)
    catoptions = models.CharField(max_length=765, blank=True)
    catalogidoptions = models.CharField(max_length=765, blank=True)
    warehouseid = models.IntegerField(null=True, db_column='warehouseID', blank=True) # Field name made lowercase.
    unitcost = models.FloatField(null=True, blank=True)
    unitstock = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    page_added = models.CharField(max_length=765, blank=True)
    itemdescription = models.CharField(max_length=450, blank=True)
    reminder = models.IntegerField(null=True, blank=True)
    recurrent = models.IntegerField(null=True, blank=True)
    offlinesold = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wsi_wishlistitems'

