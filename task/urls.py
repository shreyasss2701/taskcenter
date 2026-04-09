from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('login/' , views.login_page, name='login_page'),
    path('about/', views.about, name="about"),
    path('logout/' , views.logout_view , name="logout_view"),
    path('register/' , views.register, name='register'),
    path('add-task/', views.add_task , name="add_task"),
    path('assign-task/', views.assign_task , name="assign_task"),
    path('all_task/', views.all_task , name="all_task"),
    path('edit-task/<slug>/', views.edit_task , name="edit_task"),
    path('delete-task/<slug>/', views.delete_task , name="delete_task")

    # path('delete-task/', views.add_task , name="add_task"),


]