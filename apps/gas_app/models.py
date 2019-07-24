"""
Define models for the gas app (except User)
"""
from datetime import datetime
from django.db import models
from apps.users.models import User
# from .helpers import cap_firsts
# Create your models here.
class CarMakeManager(models.Manager):
    """
    Define a manager to validate car make inputs
    """
    def check_exists(self, post_data):
        """
        Check if a make given in the new_car form exists in the database.
        """
        if CarMake.objects.filter(make_name__iexact=post_data['make'].strip()):
            return True
        return False
    def validate(self, post_data):
        """
        Validate the make data from a new car form.
        """
        errors = {}
        if not self.check_exists(post_data):
            if len(post_data['make'].strip()) < 2:
                errors['make'] = "Make name must be at least two characters."
        return errors


class CarModelManager(models.Manager):
    """
    Define a manager to validate car model inputs
    """
    def check_exists(self, post_data):
        """
        Check if a model given in the new_car form exists in the database.
        """
        if CarModel.objects.filter(model_name__iexact=post_data['model'].strip()):
            return True
        return False
    def validate(self, post_data):
        """
        Validate the model data from a new car form.
        """
        errors = {}
        if not self.check_exists(post_data):
            if len(post_data['model'].strip()) < 1:
                errors['model'] = "Model name must be at least one character."
        return errors


class CarManager(models.Manager):
    """
    Define a manager to validate inputs for creating a new car instance
    """
    def validate(self, post_data):
        """
        Validate inputs for creating and editing car instances
        """
        errors = {}
        if 'car_name' in post_data and len(post_data['car_name']) < 2:
            errors['car_name'] = "Custom car name must be at least two characters."
        if int(post_data['year']) > datetime.today().year + 2 or int(post_data['year']) < 1885:
            errors['year'] = "Year must be a released vehicle year."
        if len(post_data['trim']) > 45:
            errors['trim'] = "Trim cannot be more than 45 characters."
        return errors

class CarMake(models.Model):
    """
    Define car makes, eg. Toyota, Honda
    """
    make_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CarModel(models.Model):
    """
    Define car models, eg. Camry, Accord
    """
    model_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    make = models.ForeignKey(CarMake, related_name="make_models")


class Car(models.Model):
    """
    Define car instances.
    """
    car_name = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    trim = models.CharField(max_length=45, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="owned_cars")
    model = models.ForeignKey(CarModel, related_name="cars")


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
