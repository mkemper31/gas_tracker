"""
Define functions for each URL route
"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Car
from apps.users.views import logged_in, cur_usr_id

# Create your views here.
def index(request): #TODO GET USER DATA RENDER gas:home
    """
    Returns the landing page, including graph and quick summary.
    """
    return render(request, "gas_app/index.html")


def new_car(request): #TODO GET NEW CAR FORM RENDER gas:new_car
    """
    Returns the form to enter a new car.
    """
    return render(request, "gas_app/new_entry.html")


def create_car(request): #TODO POST SUBMIT NEW CAR FORM REDIRECT gas:create_car
    """
    POSTs the form for the new car
    """
    print(request.POST)
    errors = Car.objects.validate(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('gas:new_car'))
    return redirect(reverse('gas:home'))


def view_car(request): #TODO GET CAR DATA RENDER gas:view_car
    """
    Returns page to view all the details for the desired call, including a
    quick summary and all the data entries for that car.
    """
    return render(request, "gas_app/entry_list.html")


def edit_car(request): #TODO GET EDIT CAR FORM RENDER gas:edit_car
    """
    Returns a form to edit an owned car.
    """
    return render(request, "gas_app/new_entry.html")


def update_car(request): #TODO POST SUBMIT EDIT CAR FORM REDIRECT gas:update_car
    """
    POST the form to the database
    """
    return redirect(reverse('gas:home'))


def delete_car(request): #TODO DELETE CAR REDIRECT gas:delete_car
    """
    Delete an owned car, and delete all related entries.
    """
    return redirect(reverse('gas:home'))


def new_entry(request): #TODO GET NEW ENTRY FORM RENDER gas:new_entry
    """
    Render form to create a new entry.
    """
    return render(request, "gas_app/new_entry.html")


def create_entry(request): #TODO SUBMIT NEW ENTRY FORM REDIRECT gas:create_entry
    """
    POST form to create a new entry.
    """
    return redirect(reverse('gas:home'))


def view_entry(request): #TODO GET ENTRY DATA RENDER gas:view_entry
    """
    Renders information for a specific entry. Maybe unnecessary.
    """
    return redirect(reverse('gas:home'))


def edit_entry(request): #TODO GET EDIT ENTRY FORM RENDER gas:edit_entry
    """
    Return form to edit user's most recent entry.
    """
    return render(request, "gas_app/new_entry.html")


def update_entry(request): #TODO POST EDIT ENTRY FORM REDIRECT gas:update_entry
    """
    Updates an entry.
    """
    return redirect(reverse('gas:home'))


def delete_entry(request): #TODO DELETE ENTRY REDIRECT gas:delete_entry
    """
    Deletes an entry.
    """
    return redirect(reverse('gas:home'))
