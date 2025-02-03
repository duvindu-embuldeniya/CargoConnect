from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="home"),
    path('parcels/', parcels, name="parcels"),
    path('customer_view/<int:pk>/', customer_page, name="customer_view"),
    path('take_parcel/<int:pk>/', takeParcell, name="take_parcel"),
    path('update_order/<int:pk>/', updateOrder, name="update_order"),
    path('delete_order/<int:pk>/', deleteOrder, name="delete_order"),
 

    path('register/', register, name='register'),
    ##### path('login/', auth_views.LoginView.as_view(template_name = 'engine/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', myProfile, name='my_profile'),
    path('profile_delete/<str:username>/', deleteProfile, name='delete_profile'),

    path('add_product', addParcel, name='add_product'),
    path('update_product/<int:pk>/', updateProduct, name='update_product'),
    path('delete_product/<int:pk>/', removeProduct, name='remove_product'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'home/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = "home/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'home/password_reset_complete.html'), name='password_reset_complete'),

]

