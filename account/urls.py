from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', views.userProfile, name="userProfile"),
    path('product/', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),


    path('create_order/<str:pk>/', views.createOrder, name="createOrder"),
    path('update_order/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="deleteOrder"),

    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
]