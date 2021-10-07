from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .form import ticketForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .models import Ticket

# Create your views here.

@login_required(login_url='customerlogin')
def createTicket(request):
    createTicket = ticketForm(request.POST or None,request.FILES or None)
    if createTicket.is_valid():
        user = createTicket.save()
        user.status= True
        user.created_by_id = request.user.id
        user.save()
        messages.add_message(request,messages.SUCCESS,'ticket is created')
        return redirect('list_ticket')

    data = {
        'ticket_info': createTicket
    }

    return render(request,'customer/ticket/create_ticket.html',data)
@login_required(login_url='customerlogin')
def listTicket(request):
    ticketList = Ticket.objects.all().filter(created_by_id = request.user.id)
    data= {
        'ticketList':ticketList
    }
    return render(request,'customer/ticket/list_ticket.html',data)

@login_required(login_url='customerlogin')
def viewDetails(request,id):
    print(id)
    return render(request,'customer/ticket/ticket_details.html')
