from django.shortcuts import render
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout 
from .models import Client, ShoppingCart, Product, ProductShoppingcart, Order, OrderProduct
from django.core.paginator import Paginator
from datetime import date
# Create your views here.

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            client = Client()
            client.user = user
            client.client_email = user.email
            client.client_name = form.cleaned_data['name']
            client.client_surname = form.cleaned_data['surname']
            client.client_phonenumber = form.cleaned_data['phone_number']
            cart = ShoppingCart()
            cart.save()
            client.shopping_cart = cart 
            client.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request=request, template_name="index.html", context={'page_obj': page_obj})

def products_by_category(request, category):
	
	products = Product.objects.filter(product_category__icontains = category).all()
	context = {'products': products}
	return render(request=request, template_name="products.html", context=context)

def product_by_id(request, id):
	
	product = Product.objects.filter(id = id).all()[0]
	return render(request = request, template_name='product.html', context = {'product': product})

def add_to_shoppingcart(request, id):
	product = Product.objects.filter(id = id).all()[0]
	username = request.user.username
	client = Client.objects.filter(user__username = username).all()[0]
	shopping_cart = client.shopping_cart
	product_in_shopping_cart = ProductShoppingcart()
	product_in_shopping_cart.Product = product
	product_in_shopping_cart.ShoppingCart = shopping_cart
	product_in_shopping_cart.save()
	return redirect('show_shopping_cart')

def show_shopping_cart(request):
	username = request.user.username
	client = Client.objects.filter(user__username = username).all()[0]
	products = ProductShoppingcart.objects.filter(ShoppingCart__id = client.shopping_cart.id).all()
	to_return = []
	total = 0
	for prod in products:
		to_return.append(prod.Product)
		total += prod.Product.price
	return render(request=request, template_name="shopping_cart.html", context={'products': to_return, "price": total})

def remove_from_shoppingcart(request, id):
	username = request.user.username
	client = Client.objects.filter(user__username = username).all()[0]
	products_in_shoppingcart = ProductShoppingcart.objects.filter(ShoppingCart__id = client.shopping_cart.id).all()
	product_to_remove = None 
	for p in products_in_shoppingcart:
		if p.Product.id == id:
			product_to_remove = p 
			break 
	product_to_remove.delete()
	return redirect('show_shopping_cart')

def make_order(request):
	username = request.user.username
	client = Client.objects.filter(user__username = username).all()[0]
	products_in_shoppingcart = ProductShoppingcart.objects.filter(ShoppingCart__id = client.shopping_cart.id).all()
	order = Order()
	order.client = client
	order.date_created = date.today()
	total = 0
	for prod in products_in_shoppingcart:
		total += prod.Product.price
	order.total_price = total
	order.save()
	for prod in products_in_shoppingcart:
		order_product = OrderProduct()
		order_product.order = order 
		order_product.product = prod.Product
		order_product.save()
	for prod in products_in_shoppingcart:
		prod.delete()
	return render(request=request, template_name="order.html")
      
	
	
	