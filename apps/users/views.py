from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
import bcrypt
from .models import User

# Create your views here.
def index(request):
    if logged_in(request):
        return redirect(reverse('gas:home'))
    return render(request, 'users/index.html')


def register(request):
    if logged_in(request):
        return redirect(reverse('gas:home'))
    return render(request, 'users/signin.html')


def signin(request):
    if logged_in(request):
        return redirect(reverse('gas:home'))
    return render(request, 'users/signin.html')


def submit_register(request):
    if request.method != "POST":
        return redirect(reverse('users:register'))
    errors = User.objects.validate_registration(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('users:register'))
    else:
        passhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], birthdate=request.POST['birthdate'], pw_hash=passhash, user_level=5)
        new_usr = User.objects.last()
        if new_usr == User.objects.first():
            print("Assigning new super admin")
            new_usr.user_level = 10
            new_usr.save()
        request.session['current_user'] = User.objects.last().id
        messages.success(request, "Successfully registered")
        return redirect(reverse('gas:home')) # DONE: redirect to proper route


def submit_signin(request):
    if request.method != "POST":
        return redirect(reverse('users:signin'))
    errors = User.objects.validate_login(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('users:signin'))
    else:
        request.session['current_user'] = User.objects.get(email=request.POST['email']).id
        messages.success(request, "Successfully logged in")
        return redirect(reverse('gas:home')) # DONE: redirect to proper route


def dashboard(request):
    pass

def success(request):
    if not logged_in(request):
        return redirect(reverse('users:home'))
    context = {
        'first_name': User.objects.get(id=request.session['current_user']).first_name,
        'last_name': User.objects.get(id=request.session['current_user']).last_name,
        'email': User.objects.get(id=request.session['current_user']).email,
        'birthdate': User.objects.get(id=request.session['current_user']).birthdate,
    }
    return render(request, 'users/success.html', context)


def logout(request):
    """
    Logs out the current session and flushes the session.
    """
    request.session.flush()
    messages.success(request, "Successfully logged out")
    return redirect(reverse('users:home'))


def invalid(request):
    return HttpResponse("<h1>HTTP 404</h1><a href='/'>Return to index</a>")


def logged_in(request):
    """
    Checks that the session is presently logged in. Useful for situations in which you need
    to check if a page should or should not be accessible when a user is or is not logged in.

    Returns boolean.
    """
    if 'current_user' not in request.session:
        print('current_user not in session')
        return False
    else:
        return True


def cur_usr_id(request):
    """
    Gets the value of the current user's ID, or returns None if not logged in.
    """
    if 'current_user' not in request.session:
        return None
    else:
        return request.session['current_user']
