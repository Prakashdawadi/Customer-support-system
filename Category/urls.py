from django.urls import path
from . import views

#category urls are listed

urlpatterns = [
    path('caretaker/create-category',views.createCategory,name='create_category'),
    path('caretaker/list-category', views.listCategory, name='list_category'),
    path('caretaker/delete/<int:id>/',views.deleteCategory,name='delete_category')


]