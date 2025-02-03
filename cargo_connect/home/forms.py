from django.forms import ModelForm
from .models import Order, Product, Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'status']
    
    def __init__(self, *args, **kwargs):
        # Get the user from the passed arguments
        user = kwargs.pop('user', None)  
        super(OrderForm, self).__init__(*args, **kwargs)

        # Exclude products with note='taken'
        self.fields['product'].queryset = Product.objects.exclude(note='taken')

        # Exclude products added by the logged-in user
        self.fields['product'].queryset = self.fields['product'].queryset.exclude(by=user)

        # Only include 'In Transit' in the status field choices
        self.fields['status'].choices = [choice for choice in Order.STATUS if choice[0] == 'In Transit']


class OrderForm2(ModelForm):
	class Meta:
		model = Order
		fields = ['status']
	
class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['date_created', 'note','by']
	
class UserUpdateForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','email']

class ProfileUpdateForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['telephone', 'image']