from django.shortcuts import render, redirect
from .models import User, Product, Address, Billing, Category, Image, Order, Review, Comment
from django.contrib import messages

def index(request):
    if not 'current_user' in request.session:
        request.session['guest'] = 'guest'
    products = Product.objects.all()
    image = Image.objects.all()
    image_list = []
    for i in image:
        images_url = str(i.image)
        test = images_url[20:]
        print ("*"*100)
        print test
        image_list.append({'id':i.product_id, 'url':test})
        print image_list
    category = Category.objects.all()
    context={'products':products, 'images':image_list, 'categories':category}
    return render (request, 'guiltypleasure/index.html', context)

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
    product = Product.objects.get(id=id)
    context = {"product":product}
    return render(request, 'guiltypleasure/show.html', context)

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
    products = Product.objects.all()
    return render(request, 'guiltypleasure/adminproducts.html', context={'products':products})

def addnew(request):
    category = Category.objects.all()
    return render(request, 'guiltypleasure/add_product.html', context={'category':category})


def addproduct(request):
    products = Product.objects.add(request.POST['name'], request.POST['description'], request.POST['select_category'], request.POST['new_cat'],request.POST['price'], request.FILES['file'])
    if products == False:
        messages.warning(request,'Bro you messed up the form')
    else:
        messages.success(request,'Successfully added a product, YOU ROCK!')
    return redirect('/addnew')

def edit(request, id):
    product = Product.objects.get(id=id)
    category = Category.objects.all()
    context={'product':product, 'category':category}
    return render(request, 'guiltypleasure/edit_product.html', context)

def editproduct(request, id):
    product = Product.objects.edit(request.POST['name'], request.POST['description'], request.POST['select_category'], request.POST['new_cat'],request.POST['price'], id)
    return redirect('/products')

def delete(request, id):
    Product.objects.filter(id=id).delete()
    return redirect('/products')
