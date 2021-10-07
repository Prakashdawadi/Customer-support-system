from django.contrib import admin
from .models import Ticket,ticketAssign,ticketConversation

# Register your models here.
admin.site.register([Ticket,ticketAssign,ticketConversation])
