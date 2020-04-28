from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', views.userProfile, name="userProfile"),
    path('product/', views.product, name="product"),
    path('account/', views.accountSettings, name="account"),
    path('customer/<str:pk>/', views.customer, name="customer"),


    path('create_order/<str:pk>/', views.createOrder, name="createOrder"),
    path('update_order/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="deleteOrder"),

    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),


    path('reset_password/', 
        auth_view.PasswordResetView.as_view(template_name="account/password_reset.html"), 
        name="reset_password"
    ),
    path('reset_password_sent/', 
        auth_view.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), 
        name="password_reset_done"
    ),
    path('reset/<uidb64>/<token>', 
        auth_view.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), 
        name="password_reset_confirm"
    ),
    path('reset_password_complete/', 
        auth_view.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), 
        name="password_reset_complete"
    ),
]