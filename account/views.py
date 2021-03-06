from .models import *
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login, logout

from .filters import OrderFilters
from .forms import OrderForm, UserCreateForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def register(request):

	# if request.user.is_authenticated:
	# 	return redirect('home')
	form = UserCreateForm()
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			form.save()
			# user = form.save()
			# group = Group.objects.get(name='customer')
			# user.groups.add(group)
			# Customer.objects.create(
			# 	user=user,
			# )

			username = form.cleaned_data.get('username')
			messages.add_message(request, messages.SUCCESS, 'User '+ username +' register successfully.')
			return redirect('login')
			
	context = {
		'form': form
	}
	return render(request, 'account/register.html', context)

@unauthenticated_user
def login(request):

	# if request.user.is_authenticated:
	# 	return redirect('home')
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username Or Password Incorrect..')

	context = {}
	return render(request, 'account/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required
@allowed_users(allowed_roles=['admin', 'customer'])
def accountSettings(request):

	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			
	context = {
		'form': form
	}
	return render(request, 'account/account_setting.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):

	orders = request.user.customer.order_set.all()

	total_orders	= orders.count() 
	delieverd 		= orders.filter(status='Delieverd').count()
	pending 		= orders.filter(status='Pending').count()
	
	context = {
		'orders': orders,
		'pending': pending, 
		'delieverd': delieverd, 
		'total_orders': total_orders,
	}

	return render(request, 'account/user.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):

	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_orders	= orders.count() 
	total_customers = customers.count()

	delieverd = orders.filter(status='Delieverd').count()
	pending = orders.filter(status='Pending').count()

	context = { 
		'orders': orders, 
		'pending': pending, 
		'customers': customers,
		'delieverd': delieverd, 
		'total_orders': total_orders, 
		'total_customers': total_customers 
	}
	return render(request, 'account/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):

	products = Product.objects.all()
	return render(request, 'account/product.html', { 'products': products })

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

	customer = Customer.objects.get(id=pk)
	
	orders = customer.order_set.all()
	orders_count = orders.count()

	myFilters = OrderFilters(request.GET, queryset=orders)
	orders = myFilters.qs

	context = {
		'orders': orders,
		'customer': customer,
		'myFilters': myFilters,
		'orders_count': orders_count,
	}
	return render(request, 'account/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):

	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
	customer = Customer.objects.get(id=pk)

	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={ 'customer': customer })
	
	if request.method == 'POST':
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('home')

	# context = { 'form': form }
	context = { 'formset': formset }
	
	return render(request, 'account/orders_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('home')

	context = {
		'form': form
	}
	return render(request, 'account/orders_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):

	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('home')

	context = {
		'item': order
	}
	return render(request, 'account/delete.html', context)

