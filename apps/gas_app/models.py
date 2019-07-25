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
        if len(post_data['car-name']) > 2:
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


class Car(models.Model):
    """
    Define car instances.
    """
    car_name = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    trim = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="owned_cars")
    objects = CarManager()


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
