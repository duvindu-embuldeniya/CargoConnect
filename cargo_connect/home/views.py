from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from . forms import OrderForm, OrderForm2, UserRegistrationForm, ProductForm
# from django.forms import inlineformset_factory
# from .filters import OrderFilter
from django.contrib.auth.models import User, auth
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import UserUpdateForm, ProfileUpdateForm
 
def home(request):
	orders = Order.objects.all().order_by('-date_created')[0:10]
	users = User.objects.all()
	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	intransit = Order.objects.filter(status='In Transit').count()
	total_customers = users.count()
	context = {'users':users, 'orders':orders,'total_orders':total_orders, 
	'delivered':delivered, 'intransit':intransit, 'total_customers': total_customers}
	
	return render(request, 'home/index.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			auth.login(request, new_user)
			messages.success(request, "Account created successfully!")
			return redirect('home')
	else:
		form = UserRegistrationForm()
	return render(request, 'home/register.html', {'form': form})

class CustomLoginView(auth_views.LoginView):
    template_name = 'home/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "You have logged in successfully!")
        return super().get_success_url()


def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, f"You haven't logged in!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "You have logged out successfully!")
    return render(request, 'home/logout.html')

@login_required
def myProfile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, "Your profile has been updated successfully!")
			return redirect('my_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {'user': request.user, 'u_form': u_form, 'p_form': p_form}
	return render(request, 'home/profile.html', context)

@login_required
def deleteProfile(request, username):
	user = User.objects.get(username=username)
	if request.user != user:
		return HttpResponse("<h1>You are not allowed here! 403</h1>")
	if request.method == 'POST':
		user.delete()
		messages.success(request, "Your account has been deleted successfully!")
		return redirect('home')
	context = {'user': user}
	return render(request, 'home/delete_profile.html', context)

@login_required
def parcels(request):
	products = Product.objects.exclude(note='taken')
	context = {'products':products}
	return render(request, 'home/products.html', context)

@login_required
def addParcel(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			new_product = form.save(commit=False)
			new_product.by = request.user
			new_product.save()
			return redirect('parcels')
	else:
		form = ProductForm()
	return render(request, 'home/add_product.html', {'form': form})
	
@login_required
def updateProduct(request, pk):
	product = Product.objects.get(pk=pk)
	usr = product.by
	if request.user != usr:
		return HttpResponse("<h1>You are not allowed here! 403</h1>")
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('parcels')
	else:
		form = ProductForm(instance=product)
	return render(request, 'home/update_product.html', {'form': form})

@login_required
def removeProduct(request, pk):
	product = Product.objects.get(pk=pk)
	usr = product.by
	if request.user != usr:
		return HttpResponse("<h1>You are not allowed here! 403</h1>")
	if request.method == 'POST':
		product.delete()
		return redirect('parcels')
	return render(request, 'home/remove_product.html', {'product':product})

@login_required
def customer_page(request, pk):
	customer = User.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()
	# orderFilter = OrderFilter(request.GET, queryset=orders) 
	# orders = orderFilter.qs
	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders}
	return render(request, 'home/customer.html', context)

@login_required
def takeParcell(request, pk):
	# orderFormset = inlineformset_factory(User, Order, fields = ('product', 'status'), extra = 3)
	# formset = orderFormset(queryset = Order.objects.none(), instance=user)
	if request.method == 'POST':
		form = OrderForm(request.POST, user=request.user)
		# formset = orderFormset(request.POST, instance=user)
		if form.is_valid():
			new_order = form.save(commit=False)
			new_order.customer = request.user
			new_order.save()

			product = new_order.product
			product.note = "taken"
			product.save()

			return redirect('customer_view', pk = request.user.pk)
	else:
		form = OrderForm(user=request.user)
	return render(request, 'home/create_order.html', {'form':form})

@login_required
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm2(instance=order)
	usr = order.customer
	if request.user != usr:
		return HttpResponse("<h1>You are not allowed here! 403</h1>")
	if request.method == 'POST':
		form = OrderForm2(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('customer_view', pk = usr.pk)

	context =  {'form':form}
	return render(request, 'home/update_order.html', context)

@login_required
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	usr = order.customer
	parcel = order.product.name
	if request.user != usr:
		return HttpResponse("<h1>You are not allowed here! 403</h1>")
	if request.method == 'POST':

		if order.status == "In Transit":
			order.delete()
			order.product.note = ''
			order.product.save()

		elif order.status == "Delivered":
			order.delete()

		return redirect('customer_view', pk = usr.pk)
		
	return render(request, 'home/delete_item.html', {'parcel':parcel, 'order':order})

