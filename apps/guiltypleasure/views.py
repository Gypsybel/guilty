from django.shortcuts import render, redirect
from .models import User, Product, Address, Billing, Category, Image, Order, Review, Comment
from django.contrib import messages

def index(request):
    if not 'current_user' in request.session:
        request.session['guest'] = 'guest'
    # Category default will be show all products
    return render (request, 'guiltypleasure/index.html')

def log_reg(request):
    return render(request, 'guiltypleasure/customer_login.html')

def customer_login(request):
    if request.method == "POST":
        errors, user = User.objects.login(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "hey there")
            del request.session['guest']
            request.session['current_user'] = user.id
    return redirect('/')

def register(request):
    if request.method == "POST":
        errors, user = User.objects.register(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "Congrats you did it!")
    return redirect('/log_reg')

def customer_logout(request):
    messages.warning(request, 'you logged out bro')
    del request.session['current_user']
    return redirect('/')

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
    return render(request, 'guiltypleasure/adminlogin.html')


def admin_log(request):
    if request.method =="POST":
        errors, user = User.objects.admin_log(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors)
                return redirect('/admin_index')
        else:
            request.session['admin'] = user.id
            return redirect('/orders')
    else:
        return redirect('/')

def admin_logout(request):
    del request.session['admin']
    return redirect('/admin_index')
def orders(request):
	# This should be able to pull in all the informaiton throught the User ID link
    return render(request, 'guiltypleasure/adminorders.html')


def show_order(request, id):
    # Queries up the ass
    pass

def products(request):
    return render(request, 'guiltypleasure/adminproducts.html')

def addnew(request):
    category = Category.objects.all()
    return render(request, 'guiltypleasure/add_product.html', context={'category':category})


def addproduct(request):
    products = Product.objects.add(request.POST['name'], request.POST['description'], request.POST['select_category'], request.POST['new_cat'])
    if products == False:
        messages.warning(request,'Bro you messed up the form')
    else:
        messages.success(request,'Successfully added a product, YOU ROCK!')
    return redirect('/addnew')

def edit(request, id):
    # edit the product -> gives you the pop up page
    # return render(request, 'guiltypleasure/.html')
    pass

def delete(request, id):
    pass