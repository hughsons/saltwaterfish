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


def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return value


@csrf_exempt
def CustomerLoginClass(request):
    if request.method == 'POST':
        logout(request)
        customer_list=""
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.info('Form Is clean')
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    else:
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
def LoginView(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.htm', {
                'error' : error,
                'form' : form,
        })
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        # Redirect to a success page.
                        login(request, user)
                        return HttpResponseRedirect('/apanel')
                    else:
                        login(request, user)
                        return HttpResponseRedirect('/')
                else:
                    # Return a 'disabled account' error message
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                 # Return an 'invalid login' error message.
                error = u'invalid login'
                return errorHandle(error)
        else:
            error = u'form is invalid'
            return errorHandle(error)
    else:
        form = LoginForm() # An unbound form
        return render_to_response('login.htm', {
            'form': form,
        })

@csrf_exempt
def loginpage(request):
    state = "Please log in below..."
    t = get_template('login.htm')
    recaptcha = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request)
    recaptcha2 = "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s" %GetRecaptcha(request)
    c = Context({
        'title': "SaltwaterFish :: Login",
        'form': LoginForm(),
        'forgotform':ForgetPwdForm,
        'recaptcha':recaptcha,
        'recaptcha2':recaptcha2,
    })
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
