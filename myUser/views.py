from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from .form import UserCreationForm,LoginForm,CustomerProfile,changePasswordForm
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
        user = authenticate(email=email,password=password)
        user_info = User.objects.get(email=email)
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
        return render(request,'customer/dashboard.html')
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
    print(request.POST)
    print(request.FILES)
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
        user_info = User.objects.get(email=email)
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
        return render(request,'caretaker/dashboard.html')
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
    print(request.POST)
    print(request.FILES)
    if not id==request.user.id:
        messages.add_message(request,messages.ERROR,"Invalid url")
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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

@login_required(login_url='caretakerlogin')
def  caretakerChangePassword(request):
    form = changePasswordForm()

    data = {
        'form' :form
    }

    # if request.method == "POST" and request.POST :
    #     oldPassword =  request.POST['old_password']
    #     newPassword = request.POST['new_password']
    #     confirmPassword = request.POST['confirm_password']
    #     if oldPassword == '' or newPassword ==  '' or confirmPassword == '' :
    #         messages.add_message(request,messages.ERROR,'Fields should not empty')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #
    #     if len(str(newPassword)) < 5:
    #         messages.add_message(request, messages.ERROR, 'new password should be of length 5')
    #
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #     if newPassword!=confirmPassword:
    #         messages.add_message(request, messages.ERROR, 'new pass word and confrm password must be same')
    #
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






    return render(request, 'caretaker/change_password.html',data)
