from django import forms

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

class CreditCardForm(forms.Form):
  previous_cards = forms.ChoiceField(choices=[], widget=forms.RadioSelect(), required=False)
  card_holder_name = forms.CharField(max_length = 50L)
  card_type = forms.ChoiceField(choices=[('V', 'Visa'), ('M', 'Master')])
  card_number = forms.CharField(max_length = 50L)
  card_expdate = forms.CharField(max_length = 5L)
  card_cvn = forms.CharField(max_length = 5L)
  is_save_card = forms.BooleanField(required=False, label="Check this")
  
  def __init__(self, *args, **kwargs):
    super(CreditCardForm, self).__init__(*args,**kwargs)
    #previous_cards = args[0]['previous_cards']
    #previous_cards = [('4111111111111111', 'Account ending in 2003'), ('378282246310005', 'Account ending in 2004'), ('4111111111111111', 'Account ending in 2005')]
    #logging.info("\n\n\n\n IN FORMS \n\n\n")
    #logging.info(args[0]['previous_cards'])
    #logging.info("\nIN FORMS \n\n\n\n\n")
    #logging.info(previous_cards)
    #self.fields['previous_cards'].choices = previous_cards 
 
    #self.fields['previous_cards'].choices = [(1, 'Hello'), (2, 'Kiran')]
  
  
class NewAccountForm(forms.Form):
  username = forms.CharField(max_length = 50L)
  password = forms.CharField(max_length = 25L)
  
class PaypalOrderFormNoLogin(AddressForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)
 
class PaypalOrderFormLoggedIn(AddressForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormNoLogin(AddressForm, CreditCardForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormLoggedIn(AddressForm, CreditCardForm):

  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)
