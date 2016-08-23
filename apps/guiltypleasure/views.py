from django.shortcuts import render, redirect
from .models import User, Product, Address, Billing, Category, Image, Order, Review, Comment

def index(request):
    return render (request, 'guiltypleasure/index.html')
