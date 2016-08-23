from django.shortcuts import render, redirect
from .models import User, Product, Address, Billing, Category, Image, Order, Review, Comment

def index(request):
    return render (request, 'guiltypleasure/index.html')

def show_product(request, id):
    return render(request, 'guiltypleasure/show.html')

def cart(request):
    pass

def admin_index(request):
    pass

def admin_log(request):
    pass

def orders(request):
    pass

def show_order(request):
    pass

def products(request):
    pass
