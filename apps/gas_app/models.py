"""
Define models for the gas app (except User)
"""
from datetime import datetime
from django.db import models
from apps.users.models import User

class CarManager(models.Manager):
    """
    Define a manager to validate inputs for creating a new car instance
    """
    def validate(self, post_data):
        """
        Validate inputs for creating and editing car instances
        """
        errors = {}
        if len(post_data['car-name']) > 255:
            errors['car_name'] = "Custom car name may not be more than 255 characters."
        if not post_data['car-years']:
            errors['year'] = "Select a year."
        elif int(post_data['car-years']) > datetime.today().year + 2 or int(post_data['car-years']) < 1885:
            errors['year'] = "Year must be a released vehicle year."
        if not post_data['car-makes']:
            errors['make'] = "Select a make."
        if not post_data['car-models']:
            errors['model'] = "Select a model."
        if not post_data['car-model-trims']:
            errors['trim'] = "Select a trim."
        return errors


class EntryManager(models.Manager):
    """
    Defines a manager for the Entry class.
    """
    def validate(self, post_data, user_id, edit=False):
        """
        Validate inputs for creating or editing entry instances.
        """
        user = User.objects.get(id=user_id)
        car = Car.objects.filter(id=post_data['car_select']).first()
        car_entries = Entry.objects.filter(car=car).order_by('-id')
        if car_entries:
            if not edit:
                last_entry = car_entries[0]
            elif edit:
                last_entry = car_entries[1]
        errors = {}
        if car.owner != user:
            errors['car_select'] = "Invalid car selection."
        if len(post_data['odometer']) < 1:
            errors['odometer'] = "Enter a value for the odometer."
        elif not isfloat(post_data['odometer']):
            errors['odometer'] = "Must be a numerical value."
        elif int(post_data['odometer']) < 0:
            errors['odometer'] = "Odometer cannot be negative."
        if car_entries:
            if int(post_data['odometer']) <= last_entry.odometer:
                errors['odometer'] = "Cannot set odometer to a smaller value than the previous entry."
        if len(post_data['gallons']) < 1:
            errors['gallons'] = "Enter a number of gallons purchased."
        elif not isfloat(post_data['gallons']):
            errors['gallons'] = "Must be a numerical value."
        elif float(post_data['gallons']) < 0:
            errors['gallons'] = "Gallons cannot be negative."
        if len(post_data['price']) < 1:
            errors['price'] = "Enter a price."
        elif not isfloat(post_data['price']):
            errors['price'] = "Must be a numerical value."
        elif float(post_data['price']) < 0:
            errors['price'] = "Price cannot be negative."
        if datetime.today() < datetime.strptime(post_data['date'], "%Y-%m-%d"):
            errors['date'] = "Date must not be in the future."
        return errors


class Car(models.Model):
    """
    Define car instances.
    """
    name = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    trim = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="owned_cars")
    objects = CarManager()
    def __repr__(self):
        name_str = f"Name: {self.name} | "
        year_str = f"Year: {self.year} | "
        make_str = f"Make: {self.make} | "
        model_str = f"Model: {self.model} | "
        trim_str = f"Trim: {self.trim} | "
        owner_str = f"Owner: {self.owner.first_name} {self.owner.last_name}"
        return name_str + year_str + make_str + model_str + trim_str + owner_str


class Entry(models.Model):
    """
    Define entry instances.
    """
    entry_date = models.DateField()
    odometer = models.IntegerField()
    gallons = models.FloatField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="created_entries")
    car = models.ForeignKey(Car, related_name="entries")
    objects = EntryManager()


# class SavedGraph(models.Model):
#     name = models.CharField(max_length=255)
#     notes = models.TextField(max_length=1000)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     x_axis = models.CharField(max_length=255) # saved selection for x-axis. date usually?
#     y_axis = models.CharField(max_length=255)
# saved selection for y-axis. mpg, price... this might not work out. might need a list?
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

def isfloat(string):
    """
    Check if a given string can be converted to a floating point number.

    Returns boolean.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False
