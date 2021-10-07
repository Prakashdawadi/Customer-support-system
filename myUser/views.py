from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from .form import UserCreationForm,LoginForm,CustomerProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myUser.models import User


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
        is_customer = 1
        is_caretaker = 0
        user = authenticate(email=email,password=password)
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
    return render(request,'customer/dashboard.html')

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
            form = CustomerProfile(request.POST,instance=user_id)
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
        return redirect('customerdashboard')
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
        return redirect('customerdashboard')
    loginForm = LoginForm(request.POST or None)
    data = {
        'form': loginForm
    }
    if loginForm.is_valid():

        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']
        is_customer = 1
        is_caretaker = 0
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, ' welcome to the dashboard')
            return redirect('caretakerdashboard')
        else:
            messages.add_message(request, messages.ERROR, "Credentials doesnot Match ")
            return render(request, 'caretaker/login.html', data)

    return render(request, 'caretaker/login.html', data)

def caretakerDashboard(request):
    pass

