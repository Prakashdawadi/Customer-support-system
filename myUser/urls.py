from django.urls import path
from . import views

urlpatterns= [
    path('customer/signup',views.customerSignup,name='customersignup'),
    path('customer/signin',views.customerLogin,name = "customerlogin"),
    path('customer/dashboard',views.customerDashboard,name="customerdashboard"),
    path('customer/logout',views.customerLogout,name='customerlogout'),
    path('customer/editprofile/<int:id>/',views.EditcustomerProfile,name='customerprofiles'),

    #caretaker signup
    path('caretaker/signup',views.caretakerSignup,name='caretakersignup'),
    path('caretaker/signin',views.caretakerLogin,name="caretakerlogin"),
    path('caretaker/dashboard',views.caretakerDashboard,name='caretakerdashboard'),
    path('caretaker/logout',views.caretakerLogout,name='caretakerlogout')


]