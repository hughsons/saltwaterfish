from django import forms
import logging

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    recaptcha = forms.CharField(max_length = 50, required=False,widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Enter Above Number'}))
    
class ForgetPwdForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address'}))
    recaptcha = forms.CharField(max_length = 20L,widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Enter Above Number'}))

class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()

class UploadForm(forms.Form):
    file = forms.FileField() 
    description = forms.CharField ( widget=forms.widgets.Textarea() )

class AddressForm(forms.Form):
    contact_id = forms.CharField(widget=forms.HiddenInput, required=False)
    first_name = forms.CharField(max_length = 50L, required=True)
    last_name = forms.CharField(max_length = 50L, required=True)
    company = forms.CharField(max_length = 255L, required=False)
    phone = forms.CharField(max_length = 50L, required=True)
    address1 = forms.CharField(max_length = 255L, required=True)
    address2 = forms.CharField(max_length = 255L, required=False)
    city = forms.CharField(max_length = 50L, required=True)
    country = forms.CharField(max_length = 100L, required=True)
    state = forms.CharField(max_length = 100L, required=True)
    zip = forms.CharField(max_length = 20L, required=True)
    address_type = forms.CharField(widget=forms.HiddenInput, required=False)

class RegistrationForm(forms.Form):
  email = forms.CharField(max_length = 25L)
  password = forms.CharField(widget=forms.PasswordInput, max_length = 25L)
  first_name = forms.CharField(max_length = 50L)
  last_name = forms.CharField(max_length = 50L)
  account_no = forms.CharField(max_length = 50L, required=False)
  company = forms.CharField(max_length = 255L, required=False)
  phone = forms.CharField(max_length = 50L, required=False)
  address1 = forms.CharField(max_length = 255L)
  address2 = forms.CharField(max_length = 255L, required=False)
  city = forms.CharField(max_length = 50L)
  country = forms.CharField(max_length = 100L)
  state = forms.CharField(max_length = 100L)
  zip = forms.CharField(max_length = 20L, required=False)
  comments = forms.CharField(max_length = 255L, required=False)
  recaptcha = forms.CharField(max_length = 20L)

class ChangePwdForm(forms.Form):
    #username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address', 'disabled':"disabled"}),max_length = 50)
    #old_password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    #new_password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address', 'disabled':"disabled"}),max_length = 50, required=False)
    old_password = forms.CharField(widget=forms.PasswordInput, max_length = 25L)
    new_password = forms.CharField(widget=forms.PasswordInput, max_length = 25L)


#--- Murthy Added Forms from 2013-16-17 --
class BillingShippingAddressForm(forms.Form):
  STATES = (('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),
            ('CA', 'California'),('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),
            ('FL', 'Florida'),('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),
            ('IN', 'Indiana'),('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
            ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),
            ('MN', 'Minnesota'),('MS', 'Mississippi'),('MO', 'Missouri'),('MT', 'Montana'),
            ('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
            ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VT', 'Vermont'),('VA', 'Virginia'),
            ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming'))  

  contact_id = forms.CharField(widget=forms.HiddenInput, required=False)
  billing_first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=False)
  billing_last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=False)
  billing_company = forms.CharField(max_length = 255L, required=False)
  billing_phone_part1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  billing_phone_part2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  billing_phone_part3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  billing_phone_ext = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  billing_address1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  billing_address2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  billing_city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':10}),max_length = 50, required=False)
  billing_state = forms.ChoiceField(choices=STATES) 
  billing_zip = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)

  shipping_first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=True)
  shipping_last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=True)
  shipping_company = forms.CharField(max_length = 255L, required=False)
  shipping_phone_part1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=True)
  shipping_phone_part2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=True)
  shipping_phone_part3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=True)
  shipping_phone_ext = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  shipping_address1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=True)
  shipping_address2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  shipping_city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':10}),max_length = 50, required=False)
  shipping_state = forms.ChoiceField(choices=STATES, initial='MO') 
  shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)


class CreditCardForm(forms.Form):
  previous_cards = forms.ChoiceField(choices=[], widget=forms.RadioSelect(), required=False)
  card_holder_name = forms.CharField(max_length = 50L)
  card_type = forms.ChoiceField(choices=[('V', 'Visa'), ('M', 'Master')])
  card_number = forms.CharField(max_length = 50L)
  card_expdate = forms.CharField(max_length = 5L)
  card_cvn = forms.CharField(max_length = 5L)
  is_save_card = forms.BooleanField(required=False, label="Check this")
  
  def __init__(self, *args, **kwargs):
    card_list = kwargs.pop('card_list')
    super(CreditCardForm, self).__init__(*args,**kwargs)
    self.fields['previous_cards'].choices = card_list 
 
 
  
class NewAccountForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 50)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=25)
  
class PaypalOrderFormNoLogin(BillingShippingAddressForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)
 
class PaypalOrderFormLoggedIn(BillingShippingAddressForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormNoLogin(BillingShippingAddressForm, CreditCardForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormLoggedIn(BillingShippingAddressForm, CreditCardForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class NoGateWay(BillingShippingAddressForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class RadioForm(forms.Form):
  STATES = (('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),
            ('CA', 'California'),('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),
            ('FL', 'Florida'),('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),
            ('IN', 'Indiana'),('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
            ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),
            ('MN', 'Minnesota'),('MS', 'Mississippi'),('MO', 'Missouri'),('MT', 'Montana'),
            ('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
            ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VT', 'Vermont'),('VA', 'Virginia'),
            ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming'))  

  shipping_state = forms.ChoiceField(choices=STATES, initial='CA')