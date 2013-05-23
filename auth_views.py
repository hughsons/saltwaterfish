from django.contrib.auth import *
from django.http import *
from forms import *
from django.template.loader import get_template
from django.template import Context
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
import logging, random, hashlib, datetime
from models import *
from django.core.context_processors import csrf


def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return value


@csrf_exempt
def CustomerLoginClass(request):
    if request.method == 'POST':
        #logout(request)
        customer_list=""
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.info('Form Is clean')
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if form.cleaned_data['recaptcha'] == str(request.session['ReCaptcha']):
                customer_list = customers.objects.filter(email = email,
                                                         pass_field= password, custenabled=1)
                if customer_list:
                    t = customers.objects.get(email = email,
                                              pass_field= password, custenabled=1)
                    t.lastlogindate = datetime.datetime.now()
                    t.save()
                    request.session['IsLogin'] = True
                    request.session['Customer'] = customer_list[0]
                    success = True
                    logging.info('LoginfoMessage:: %s',customer_list[0])
                    return HttpResponseRedirect('/myaccount')
                else:
                    request.session['ErrorMessage'] = "Invalid User name or Password."
                    return HttpResponseRedirect('/login')
            else:
                request.session['ErrorMessage'] = "Recaptcha is not matched."
                return HttpResponseRedirect('/login')
        else:
            request.session['ErrorMessage'] = "Invalid Form data."
            return HttpResponseRedirect('/login')
    else:
        request.session['ErrorMessage'] = "Form submission is not as expected."
        return HttpResponseRedirect('/login')

@csrf_exempt
def AdminLoginClass(request):
    if request.method == 'POST':
        logout(request)
        customer_list=""
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.info('Form Is clean')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            staff_list = Admins.objects.filter(username = username,
                                                     pass_field= hashlib.md5(password).hexdigest())
            if staff_list:
                t = Admins.objects.get(username = username,
                                       pass_field= hashlib.md5(password).hexdigest())
                t.lastlogin = datetime.datetime.now()
                t.save()
                request.session['IsLogin'] = True
                request.session['Staff_username'] = username
                request.session['Staff_password'] = password
                request.session['Staff'] = staff_list[0]
                success = True
                logging.info('LoginfoMessage:: %s',request.session['Staff_password'])
                return HttpResponseRedirect('/apanel')
            else:
                return HttpResponseRedirect('/alogin')
        else:
            return HttpResponseRedirect('/alogin')
    else:
        return HttpResponseRedirect('/alogin')

@csrf_exempt
def loginpage(request):
    state = "Please log in below..."
    t = get_template('login.htm')
    recaptcha = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request)
    #recaptcha2 = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request)
    default_message = ""
    error_message1, error_message2 = "", ""

    if 'message' in request.GET:
      default_message = request.GET['message']

    #if 'error' in request.GET:
    #  error_message = request.GET['error']
    error_message = ""
    if "ErrorMessage" in request.session:
      error_message1 = request.session["ErrorMessage"]
      del request.session["ErrorMessage"]
      
    if "ErrorMessage2" in request.session:
      error_message2 = request.session["ErrorMessage2"]
      del request.session["ErrorMessage2"]
    c = Context({
        'title': "SaltwaterFish :: Login",
        'form': LoginForm(),
        'forgotform':ForgetPwdForm,
        'recaptcha':recaptcha,
        'recaptcha2':recaptcha,
        'message2': default_message,
        'error_message1': error_message1,
        'error_message2': error_message2
    })
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def Adminloginpage(request):
    state = "Please log in below..."
    t = get_template('admin_login.htm')
    recaptcha = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request)
    c = Context({
        'title': "Adminstration Area",
        'form': LoginForm(),
    })
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
