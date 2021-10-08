from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.urls import reverse
from .form import ticketForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .models import Ticket,ticketAssign

# Create your views here.

@login_required(login_url='customerlogin')
def createTicket(request):
    createTicket = ticketForm(request.POST or None,request.FILES or None)
    print(request.POST)
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
    ticketList = Ticket.objects.all().filter(created_by_id = request.user.id).order_by('-id')
    data= {
        'ticketList':ticketList
    }
    return render(request,'customer/ticket/list_ticket.html',data)

@login_required(login_url='customerlogin' or 'caretakerlogin')
def viewDetails(request,id):
    ticketInfo = Ticket.objects.get(id=id)
    data = {
        'ticketInfo': ticketInfo
    }
    if request.user.is_Caretaker:
        return render(request, 'customer/ticket/ticket_details.html', data)

    # to validate that the valid user is searching its details
    if not request.user.id == ticketInfo.created_by_id:
        messages.add_message(request,messages.ERROR,'Invalid url')

        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseRedirect(reverse('list_ticket'))

        #return redirect('list_ticket')

    return render(request,'customer/ticket/ticket_details.html',data)


@login_required(login_url='caretakerlogin')
def incomingTicket(request):

    ticketList = Ticket.objects.all().filter(status=True).order_by('-id')
    joininfo = ticketAssign.objects.filter(status=True).select_related('ticketId')
    print(joininfo)
    # try:
    #
    #     data = {
    #     'ticketList': ticketList,
    #     'ticket_info':ticket_info
    #      }
    #     return render(request,'caretaker/tickets/incoming_tickets.html',data)
    # except:
    data = {
    'ticketList': ticketList,
     }
    return render(request, 'caretaker/tickets/incoming_tickets.html', data)



def ticketAssigns(request,id,tid):

    print(id)
    print(tid)
    insert = ticketAssign(caretakerId_id=id, ticketId_id=tid,status=True)
    insert.save()
    ticket_info = ticketAssign.objects.all().get(id=tid, status=True)

    messages.add_message(request, messages.SUCCESS,'successfully assign now you can chat with this customer')
    return redirect('incoming_ticket')







