from django.db import models
from django.contrib.auth.models import User

def validate_not_spaces(value):
    if value.strip() == '':
        
        raise ValidationError(u"You must provide more than just whitespace.")

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
        app_label = ''
 
class customers(models.Model):
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
    pass_field = models.CharField(max_length=150, db_column='pass', blank=True)
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
        app_label = ''
        ordering = ["-contactid"]

    
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
        app_label = ''

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
        app_label = ''
        ordering = ["-id"]

class CrmDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=150, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'crm_department'
        app_label = ''
        ordering = ["id"]

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
        app_label = ''

class CrmStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    statusid = models.IntegerField(null=True, blank=True)
    statustext = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'crm_status'
        app_label = ''

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
        app_label = ''

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
        app_label = ''

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
        app_label = ''

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
        app_label = ''
        ordering = ["-certificate_date"]

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
        app_label = ''

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
        app_label = ''

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
        app_label = ''

class OrderQuestions(models.Model):
    id = models.IntegerField(primary_key=True)
    questionid = models.IntegerField(null=True, blank=True)
    orderid = models.IntegerField(null=True, blank=True)
    answer = models.TextField(blank=True)
    class Meta:
        db_table = u'order_questions'
        app_label = ''


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
        app_label = ''
        ordering = ["-odate"]

class OrderStatus(models.Model):
    id = models.IntegerField()
    statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) # Field name made lowercase.
    statusdefinition = models.CharField(max_length=150, db_column='StatusDefinition', blank=True) # Field name made lowercase.
    statustext = models.CharField(max_length=150, db_column='StatusText', blank=True) # Field name made lowercase.
    visible = models.IntegerField(null=True, db_column='Visible', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'order_status'
        app_label = ''
        ordering = ["statusid"]

class PaymentMethods(models.Model):
    id = models.IntegerField()
    gateway_id = models.IntegerField(null=True, db_column='gateway_ID', blank=True) # Field name made lowercase.
    payment_gateway = models.CharField(max_length=150, blank=True)
    ccgateway = models.IntegerField(null=True, db_column='CCGateway', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'payment_methods'

class ProductAccessories(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    accessory_id = models.IntegerField(null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_accessories'
        app_label = ''

class ProductArticle(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    article_title = models.CharField(max_length=150, blank=True)
    short_review = models.CharField(max_length=450, blank=True)
    long_review = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    approved = models.IntegerField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_article'
        app_label = ''


class ProductBoxes(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_boxes'
        app_label = ''

class ProductCategory(models.Model):
    id = models.IntegerField()
    catalogid = models.IntegerField(null=True, blank=True)
    categoryid = models.IntegerField(null=True, blank=True)
    ismain = models.CharField(max_length=150, blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_category'
        app_label = ''


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
        app_label = ''

class ProductShipping(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    shipcarriermethodid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'product_shipping'
        app_label = ''

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
        app_label = ''

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
        app_label = ''

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
        app_label = ''
        ordering = ["-id"]

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
        app_label = ''
        ordering = ["-rmadate"]

class Rmastatus(models.Model):
    idrmastatus = models.IntegerField(primary_key=True, db_column='IdRmaStatus') # Field name made lowercase.
    rmastatus = models.CharField(max_length=150, db_column='RmaStatus', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'rmastatus'
        app_label = ''

class ShippingCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    ship_categoryname = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=150, blank=True)
    createddate = models.DateField(auto_now_add = True)
    class Meta:
        db_table = u'shipping_category'
        app_label = ''
        ordering = ["id"]

class ShippingCountries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name-short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    enabled_billing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_countries'
        app_label = ''

class ShippingStates(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name-short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_states'
        app_label = ''

class SiteBanners(models.Model):
    id = models.IntegerField(primary_key=True)
    banner_name = models.CharField(max_length=250, blank=True)
    banner_type = models.CharField(max_length=100, blank=True)
    banner_image = models.CharField(max_length=250, blank=True)
    banner_link = models.TextField(blank=True)
    banner_content = models.TextField(blank=True)
    banner_target = models.CharField(max_length=33, blank=True)
    banner_status = models.IntegerField(null=True, blank=True)
    datentime = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'site_banners'
        app_label = ''

class StoreSettings2(models.Model):
    id = models.IntegerField()
    varname = models.CharField(max_length=150, blank=True)
    varvalue = models.TextField(blank=True)
    class Meta:
        db_table = u'store_settings2'
        app_label = ''


class SwfCustomerCreditsLog(models.Model):
    id = models.IntegerField()
    customers_email_address = models.CharField(max_length=765)
    customers_credit = models.FloatField(null=True, blank=True)
    customers_promocode = models.CharField(max_length=765, blank=True)
    customers_credit_type = models.CharField(max_length=765, blank=True)
    customers_credit_applied = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'swf_customer_credits_log'
        app_label = ''

class SwfCustomerCreditsTracking(models.Model):
    id = models.IntegerField()
    customers_email_address = models.CharField(max_length=765)
    customers_credit = models.DecimalField(null=True, max_digits=21, decimal_places=4, blank=True)
    customers_promocode = models.CharField(max_length=765, blank=True)
    customers_credit_type = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'swf_customer_credits_tracking'
        app_label = ''

class SwfProductSortTemp(models.Model):
    id = models.IntegerField(primary_key=True)
    product_category_id = models.IntegerField()
    product_category_sorting = models.IntegerField()
    class Meta:
        db_table = u'swf_product_sort_temp'
        app_label = ''

class Tax(models.Model):
    id = models.IntegerField(primary_key=True)
    tax_country = models.CharField(max_length=150, blank=True)
    tax_state = models.CharField(max_length=150, blank=True)
    tax_value1 = models.CharField(max_length=9, blank=True)
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
        app_label = ''

class Template(models.Model):
    template = models.CharField(max_length=150, blank=True)
    stylesheet = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'template'
        app_label = ''

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
        app_label = ''

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
        app_label = ''

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
        app_label = ''
