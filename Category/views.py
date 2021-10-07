from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import categoryForm
from .models import Category

# Create your views here.
@login_required(login_url='caretakerlogin')
def createCategory(request):
    form = categoryForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        user = form.save()
        user.created_by_id = request.user.id
        user.save()
        messages.add_message(request,messages.SUCCESS, 'Category has been successfully created')
        return redirect('list_category')


    data = {
        'form':form
    }
    return render(request,'caretaker/category/create_category.html',data)

@login_required(login_url='caretakerlogin')
def listCategory(request):
    category = Category.objects.all().order_by('-id')
    data = {
        'category':category
    }
    return render(request,'caretaker/category/list_category.html',data)

# @login_required(login_url='caretakerlogin')
def deleteCategory(request,id):
    user_info = Category.objects.get(id=id)
    if not user_info:
        messages.add_message(request,messages.ERROR,"cannot delete at this moment")
        return redirect('list_category')
    delete_data =  user_info.delete()
    if delete_data:
        messages.add_message(request, messages.ERROR, "category has been deleted")
        return redirect('list_category')





