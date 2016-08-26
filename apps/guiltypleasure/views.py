from django.shortcuts import render, redirect
from .models import User, Product, Category, Image, Order, Review, Comment, Ord_Prod
from django.contrib import messages
from django.db.models import Q

def index(request):
    if not 'current_user' in request.session:
        request.session['guest'] = []
    products = Product.objects.all()
    image = Image.objects.all()
    image_list = []
    for i in image:
        images_url = str(i.image)
        test = images_url[20:]
        image_list.append({'id':i.product_id, 'url':test})
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
            if 'guest' in request.session:
                del request.session['guest']
            request.session['current_user'] = user.id
    return redirect ('/')

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
    if 'product' in request.session:
        del request.session['product']
    if 'quantity' in request.session:
        del request.session['quantity']
    if 'current_user' in request.session:
        messages.warning(request, 'you logged out bro')
        del request.session['current_user']
    return redirect('/')

def category(request, id):
    if not 'current_user' in request.session:
        request.session['guest'] = 'guest'
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category_id = category)
    image = Image.objects.all()
    image_list = []
    for i in image:
        images_url = str(i.image)
        test = images_url[20:]
        image_list.append({'id':i.product_id, 'url':test})
    title = category.category
    category = Category.objects.all()
    context={'products':products, 'images':image_list, 'categories':category, 'titles':title}
    return render (request, 'guiltypleasure/index.html', context)

def show_product(request, id):
    product = Product.objects.get(id=id)
    similar = Product.objects.filter(category_id=product.category_id).exclude(id=id)[:6]
    print ('*'*100)
    print similar
    similar_url = []
    for i in similar:
        temp = Image.objects.get(product_id=i)
        tempimage = str(temp.image)[20:]
        similar_url.append({'url':tempimage, 'product':i})
    image = Image.objects.get(product_id=product)
    image_str = str(image.image)
    sliced = image_str[20:]
    context = {"product":product, 'image':sliced, 'similar':similar_url}
    return render(request, 'guiltypleasure/show.html', context)

def review(request, id):
   	pass

def comment(request, id):
    pass

def add_to_cart(request, id):
    if 'current_user' in request.session:
        prod_add = Product.objects.get(id=id)
        if 'product' in request.session:
            temp = request.session['product']
            temp.append(prod_add.id)
            request.session['product'] = temp
        else:
            request.session['product'] = [prod_add.id]
        if 'quantity' in request.session:
            temp = request.session['quantity']
            temp.append(request.POST['quantity'])
            request.session['quantity'] = temp
        else:
            request.session['quantity'] = [request.POST['quantity']]
    elif 'guest' in request.session:
        prod_add = Product.objects.get(id=id)
        if 'product' in request.session:
            temp = request.session['product']
            temp.append(prod_add.id)
            request.session['product'] = temp
        else:
            request.session['product'] = [prod_add.id]
        if 'quantity' in request.session:
            temp = request.session['quantity']
            temp.append(request.POST['quantity'])
            request.session['quantity'] = temp
        else:
            request.session['quantity'] = [request.POST['quantity']]
    else:
        return redirect('/')
    print request.session['product']
    print request.session['quantity']
    return redirect('/show_product/' + id)

# Buy button should update the quantity field in the Cart view

def cart(request):
    if 'current_user' in request.session:
        user = User.objects.get(id=request.session['current_user'])
    else:
        user = 'guest'
    product_name = []
    product_price =[]
    quantity_list = []
    total = []
    if 'product' in request.session:
        for i in range(0, len(request.session['product'])):
            prod = Product.objects.get(id = request.session['product'][int(i)])
            product_name.append(prod.name)
            product_price.append(prod.price)
    if 'quantity' in request.session:
        quantity_list = request.session['quantity']
    for u in range(0, len(product_name)):
        total_cost = (int(quantity_list[u]) * int(product_price[u]))
        total.append(total_cost)
    

    all_data = []
    for x in range(0,len(product_name)):
        name = product_name[x]
        price = product_price[x]
        quantity = quantity_list[x]
        cost = total[x]
        all_data.append({'name': name, 'price': price, 'quantity': quantity, 'cost':cost})
    real_total = 0
    for a in range(0, len(total)):
        real_total += total[a]
    
    context = {'all_data': all_data,
                'display_total':real_total,
                'user': user}

    return render(request, 'guiltypleasure/carts.html', context)


def update(request):
    pass

def place_order(request):
    Order.objects.create(order_first_name=request.POST['first_name'], order_last_name=request.POST['last_name'], address_line1=request.POST['address_line1'], address_line2=request.POST['address_line2'], city=request.POST['city'], state=request.POST['state'], zipcode=request.POST['zipcode'], billing_address_line1=request.POST['billing_address_line1'], billing_address_line2=request.POST['billing_address_line2'], billing_city=request.POST['billing_city'], billing_state=request.POST['billing_state'], billing_zipcode=request.POST['billing_zipcode'], card=request.POST['card'], security_code=request.POST['security_code'], expiration=request.POST['expiration'] )
    print ("*"*100)
    print ('we posted an order!')
    order = Order.objects.filter(card=request.POST['card']).order_by('-created_at')[0:1]
    # this may only grab the latest order 
    print order


# once order is created need specific Order ID

    product_id = []
    product_name = []
    product_price =[]
    quantity_list = []
    total = []
    if 'product' in request.session:
        for i in range(0, len(request.session['product'])):
            prod = Product.objects.get(id = request.session['product'][int(i)])
            product_id.append(prod.id)
            product_name.append(prod.name)
            product_price.append(prod.price)
    if 'quantity' in request.session:
        quantity_list = request.session['quantity']
    for u in range(0, len(product_name)):
        total_cost = (int(quantity_list[u]) * int(product_price[u]))
        total.append(total_cost)

    for x in range(0, len(product_id)):
        product_object = Product.objects.get(id=product_id[x])
        Ord_Prod.objects.create(order_id = order,product_id=product_object,quantity=quantity_list[x], price_total=total[x] )

        # this will make objects in the Ord_Prod table and will need to link to get ID from Order table
    return redirect('/')

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
            return redirect('/order_list')
    else:
        return redirect('/')

def admin_logout(request):
    del request.session['admin']
    return redirect('/admin_index')

def order_list(request):
    orders = Ord_Prod.objects.all().order_by('-created_at')
    context = {'orders':orders}
	# This should be able to pull in all the informaiton throught the User ID link
    return render(request, 'guiltypleasure/adminorders.html', context)


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
