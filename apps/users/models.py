from django.db import models
from datetime import datetime
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])+(?=.*[0-9])+.{8,40}$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters.'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Please enter a valid email.'
        elif User.objects.filter(email=post_data['email']):
            errors['email'] = 'Email address already registered.'
        if datetime.today().year - datetime.strptime(post_data['birthdate'], "%Y-%m-%d").year < 13:
            errors['birthdate'] = "You must be 13 years or older to register."
        if not PASSWORD_REGEX.match(post_data['password']):
            errors['password'] = 'Password must have at least one uppercase letter, one lowercase letter, and one number, and be 8 to 40 characters in length.'
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = 'Given password does not match.'
        return errors
    def validate_login(self, post_data):
        errors = {}
        if not User.objects.filter(email=post_data['email']):
            errors['login'] = 'Login failed.'
            return errors
        if not bcrypt.checkpw(post_data['password'].encode(), User.objects.get(email=post_data['email']).pw_hash.encode()):
            errors['login'] = 'Login failed.'
            return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthdate = models.DateField()
    pw_hash = models.CharField(max_length=80)
    user_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        user_level_dict = {"1": "Suspended",
            "2": "Unverified",
            "5": "Normal",
            "9": "Admin",
            "10": "Superadmin"}
        return f"First Name: {self.first_name} | Last Name: {self.last_name} | Email: {self.email} | User level: {user_level_dict[str(self.user_level)]}"
