from django.urls import path
from . import views

#ticket urls

urlpatterns = [
    path('customer/create-ticket',views.createTicket,name='create_ticket'),
    path('customer/list-ticket',views.listTicket,name='list_ticket'),
    path('customer/view-details/<int:id>',views.viewDetails,name='view_details')
]