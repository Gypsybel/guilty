from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, form_data):
            errors = []
            if len(form_data['email']) > 0 and len(form_data['password']) > 7:
                check_email = User.objects.filter(email=form_data['email'].lower())
                if len(check_email) > 0:
                    user = check_email[0]
                    if bcrypt.hashpw(form_data['password'].encode(), user.password.encode()) == user.password:
                        return (None, user)
            errors.append('Invalid login credentials.')
            return (errors, None)

    def register(self, form_data):
        errors = []
        if len(form_data['first_name']) < 1:
            errors.append('Name should be at least one character')
        if len(form_data['last_name']) < 1:
            errors.append('Alias should be at least one character')
        if not len(form_data['email']) > 0:
            errors.append('Email is required')
        elif not VALID_EMAIL.match(form_data['email']):
            errors.append('Please enter a valid email')
        if len(form_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif form_data['password'] != form_data['passconf']:
            errors.append('Password must match confirmation field')
        if len(errors) > 0:
            return (errors, None)
        else:
            check_email = User.objects.filter(email=form_data['email'].lower())
            if len(check_email) > 0:
                return (['Email already taken!'], None)
            hashed_password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=form_data['name'], alias=form_data['alias'],
                                        email=form_data['email'].lower(),
                                        password=hashed_password
            if not user:
                return (['Something went wrong'], None)
            return (None, user)

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Address(models.Model):
    address_type = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    zipcode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Billing(models.Model):
    card = models.CharField(max_length=40)
    security_code = models.CharField(max_length=5)
    expiration = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    category_id = models.ForeignKey(Category)
    image_id = models.ForeignKey(Image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

class Category(models.Model):
    category = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    status = models.CharField(max_length=40)
    user_name = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

class Comment(models.Model):
    comment = models.TextField(max_length=250)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField(max_length=400)
    user_id = models.ForeignKey(User)
    comment_id = models.ForeignKey(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
