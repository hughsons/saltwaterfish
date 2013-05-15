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
