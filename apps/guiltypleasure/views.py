from django.shortcuts import render, redirect
from .models import User, Product, Address, Billing, Category, Image, Order, Review, Comment

def index(request):
    # Category default will be show all products
    return render (request, 'guiltypleasure/index.html')

def customer_login(request):
        pass    

def category(request, id):
    # take in category ID and filter by products with the category ID	
    	pass  

def show_product(request, id):
    # take you to product page with discription
    # query the "show" product ID and filter the similar products by category ID to display
    return render(request, 'guiltypleasure/show.html')

def review(request, id):
   	pass

def comment(request, id):
    pass    	    

def buy(request, id):
    # TOAST a message " Item added to the cart" and then fade out the message after a few seconds
    return render(request, 'guiltypleasure/show.html')   

# Buy button should update the quantity field in the Cart view

def cart(request):
    # take in session User id to view current products in the CART!!!
    # IF guest they need to fill in the table.
    # IF logged in user info populates on tables.
    return render(request, 'guiltypleasure/carts.html')

def update(request):
    pass    

def pay(request, id):
	# Credit card api and
	pass
  

# def page(request):
# 	# Still to figure out!
# 	pass

		# ADMIN STUFF

def admin_index(request):
    # return render(request, 'guiltypleasure/admindashboard.html')
    pass

def admin_log(request):
    # Log in verification here
    pass
    # return redirect ('/orders')

def orders(request):
	# This should be able to pull in all the informaiton throught the User ID link
    # return render(request, 'guiltypleasure/orders.html')
    pass

def show_order(request, id):
    # Queries up the ass
    pass

def products(request):
    # return render(request, 'guiltypleasure/products.html')
    pass

def addnew(request):
	# return render (request, 'guiltypleasure/addnew.html')
	pass

def edit(request, id):
    # edit the product -> gives you the pop up page
    pass    
