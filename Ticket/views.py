from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from .form import ticketForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .models import Ticket,ticketAssign,ticketConversation

# Create your views here.

@login_required(login_url='customerlogin')
def createTicket(request):
    createTicket = ticketForm(request.POST or None,request.FILES or None)
    print(request.POST)
    if createTicket.is_valid():
        user = createTicket.save()
        user.status= True
        user.assignStatus =False
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

# customer view details view
@login_required(login_url='customerlogin' or 'caretakerlogin')
def viewDetails(request,id):
    ticketInfo = Ticket.objects.get(id=id)
    if request.user.is_Caretaker:

        #Cartakers also view the details of all incoming tickets but not assign tickets
        caretakerAassignedOrNot = ticketAssign.objects .select_related('caretakerId') .filter(caretakerId=request.user.id, ticketId=id)
        ticketInfo = Ticket.objects.get(id=id)
        if not ticketInfo.status:
            messages.add_message(request, messages.ERROR, "the ticket is closed")
            return redirect('close_ticket')

        if caretakerAassignedOrNot:
             messages_info= ticketConversation.objects.all().filter(ticket_id=id)
             print(messages_info.count())
             print(ticketInfo.status)
             counts= messages_info.count()
             if counts == 1:
                 data = {
                 'ticketInfo': ticketInfo,
                 'caretakerAssignedornot': caretakerAassignedOrNot,
                 'messages_info':messages_info,
                 'counts':counts,
                 'ticket_status':ticketInfo.status,

                  }
                 return render(request, 'customer/ticket/ticket_details.html', data)
             else:
                 data = {
                     'ticketInfo': ticketInfo,
                     'caretakerAssignedornot': caretakerAassignedOrNot,
                     'messages_info': messages_info,
                     'ticket_status':ticketInfo.status,
                 }
                 return render(request, 'customer/ticket/ticket_details.html', data)

             return render(request, 'customer/ticket/ticket_details.html', data)
        else:
            data = {
               'ticketInfo': ticketInfo,
               'caretakerassign': caretakerAassignedOrNot
            }
            return render(request, 'customer/ticket/ticket_details.html', data)
    else:
        try:
            #print('before_try')
            key = get_object_or_404(Ticket,pk=id)

            if not request.user.id == ticketInfo.created_by_id:
                messages.add_message(request, messages.ERROR, 'Invalid url')
                return HttpResponseRedirect(reverse('list_ticket'))
            else:
                #user can also view the chatting box after being assigned so check whether that ticket is assigned or not
                caretaker_info = ticketAssign.objects \
                .select_related('caretakerId') \
                .filter(customerId=request.user.id, ticketId=id)
                ticketInfo = Ticket.objects.get(id=id)
                messages_info = ticketConversation.objects.all().filter(ticket_id=id)
                #print("hello")
                #print(ticketInfo.status)

                counts = messages_info.count()
                if counts == 1:
                    data = {
                        'ticketInfo': ticketInfo,
                        'caretaker': caretaker_info,
                        'messages_info': messages_info,
                        'counts':counts,

                    }
                    return render(request, 'customer/ticket/ticket_details.html', data)
                else:
                    data = {
                        'ticketInfo': ticketInfo,
                        'caretaker': caretaker_info,
                        'messages_info': messages_info,

                    }
                    return render(request, 'customer/ticket/ticket_details.html', data)
                return render(request, 'customer/ticket/ticket_details.html', data)
        except Exception as e:
            #print("exceptss")
            messages.add_message(request, messages.ERROR, e)
            return redirect('list_ticket')




@login_required(login_url='caretakerlogin')
def incomingTicket(request):

       # to view the incoming ticket the caretaker must be online or available or no busy
       if request.user.is_Caretaker and request.user.caretaker_status == 'busy':
           return render(request, 'caretaker/tickets/incoming_tickets.html')

       # this is for whether the data exists in ticket assign table or not
       ticket_exists = ticketAssign.objects.select_related('ticketId').exists()
       if ticket_exists:
            incoming_ticket = Ticket.objects.filter(assignStatus=False)
            #print(incoming_ticket)
            data = {
            'ticket_info':incoming_ticket
            }
            return render(request, 'caretaker/tickets/incoming_tickets.html',data)
       else:
            ticketList = Ticket.objects.all().filter(status=True).order_by('-id')
            data = {
                'ticketList': ticketList,
            }
            #print("b")

            return render(request, 'caretaker/tickets/incoming_tickets.html', data)

@login_required(login_url='caretakerlogin')
def ticketAssigns(request):
    if request.POST:
        ticket_id    =  request.POST['ticket']
        caretaker_id = request.POST['caretaker']
        customer_id  =  request.POST['customer']
        already_assign = ticketAssign.objects.filter(ticketId_id = ticket_id).exists()
        if already_assign:
            print(already_assign)
            messages.add_message(request,messages.ERROR,'this ticket is already been assign by another caretaker')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        insert = ticketAssign(ticketId_id=ticket_id,caretakerId_id=caretaker_id,customerId_id = customer_id,  status=True)
        insert.save()
        insertStatus = Ticket.objects.get(id=ticket_id)
        insertStatus.assignStatus = True
        insertStatus.save()
        messages.add_message(request, messages.SUCCESS,'successfully assign now you can chat with this customer')
        return redirect('assign_list')

@login_required(login_url='caretakerlogin')
def assignList(request):
    assign_ticket_info = ticketAssign.objects.select_related('ticketId').filter(caretakerId= request.user.id)
    bag = []
    for s in assign_ticket_info:
        result = (s.ticketId.id)
        bag.append(result)
    #print(bag)
    assign_ticket = Ticket.objects.filter(id__in=bag, status=True)
    # print(close_ticket)
    print(assign_ticket_info)
    data ={
        'assign':assign_ticket
    }
    return render(request,'caretaker/tickets/assign_ticket.html',data)

# # view details section by caretaker
# @login_required(login_url='caretakerlogin')
# def assignedTicketviewDetails(request,id):
#
#     if request.user.is_Caretaker:
#         ticketId_exists = ticketAssign.objects.filter(ticketId=id, caretakerId=request.user.id).exists()
#         # with assign view details and display conversation section
#         if (ticketId_exists):
#             ticket_Info = Ticket.objects.get(id=id)
#             caretaker_info = ticketAssign.objects.select_related('caretakerId').filter(caretakerId=request.user.id,ticketId=id)
#             data = {
#                 'ticket_info': ticket_Info,
#                 'assigner_name':caretaker_info
#
#             }
#             print(caretaker_info)
#
#             return render(request, 'caretaker/tickets/assign_ticket_viewdetails.html', data)
#         else:
#             # without assign view details section
#             ticketInfo = Ticket.objects.get(id=id)
#             data = {
#                 'ticketInfo': ticketInfo
#             }
#             return render(request, 'caretaker/tickets/assign_ticket_viewdetails.html', data)
#     else:
#         messages.add_message(request,messages.ERROR,'cannot details at this moment')
#         return redirect(request, 'caretakerdashboard')

@login_required(login_url="customerlogin")
def deleteTicket(request,id):
    if request.user.is_customer:
        findId = Ticket.objects.get(pk=id)
        print(findId)
        findId.delete();
        messages.add_message(request,messages.SUCCESS,"Tickets has been deleted successfully")
        return redirect('list_ticket')

    return redirect('customerlogin')

@login_required(login_url="customerlogin")
def editTicket(request,id):
    try:
        findId = get_object_or_404(Ticket,pk=id)
        if not request.user.id == findId.created_by_id:
            messages.add_message(request, messages.SUCCESS, "invalid-urls")
            return render(request, 'customer/ticket/edit_ticket.html')
        form =ticketForm(instance=findId)
        data = {
            'form':form
        }
        if request.method == "POST":
            #print(request.POST)
            title = str(request.POST.get('subject'))
            title_length = len(title)
            print(title)
            description = len(str(request.POST.get('description')))
            if title == '' or title_length<5:
                messages.add_message(request, messages.ERROR, "Title should not empty and must be of 4 letter")
                return render(request, 'customer/ticket/edit_ticket.html',data)

            form = ticketForm(request.POST or None, request.FILES or None,instance=findId)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Ticket has been updated successfully')
                return redirect('list_ticket')

        return render(request, 'customer/ticket/edit_ticket.html', data)
    except  Exception as e:
        messages.add_message(request, messages.SUCCESS, e)
        return render(request, 'customer/ticket/edit_ticket.html')


    return render(request,'customer/edit_ticket.html')

# message section

@login_required(login_url='customerlogin or caretakerlogin')
def customerMessage(request):
    print(request.POST)

    if request.method == "POST":
        content = request.POST['textarea']
        if content == '':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        print(request.POST)
        tickets = request.POST['ticket']
        caretakers = request.POST['caretaker']
        customers = request.POST['customer']

        insert = ticketConversation(customer_id_id=customers,
                                      caretaker_id_id=caretakers,
                                      ticket_id_id=tickets,
                                      message=content,
                                    msg_created_by_id = request.user.id)
        insert.save()
            # messages.add_message(request,messages.success,'added successfully')
        return redirect('view_details',tickets)
    messages.add_message(request,messages.ERROR,'cannot add msg')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="caretakerlogin")
def closeTicket(request):
    print(request.POST.get('ticketId'))
    ticket_info  = Ticket.objects.filter(pk=request.POST.get('ticketId')).update(status=False)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="caretakerlogin")
def solvedClosedList(request):
    #before closing a ticket we must ensure which tickets has been assigned to login user
    assign_ticket_list = ticketAssign.objects.select_related('ticketId').filter(caretakerId=request.user.id)
    #print(solved_ticket_list.count())
    bag = []
    for s in assign_ticket_list:
        result = (s.ticketId.id)
        bag.append(result)
    #print(bag)
    #choose the tickets that are closed only from assigned list bag
    close_ticket = Ticket.objects.filter(id__in=bag,status=False)
    #print(close_ticket)

    data = {
    'info': close_ticket
    }
    return render(request,'caretaker/tickets/solved_tickets.html',data)

@login_required(login_url="customerlogin")
def assignTicket(request):
    return render(request,'customer/ticket/assign_ticket.html')

@login_required(login_url="customerlogin")
def solvedTicket(request):
    return render(request,'customer/ticket/solved_ticket.html')










