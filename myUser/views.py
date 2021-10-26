from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from .form import UserCreationForm,LoginForm,CustomerProfile,changePasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myUser.models import User
from Ticket.models import Ticket, ticketAssign
from django.contrib.auth.hashers import check_password


# Create your views here.

#--------------------------------------------------------
# customer sections
def customerSignup(request):
    if request.user.is_authenticated:
        return redirect('customerdashboard')
    form = UserCreationForm(request.POST or None)
    data = {
        'form': form
    }
    if request.POST:

        #validation the contact number
        contact_no = str(request.POST.get('phone_no'))
        check = contact_no.isdigit()

        length = len(str(contact_no))

        if (check == True and length == 10):

            # form is now complete valid
            if form.is_valid():
                user = form.save()
                user.is_customer =True
                user.is_Caretaker =False
                user.set_password(request.POST.get('password'))
                user.save()
                messages.add_message(request, messages.SUCCESS, "Sign up successfully")
                return redirect('customerlogin')
            else:
                return render(request, 'customer/signup.html',data)
        else:
            messages.add_message(request, messages.ERROR, "User contact number will be of 10 digits")
            return render(request, 'customer/signup.html', data)

    else:
        return render(request,'customer/signup.html',data)

def customerLogin(request):
    if request.user.is_authenticated:
       return redirect('customerdashboard')
    loginForm = LoginForm(request.POST or None)

    data = {
        'form': loginForm
    }
    if loginForm.is_valid():
        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']
        user = authenticate(email=email,password=password)
        try:
            user_info = User.objects.get(email=email)
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Sorry! your email address is wrong")
            return render(request, 'customer/login.html', data)

        if not user_info.is_customer:
            messages.add_message(request, messages.ERROR, 'you r not a customer')
            return render(request, 'customer/login.html', data)
        if user is not None:
            login(request, user)
            messages.add_message(request,messages.SUCCESS,' welcome to the dashboard')
            return redirect('customerdashboard')
        else:
            messages.add_message(request,messages.ERROR,"Credentials doesnot Match ")
            return render(request,'customer/login.html',data)

    return render(request,'customer/login.html',data)

@login_required(login_url='customerlogin')
def customerDashboard(request):
    if request.user.is_customer:
        total_ticket_created = Ticket.objects.filter(created_by_id = request.user.id)
        total_ticket_assigned = Ticket.objects.filter(created_by_id=request.user.id,assignStatus= True )
        total_solved_assigned = Ticket.objects.filter(created_by_id=request.user.id,status= False )
        total_pending_ticket = Ticket.objects.filter(created_by_id=request.user.id,status= True,assignStatus=False )
        print(total_solved_assigned.count())
        data = {
            'total_ticket': total_ticket_created.count(),
            'total_assigned':total_ticket_assigned.count(),
            'total_solved':total_solved_assigned.count(),
            'total_pending':total_pending_ticket.count()
        }
        return render(request,'customer/dashboard.html',data)
    else:
        return redirect('caretakerdashboard')


@login_required(login_url='customerlogin')
def customerLogout(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'Thank you for taking our services')
    return redirect('customerlogin')

@login_required(login_url='customerlogin')
def EditcustomerProfile(request,id):
    #p = get_object_or_404(User,id=id)
    if not id==request.user.id:
        messages.add_message(request,messages.ERROR,"Invalid url")
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('customerdashboard')
    user_id = User.objects.get(id=id)
    form = CustomerProfile(instance=user_id)
    data = {
        'form':form
    }
    contact_no = str(request.POST.get('phone_no'))
    check = contact_no.isdigit()

    length = len(str(contact_no))
    if request.POST:
        if (check == True and length == 10):
        # form is now complete valid
            form = CustomerProfile(request.POST, request.FILES or None, instance=user_id)
            if form.is_valid():
                user = form.save()
                messages.add_message(request, messages.SUCCESS, "user updated")
                return redirect('customerdashboard')

        else:
            messages.add_message(request, messages.ERROR, "User contact number will be of 10 digits")
            return render(request, 'customer/customerprofile.html', data)

    return render(request, 'customer/customerprofile.html',data)

#caretaker section

def caretakerSignup(request):
    if request.user.is_authenticated:
        return redirect('caretakerdashboard')
    form = UserCreationForm(request.POST or None)
    data = {
        'form': form
    }
    if request.POST:

        # validation the contact number
        contact_no = str(request.POST.get('phone_no'))
        check = contact_no.isdigit()

        length = len(str(contact_no))

        if (check == True and length == 10):

            # form is now complete valid
            if form.is_valid():
                user = form.save()
                user.is_customer = False
                user.is_Caretaker = True
                user.set_password(request.POST.get('password'))
                user.caretaker_status= "available"
                user.save()
                messages.add_message(request, messages.SUCCESS, "Sign up successfully")
                return redirect('caretakerlogin')
            else:
                return render(request, 'caretaker/signup.html', data)
        else:
            messages.add_message(request, messages.ERROR, "User contact number will be of 10 digits")
            return render(request, 'caretaker/signup.html', data)

    else:
        return render(request, 'caretaker/signup.html', data)

def caretakerLogin(request):
    if request.user.is_authenticated:
        return redirect('caretakerdashboard')
    loginForm = LoginForm(request.POST or None)
    data = {
        'form': loginForm
    }
    if loginForm.is_valid():
        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']
        user = authenticate(email=email, password=password)
        try:
            user_info = User.objects.get(email=email)
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Sorry! your email address is wrong")
            return render(request, 'caretaker/login.html', data)

        if not user_info.is_Caretaker:
            messages.add_message(request, messages.ERROR, 'you r not a Caretaker')
            return render(request, 'caretaker/login.html', data)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, ' welcome to the caretaker dashboard')
            return redirect('caretakerdashboard')
        else:
            messages.add_message(request, messages.ERROR, "Credentials does not Match ")
            return render(request, 'caretaker/login.html', data)

    return render(request, 'caretaker/login.html', data)

@login_required(login_url='caretakerlogin')
def caretakerDashboard(request):
    if request.user.is_Caretaker:
        total_ticket = Ticket.objects.all()
        incoming_ticket = Ticket.objects.filter(assignStatus=False)
        assign_ticket_info = ticketAssign.objects.select_related('ticketId').filter(caretakerId=request.user.id)
        bag = []
        for s in assign_ticket_info:
            result = (s.ticketId.id)
            bag.append(result)
        assign_ticket = Ticket.objects.filter(id__in=bag, status=True)
        solved_ticket = Ticket.objects.filter(id__in=bag, status=False)
        data = {
            'total_ticket':total_ticket.count(),
            'incoming_ticket':incoming_ticket.count(),
            'assign_ticket':assign_ticket.count(),
            'solved_ticket':solved_ticket.count(),
        }
        return render(request,'caretaker/dashboard.html',data)
    else:

        return redirect('customerdashboard')

@login_required(login_url='caretakerlogin')
def caretakerLogout(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,"Thank you taking and helping our customer")
    return redirect('caretakerlogin')


@login_required(login_url='caretakerlogin')
def EditCaretakerProfile(request,id):
    #p = get_object_or_404(User,id=id)
    if not id==request.user.id:
        messages.add_message(request,messages.ERROR,"Invalid url")
        return redirect('caretakerdashboard')
    user_id = User.objects.get(id=id)
    form = CustomerProfile(instance=user_id)
    data = {
        'form':form
    }
    contact_no = str(request.POST.get('phone_no'))
    check = contact_no.isdigit()

    length = len(str(contact_no))
    if request.POST:
        if (check == True and length == 10):
        # form is now complete valid
            form = CustomerProfile(request.POST, request.FILES or None, instance=user_id)
            if form.is_valid():
                user = form.save()
                messages.add_message(request, messages.SUCCESS, "user updated")
                return redirect('caretakerdashboard')

        else:
            messages.add_message(request, messages.ERROR, "User contact number will be of 10 digits")
            return render(request, 'caretaker/caretakerprofiles.html', data)

    return render(request, 'caretaker/caretakerprofiles.html',data)


login_required(login_url='caretakerlogin')
def changeStatus(request):
    if request.method =="POST" and request.POST and request.user.is_Caretaker:

        change_status = User.objects.get(pk=request.user.id)
        change_status.caretaker_status=request.POST.get('status')
        change_status.save()
    return redirect('caretakerdashboard')

@login_required(login_url="caretakelogin" or 'customerlogin')
def ChangePassword(request):
    form = changePasswordForm(request.POST or None)
    data= {
        'form':form
    }
    if request.method=="POST":
       old_pass = request.POST.get('old_password')
       new_pass = str(request.POST.get('password'))
       len_pass =len(new_pass)
       confirm_pass = request.POST.get('confirm_password')
       findUser = User.objects.get(pk=request.user.id)
       check_old_pass = check_password(old_pass,request.user.password)
       if check_old_pass==False :
           messages.add_message(request,messages.ERROR,'Incorrect  old password')
           return render(request,'customer/change_password.html',data)
       if new_pass == '' or len_pass <6:
           messages.add_message(request, messages.ERROR, 'password field must not be empty and of 5 character')
           return render(request, 'customer/change_password.html', data)
       if new_pass != confirm_pass:
           messages.add_message(request, messages.ERROR, 'new password and confirm password does not match')
           return render(request, 'customer/change_password.html', data)
       if new_pass == confirm_pass:
           findUser.set_password(request.POST.get('password'))
           findUser.save()
           user = User.objects.get(email=request.user.email)
           login(request,user)
           messages.add_message(request, messages.SUCCESS, 'password changed succesfully')
           if request.user.is_customer:
              return redirect('customerdashboard')
           else:
               return redirect('caretakerdashboard')


    return render(request ,'customer/change_password.html',data)
