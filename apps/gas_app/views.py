"""
Define functions for each URL route
"""
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Sum, F
from apps.users.views import logged_in, cur_usr_id
from apps.users.models import User
from .models import Car, Entry

# Create your views here.
def index(request): #TODO GET USER DATA RENDER gas:home
    """
    Returns the landing page, including graph and quick summary.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    if 'active_car' not in request.session or not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
    current_car = Car.objects.get(id=cur_car_id(request))
    current_user = User.objects.get(id=cur_usr_id(request))
    if not Entry.objects.filter(car=current_car):
        return redirect(reverse('gas:new_entry'))
    all_entries = Entry.objects.annotate(price_per_gallon=F('price') / F('gallons')).filter(car=current_car).order_by('-id')
    entries = Entry.objects.annotate(price_per_gallon=F('price') / F('gallons')).filter(car=current_car).order_by('-id')[:6]
    comparison_dict = {}
    all_data = {
        "dates": [],
        "gallons": [],
        "odometer": [],
        "miles_since_last": [],
        "miles_per_gallon": [],
        "miles_per_day": [],
        "cost": [],
        "cost_per_gallon": [],
    }
    for i in range(len(all_entries)-1):
        date_string = all_entries[i].entry_date.strftime("%d %b %Y")
        all_data['dates'].append(date_string)
        all_data['gallons'].append(all_entries[i].gallons)
        all_data['odometer'].append(all_entries[i].odometer)
        mile_comparison = all_entries[i].odometer - all_entries[i+1].odometer
        all_data['miles_since_last'].append(mile_comparison)
        mpg_comparison = mile_comparison / all_entries[i].gallons
        all_data['miles_per_gallon'].append(mpg_comparison)
        days_between = all_entries[i].entry_date - all_entries[i+1].entry_date
        try:
            per_day_comparison = mile_comparison / days_between.days
        except ZeroDivisionError:
            per_day_comparison = 0
        all_data['miles_per_day'].append(per_day_comparison)
        all_data['cost'].append(all_entries[i].price)
        all_data['cost_per_gallon'].append(round(all_entries[i].price_per_gallon, 2))
    for key in all_data:
        all_data[key] = all_data[key][::-1]
    for i in range(len(entries)-1):
        mile_comparison = entries[i].odometer - entries[i+1].odometer
        mpg_comparison = mile_comparison / entries[i].gallons
        comparison_dict[entries[i]] = [mile_comparison, mpg_comparison]
    #data_json = json.dumps(all_data, sort_keys=False, indent=1, cls=DjangoJSONEncoder)
    #print(data_json)
    context = {
        "data_json": all_data,
        "current_car": current_car,
        "comp_dict": comparison_dict,
        "all_cars": Car.objects.filter(owner=current_user),
        "last_entry": Entry.objects.filter(car=current_car).last(),
    }
    return render(request, "gas_app/index.html", context)


def new_car(request): #DONE GET NEW CAR FORM RENDER gas:new_car
    """
    Returns the form to enter a new car.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    current_user = User.objects.get(id=cur_usr_id(request))
    context = {
        "all_cars": Car.objects.filter(owner=current_user),
    }
    return render(request, "gas_app/new_entry.html", context)


def create_car(request): #DONE POST SUBMIT NEW CAR FORM REDIRECT gas:create_car
    """
    POSTs the form for the new car
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    errors = Car.objects.validate(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('gas:new_car'))
    fields = {
        "car_name": request.POST['car-name'],
        "car_year": int(request.POST['car-years']),
        "car_make": request.POST['car-makes'],
        "car_model": request.POST['car-models'],
        "car_trim": request.POST['car-model-trims'],
        "car_owner": User.objects.get(id=cur_usr_id(request))
    }
    if not request.POST['car-name']:
        fields["car_name"] = "My Car"
    car = Car.objects.create(name=fields['car_name'], year=fields['car_year'], make=fields['car_make'], model=fields['car_model'], trim=fields['car_trim'], owner=fields['car_owner'])
    request.session['active_car'] = car.id
    return redirect(reverse('gas:home'))


def view_car(request, car_id): #DONE GET CAR DATA RENDER gas:view_car
    """
    Returns page to view all the details for the desired call, including a
    quick summary and all the data entries for that car.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    request.session['active_car'] = car_id
    if not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
        return redirect(reverse('gas:view_car', kwargs={'car_id': cur_car_id(request)}))
    current_car = Car.objects.get(id=cur_car_id(request))
    current_user = User.objects.get(id=cur_usr_id(request))
    if not Entry.objects.filter(car=current_car):
        limited_context = {
            "current_car": current_car,
            "all_cars": Car.objects.filter(owner=current_user),
            "no_entries": True
        }
        return render(request, "gas_app/entry_list.html", limited_context)
    total_miles = Entry.objects.filter(car=current_car).last().odometer - Entry.objects.filter(car=current_car).first().odometer
    total_gallons = Entry.objects.filter(car=current_car).aggregate(Sum('gallons'))
    total_spent = Entry.objects.filter(car=current_car).aggregate(Sum('price'))
    try:
        avg_price_per_mile = total_spent['price__sum'] / total_miles
    except ZeroDivisionError:
        avg_price_per_mile = 0
    avg_price_per_mile = str(round(avg_price_per_mile, 2))
    try:
        avg_mpg = total_miles / (total_gallons['gallons__sum'] - Entry.objects.filter(car=current_car).first().gallons)
    except ZeroDivisionError:
        avg_mpg = 0
    avg_mpg = str(round(avg_mpg, 2))
    avg_price_per_gal = total_spent['price__sum'] / total_gallons['gallons__sum']
    avg_price_per_gal = str(round(avg_price_per_gal, 2))
    try:
        avg_miles_per_day = total_miles / (Entry.objects.filter(car=current_car).last().entry_date - Entry.objects.filter(car=current_car).first().entry_date).days
    except ZeroDivisionError:
        avg_miles_per_day = 0
    avg_miles_per_day = str(round(avg_miles_per_day, 2))
    total_gallons = str(round(total_gallons['gallons__sum'], 3))
    total_spent = str(round(total_spent['price__sum'], 2))
    all_entries = Entry.objects.annotate(price_per_gallon=F('price') / F('gallons')).filter(car=current_car).order_by('-id')
    comparison_dict = {}
    for i in range(len(all_entries)-1):
        mile_comparison = all_entries[i].odometer - all_entries[i+1].odometer
        mpg_comparison = mile_comparison / all_entries[i].gallons
        comparison_dict[all_entries[i]] = [mile_comparison, mpg_comparison]
    context = {
        "no_entries": False,
        "all_entries": all_entries,
        "range": range(len(all_entries)),
        "comp_dict": comparison_dict,
        "last_entry": Entry.objects.filter(car=current_car).last(),
        "first_entry": Entry.objects.filter(car=current_car).first(),
        "total_miles": total_miles,
        "total_gallons": total_gallons,
        "total_spent": total_spent,
        "avg_miles_per_day": avg_miles_per_day,
        "avg_price_per_gal": avg_price_per_gal,
        "avg_price_per_mile": avg_price_per_mile,
        "avg_mpg": avg_mpg,
        "current_car": current_car,
        "all_cars": Car.objects.filter(owner=current_user),
    }
    return render(request, "gas_app/entry_list.html", context)


def edit_car(request, car_id): #TODO GET EDIT CAR FORM RENDER gas:edit_car
    """
    Returns a form to edit an owned car.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    request.session['active_car'] = car_id
    current_car = Car.objects.get(id=cur_car_id(request))
    current_user = User.objects.get(id=cur_usr_id(request))
    context = {
        "current_car": current_car,
        "all_cars": Car.objects.filter(owner=current_user),
    }
    return render(request, "gas_app/new_entry.html", context)


def update_car(request): #TODO POST SUBMIT EDIT CAR FORM REDIRECT gas:update_car
    """
    POST the form to the database
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    errors = Car.objects.validate(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('gas:edit_car'))
    fields = {
        "car_name": request.POST['car-name'],
        "car_year": int(request.POST['car-years']),
        "car_make": request.POST['car-makes'],
        "car_model": request.POST['car-models'],
        "car_trim": request.POST['car-model-trims'],
    }
    if not request.POST['car-name']:
        fields["car_name"] = "My Car"
    car = Car.objects.get(id=cur_car_id(request))
    car.name = fields['car_name']
    car.year = fields['car_year']
    car.make = fields['car_make']
    car.model = fields['car_model']
    car.trim = fields['car_trim']
    car.save()
    return redirect(reverse('gas:home'))


def delete_car(request, car_id): #TODO DELETE CAR REDIRECT gas:delete_car
    """
    Delete an owned car, and delete all related entries.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    request.session['active_car'] = car_id
    if not owns_car(request):
        request.session['active_car'] = None
        return redirect(reverse('gas:home'))
    c = Car.objects.get(id=cur_car_id(request))
    c.delete()
    return redirect(reverse('gas:home'))


def new_entry(request): #TODO GET NEW ENTRY FORM RENDER gas:new_entry
    """
    Render form to create a new entry.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    if 'active_car' not in request.session or not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
    current_car = Car.objects.get(id=cur_car_id(request))
    current_user = User.objects.get(id=cur_usr_id(request))
    context = {
        "current_car": current_car,
        "all_cars": Car.objects.filter(owner=current_user),
    }
    return render(request, "gas_app/new_entry.html", context)


def create_entry(request): #TODO SUBMIT NEW ENTRY FORM REDIRECT gas:create_entry
    """
    POST form to create a new entry.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    if 'active_car' not in request.session or not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
    errors = Entry.objects.validate(request.POST, cur_usr_id(request))
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('gas:new_entry'))
    fields = {
        'entry_date': request.POST['date'],
        'odometer': int(request.POST['odometer']),
        'gallons': float(request.POST['gallons']),
        'price': float(request.POST['price']),
        'creator': User.objects.get(id=cur_usr_id(request)),
        'car': Car.objects.get(id=request.POST['car_select'])
    }
    Entry.objects.create(entry_date=fields['entry_date'], odometer=fields['odometer'], gallons=fields['gallons'], price=fields['price'], creator=fields['creator'], car=fields['car'])
    return redirect(reverse('gas:home'))


def view_entry(request): #TODO GET ENTRY DATA RENDER gas:view_entry
    """
    Renders information for a specific entry. Maybe unnecessary.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    return redirect(reverse('gas:home'))


def edit_entry(request, entry_id): #TODO GET EDIT ENTRY FORM RENDER gas:edit_entry
    """
    Return form to edit user's most recent entry.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    if 'active_car' not in request.session or not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
    current_car = Car.objects.get(id=cur_car_id(request))
    current_user = User.objects.get(id=cur_usr_id(request))
    entry = Entry.objects.get(id=entry_id)
    context = {
        "current_car": current_car,
        "all_cars": Car.objects.filter(owner=current_user),
        "entry": entry,
    }
    return render(request, "gas_app/new_entry.html", context)


def update_entry(request, entry_id): #TODO POST EDIT ENTRY FORM REDIRECT gas:update_entry
    """
    Updates an entry.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    if not has_car(request):
        return redirect(reverse("gas:new_car"))
    if 'active_car' not in request.session or not owns_car(request):
        request.session['active_car'] = Car.objects.filter(owner=User.objects.get(id=cur_usr_id(request))).first().id
    errors = Entry.objects.validate(request.POST, cur_usr_id(request))
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('gas:new_entry'))
    fields = {
        'entry_date': request.POST['date'],
        'odometer': int(request.POST['odometer']),
        'gallons': float(request.POST['gallons']),
        'price': float(request.POST['price']),
    }
    e = Entry.objects.filder(id=entry_id)[0]
    e.entry_date = fields['entry_date']
    e.odometer = fields['odometer']
    e.gallons = fields['gallons']
    e.price = fields['price']
    e.save()
    return redirect(reverse('gas:home'))


def delete_entry(request): #TODO DELETE ENTRY REDIRECT gas:delete_entry
    """
    Deletes an entry.
    """
    if not logged_in(request):
        return redirect(reverse('users:home'))
    return redirect(reverse('gas:home'))


def has_car(request):
    """
    Checks if current user has a car.
    """
    user = User.objects.get(id=cur_usr_id(request))
    cars = Car.objects.filter(owner=user)
    if not cars:
        return False
    return True


def cur_car_id(request):
    """
    If there is an `active_car` in session, returns its ID. Otherwise, return none.
    """
    if 'active_car' not in request.session:
        return None
    return request.session['active_car']

def owns_car(request):
    """
    Check if the current user owns the currently active car.
    """
    if 'current_user' not in request.session or 'active_car' not in request.session or not Car.objects.filter(id=cur_car_id(request)):
        return False
    user = User.objects.get(id=cur_usr_id(request))
    car = Car.objects.get(id=cur_car_id(request))
    if car.owner != user:
        return False
    return True
