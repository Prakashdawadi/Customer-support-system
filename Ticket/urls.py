from django.urls import path
from . import views

#ticket urls

urlpatterns = [
    path('customer/create-ticket',views.createTicket,name='create_ticket'),
    path('customer/list-ticket',views.listTicket,name='list_ticket'),
    path('customer/view-details/<int:id>',views.viewDetails,name='view_details'),
    path('caretaker/incoming-ticket',views.incomingTicket,name='incoming_ticket'),
    path('caretaker/ticket-assign/<int:id>/<int:tid>/',views.ticketAssigns,name='ticket_assign')
]