from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import categoryForm
from .models import Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

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
    category = Category.objects.all().order_by('-updated_at')
    all_category = Paginator(category,4)
    page_url = request.GET.get('page')
    #print(all_category)
    try:
        cats_info = all_category.page(page_url)
    except PageNotAnInteger:
        cats_info = all_category.page(1)
    except EmptyPage:
        cats_info = all_category.page(all_category.num_pages)


    data = {
        'category':cats_info,
        'range':all_category
    }
    return render(request,'caretaker/category/list_category.html',data)

@login_required(login_url='caretakerlogin')
def deleteCategory(request,id):
    user_info = Category.objects.get(id=id)
    if not user_info:
        messages.add_message(request,messages.ERROR,"cannot delete at this moment")
        return redirect('list_category')
    delete_data =  user_info.delete()
    if delete_data:
        messages.add_message(request, messages.ERROR, "category has been deleted")
        return redirect('list_category')
@login_required(login_url="caretakerlogin")
def editCategory(request,id):

    try:
        find_id = Category.objects.get(id=id)
        form = categoryForm(request.POST or None, instance=find_id)
        title = len (str(request.POST.get('category')))
        if title == '' or  title <4:
            messages.add_message(request, messages.ERROR, "title mustnot be empty and of 4 length")
        if form.is_valid():
            update = form.save()
            messages.add_message(request, messages.SUCCESS, "updated successfully")
            return redirect("list_category")


        data = {
            'form':form
        }

        return render(request,'caretaker/category/edit_category.html',data)
    except Exception as e:
         messages.add_message(request,messages.ERROR, e)
         return redirect("list_category")

    return render(request,'caretaker/category/edit_category.html')









