from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PRICE_REGEX = re.compile(r'^[0-9]+\.[0-9][0-9]$')

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
            errors.append('First name should be at least one character')
        if len(form_data['last_name']) < 1:
            errors.append('Last name should be at least one character')
        if not len(form_data['email']) > 0:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(form_data['email']):
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
            user = User.objects.create(first_name=form_data['first_name'], last_name=form_data['last_name'],
                                        email=form_data['email'].lower(), password=hashed_password)
            if not user:
                return (['Something went wrong'], None)
            return (None, user)

    def admin_log(self, form_data):
        errors = []
        if len(form_data['email']) > 0 and len(form_data['password']) > 7:
            check_email = User.objects.filter(email='admin@kelvinfanclub.com'.lower())
            if len(check_email) > 0 and form_data['email'] == 'admin@kelvinfanclub.com':
                user = check_email[0]
                if bcrypt.hashpw(form_data['password'].encode(), user.password.encode()) == user.password:
                    return (None, user)
        errors.append('Invalid login credentials.')
        return (errors, None)

class ProductManager(models.Manager):
    def add(self, name, description, select_category, new_cat,price, file):
        if name == '':
            return (False)
        if description == '':
            return (False)
        if not PRICE_REGEX.match(price):
            return (False)
        if select_category == '':
            if new_cat == '':
                return(False)
            else:
                check_cat = Category.objects.filter(category = select_category)
                if len(check_cat) > 0:
                    return (False)
                Category.objects.create(category = new_cat)
                category = Category.objects.get(category = new_cat)
        else:
            category = Category.objects.get(id = select_category)

        Product.objects.create(name= name,description = description,price = price, category_id = Category.objects.get(id=category.id),inventory = 100, sold = 0,)
        product = Product.objects.get(name= name, description = description,price = price, category_id = Category.objects.get(id=category.id))
        Image.objects.create(image=file, product_id=product)
        return(True)

    def edit(self, name, description, select_category, new_cat,price, id):
        if name == '':
            return (False)
        if description == '':
            return (False)
        if not PRICE_REGEX.match(price):
            return (False)
        if select_category == '':
            if new_cat == '':
                return(False)
            else:
                check_cat = Category.objects.filter(category = select_category)
                if len(check_cat) > 0:
                    return (False)
                Category.objects.create(category = new_cat)
                category = Category.objects.get(category = new_cat)
        else:
            category = Category.objects.get(id = select_category)
        Product.objects.filter(id=id).update(name= name)
        Product.objects.filter(id=id).update(description = description)
        Product.objects.filter(id=id).update(price = price)
        Product.objects.filter(id=id).update(category_id = Category.objects.get(id=category.id))
        return(True)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    address_id = models.OneToOneField('Address', related_name = 'Address', null = True)
    billing_id = models.OneToOneField('Billing', related_name = 'Billing', null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Address(models.Model):
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    zipcode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Billing(models.Model):
    billing_address_line1 = models.CharField(max_length=100)
    billing_address_line2 = models.CharField(max_length=100)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=40)
    billing_zipcode = models.CharField(max_length=10)
    card = models.CharField(max_length=40)
    security_code = models.CharField(max_length=5)
    expiration = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits = 20, decimal_places = 2)
    category_id = models.ForeignKey('Category')
    inventory = models.IntegerField()
    sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

class Category(models.Model):
    category = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    image = models.ImageField(upload_to='apps/guiltypleasure/static/guiltypleasure/images')
    product_id = models.ForeignKey(Product, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    status = models.CharField(max_length=40)
    user_id = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = OrderManager() does not exist yet

class Comment(models.Model):
    comment = models.TextField(max_length=250)
    review_id = models.ForeignKey('Review')
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField(max_length=400)
    rating = models.IntegerField()
    product_id = models.ForeignKey(Product)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
