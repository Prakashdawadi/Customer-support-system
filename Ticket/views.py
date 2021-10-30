from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from .form import ticketForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .models import Ticket,ticketAssign,ticketConversation
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

@login_required(login_url='customerlogin')
def createTicket(request):
    createTicket = ticketForm(request.POST or None,request.FILES or None)
    #print(request.POST)
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
    ticketList = Ticket.objects.all().filter(created_by_id = request.user.id,status=True,assignStatus=False).order_by('-updated_at')

    paginate = Paginator(ticketList, 4)
    page_url = request.GET.get('page')
    try:
        ticket_info = paginate.page(page_url)
    except PageNotAnInteger:
        ticket_info = paginate.page(1)
    except EmptyPage:
        ticket_info = paginate.page(paginate.num_pages)
    data= {
        'ticketList':ticket_info,
        'range': paginate
    }
    return render(request,'customer/ticket/list_ticket.html',data)

# customer view details view
@login_required(login_url='customerlogin' or 'caretakerlogin')
def viewDetails(request,id):

    try:
        findId = get_object_or_404(Ticket,id=id)
        # check whether the ticket is seen by authorized caretaker or not
        caretaker_details=ticketAssign.objects.select_related('caretakerId').filter(caretakerId=request.user.id, ticketId=id)
        if request.user.is_Caretaker and findId.assignStatus and not caretaker_details:
            messages.add_message(request, messages.ERROR, " you have not assigned this ticket")
            return redirect('caretakerdashboard')
        # check whether the customer is authorized to view this ticket or not
        print(request.user.id)
        print(findId.created_by_id)
        if request.user.is_customer and not request.user.id == findId.created_by_id:
            messages.add_message(request, messages.ERROR, " you have not created this ticket")
            return redirect('customerdashboard')

        if not findId.status:
            if request.user.is_Caretaker:
                messages.add_message(request, messages.ERROR, " Sorry! The ticket is closed")
                return redirect('solve_ticket_list')
            else:
                messages.add_message(request, messages.ERROR, "Sorry! The ticket is closed")
                return redirect('solved_ticket')

    except Exception as e:
            messages.add_message(request, messages.ERROR, e)
            return redirect('list_ticket')

    if request.user.is_Caretaker:
       caretakerAssignedOrNot=ticketAssign.objects.select_related('caretakerId').filter(caretakerId=request.user.id, ticketId=id)
       if caretakerAssignedOrNot:
            #caretaker is assgigned to that ticket now we can display conversation
            message_info = ticketConversation.objects.filter(ticket_id=id)
            data = {
                'caretakerAssignedOrNot':caretakerAssignedOrNot,
                'ticketInfo':findId,
                'messages_info':message_info
            }
            return render(request, 'customer/ticket/ticket_details.html',data)

       else:
            #only ticket details seen by careataker
            data = {

                'ticketInfo': findId
            }
            return render(request, 'customer/ticket/ticket_details.html',data)

    else:
        caretakerAssignedOrNot = ticketAssign.objects.select_related('caretakerId').filter(customerId=request.user.id,
                                                                                           ticketId=id)
        if caretakerAssignedOrNot:
            # caretaker is assgigned to that ticket now we can display conversation
            message_info = ticketConversation.objects.filter(ticket_id=id)
            data = {
                'caretakerAssignedOrNot': caretakerAssignedOrNot,
                'ticketInfo': findId,
                'messages_info': message_info
            }
            return render(request, 'customer/ticket/ticket_details.html', data)

        else:
            # only ticket details seen by careataker
            data = {

                'ticketInfo': findId
            }
            return render(request, 'customer/ticket/ticket_details.html', data)






@login_required(login_url='caretakerlogin')
def incomingTicket(request):

    ticket = Ticket.objects.filter(status=True,assignStatus=False).order_by('id')
    ticket_list = Paginator(ticket,4)
    page_url = request.GET.get('page')

    try:
        ticket_info = ticket_list.page(page_url)
    except PageNotAnInteger:
        ticket_info = ticket_list.page(1)
    except EmptyPage:
        ticket_info = ticket.page(ticket.num_pages)

    data = {
        'ticketList':ticket_info,
        'range':ticket_list
    }
    return render(request, 'caretaker/tickets/incoming_tickets.html', data)

@login_required(login_url='caretakerlogin')
def ticketAssigns(request):
    if request.POST:
        ticket_id    =  request.POST['ticket']
        caretaker_id = request.POST['caretaker']
        customer_id  =  request.POST['customer']
        already_assign = ticketAssign.objects.filter(ticketId_id = ticket_id).exists()
        if already_assign:
            #print(already_assign)
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
    assign_ticket = Ticket.objects.filter(id__in=bag, status=True).order_by('id')
    paginate = Paginator(assign_ticket,4)
    page_url = request.GET.get('page')
    try:
        ticket_info = paginate.page(page_url)
    except PageNotAnInteger:
        ticket_info = paginate.page(1)
    except EmptyPage:
        ticket_info = paginate.page(paginate.num_pages)
    data ={
        'assign':ticket_info,
        'range': paginate
    }
    return render(request,'caretaker/tickets/assign_ticket.html',data)

@login_required(login_url="customerlogin")
def deleteTicket(request,id):
    if request.user.is_customer:
        findId = Ticket.objects.get(pk=id)
        #print(findId)
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
            #print(title)
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
    #print(request.POST)

    if request.method == "POST":
        content = request.POST['textarea']
        if content == '':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #print(request.POST)
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
    messages.add_message(request,messages.SUCCESS ,"Ticket has been closed successfully")
    return redirect('solve_ticket_list')

@login_required(login_url="caretakerlogin")
def solvedClosedList(request):
    #before closing a ticket we must ensure which tickets has been assigned to login user
    assign_ticket_list = ticketAssign.objects.select_related('ticketId').filter(caretakerId=request.user.id)
    #print(solved_ticket_list.count())
    bag = []
    for s in assign_ticket_list:
        result = (s.ticketId.id)
        bag.append(result)
    #choose the tickets that are closed only from assigned list bag
    close_ticket = Ticket.objects.filter(id__in=bag,status=False).order_by('-updated_at')

    paginate = Paginator(close_ticket, 4)
    page_url = request.GET.get('page')
    try:
        ticket_info = paginate.page(page_url)
    except PageNotAnInteger:
        ticket_info = paginate.page(1)
    except EmptyPage:
        ticket_info = paginate.page(paginate.num_pages)


    data = {
    'info': ticket_info,
    'range': paginate
    }
    return render(request,'caretaker/tickets/solved_tickets.html',data)

@login_required(login_url="customerlogin")
def assignTicket(request):
    # before closing a ticket we must ensure which tickets has been assigned to login user
    assign_ticket = Ticket.objects.filter(created_by=request.user.id, status=True, assignStatus=True)
    paginate = Paginator(assign_ticket, 4)
    page_url = request.GET.get('page')
    try:
        ticket_info = paginate.page(page_url)
    except PageNotAnInteger:
        ticket_info = paginate.page(1)
    except EmptyPage:
        ticket_info = paginate.page(paginate.num_pages)

    data = {
        'info': ticket_info,
        'range':paginate,
    }
    return render(request,'customer/ticket/assign_ticket.html',data)

@login_required(login_url="customerlogin")
def solvedTicket(request):
    # before closing a ticket we must ensure which tickets has been assigned to login user
    solvedTicket = Ticket.objects.filter(created_by=request.user.id,status=False,assignStatus=True)
    paginate = Paginator(solvedTicket, 4)
    page_url = request.GET.get('page')
    try:
        ticket_info = paginate.page(page_url)
    except PageNotAnInteger:
        ticket_info = paginate.page(1)
    except EmptyPage:
        ticket_info = paginate.page(paginate.num_pages)

    data = {
        'info': ticket_info,
        'range':paginate
    }
    return render(request,'customer/ticket/solved_ticket.html',data)










