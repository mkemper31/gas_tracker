from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
import bcrypt
from .models import User

# Create your views here.
def index(request):
    if logged_in(request):
        return redirect(reverse('users:success'))
    return render(request, 'users/index.html')


def register(request):
    return render(request, 'users/signin.html')


def signin(request):
    return render(request, 'users/signin.html')


def submit_register(request):
    if request.method != "POST":
        return redirect(reverse('users:index'))
    errors = User.objects.validate_registration(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('users:index'))
    else:
        passhash = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['reg_email'], birthdate=request.POST['birthdate'],pw_hash=passhash)
        request.session['current_user'] = User.objects.last().id
        messages.success(request, "Successfully registered")
        return redirect(reverse('gas:home')) # TODO: redirect to proper route


def submit_signin(request):
    if request.method != "POST":
        return redirect(reverse('users:index'))
    errors = User.objects.validate_login(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('users:index'))
    else:
        request.session['current_user'] = User.objects.get(email=request.POST['login_email']).id
        messages.success(request, "Successfully logged in")
        return redirect(reverse('gas:home')) # TODO: redirect to proper route


def dashboard(request):
    pass

def success(request):
    if not logged_in(request):
        return redirect(reverse('users:index'))
    context = {
        'first_name': User.objects.get(id=request.session['current_user']).first_name,
        'last_name': User.objects.get(id=request.session['current_user']).last_name,
        'email': User.objects.get(id=request.session['current_user']).email,
        'birthdate': User.objects.get(id=request.session['current_user']).birthdate,
    }
    return render(request, 'users/success.html', context)


def logout(request):
    request.session.flush()
    messages.success(request, "Successfully logged out")
    return redirect(reverse('users:index'))


def invalid(request):
    return HttpResponse("<h1>HTTP 404</h1><a href='/'>Return to index</a>")


def logged_in(request):
    if 'current_user' not in request.session:
        print('current_user not in session')
        return False
    else:
        return True


def cur_usr_id(request):
    if 'current_user' not in request.session:
        return None
    else:
        return request.session['current_user']
