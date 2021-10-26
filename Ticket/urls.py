from django.urls import path
from . import views

#ticket urls

urlpatterns = [
    path('customer/create-ticket',views.createTicket,name='create_ticket'),
    path('customer/list-ticket',views.listTicket,name='list_ticket'),
    path('customer/solved-ticket',views.solvedTicket,name='solved_ticket'),
    path('customer/assign-ticket',views.assignTicket,name='assign_ticket'),
    path('customer/delete-ticket/<int:id>/',views.deleteTicket,name='delete_ticket'),
    path('customer/edit-ticket/<int:id>/',views.editTicket,name='edit_ticket'),
    path('view-details/<int:id>',views.viewDetails,name='view_details'),

    path('caretaker/incoming-ticket',views.incomingTicket,name='incoming_ticket'),
    path('caretaker/ticket-assign/',views.ticketAssigns,name='ticket_assign'),
    path('caretaker/solved-ticket-list/',views.solvedClosedList,name='solve_ticket_list'),
    path('caretaker/my-assign-list',views.assignList,name='assign_list'),
    path('customer/send-message',views.customerMessage,name='customer_message'),
    path('carateker/close-ticket',views.closeTicket,name='close_ticket')

]