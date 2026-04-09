from django.shortcuts import render,redirect,HttpResponse,HttpResponsePermanentRedirect,get_object_or_404,HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from .utils import generateRandomToken,sendEmailToken,sendOTPtoEmail,generateSlug
from django.db.models import Q
import random
from django.utils.text import slugify
import uuid

# from stayvia.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET,RAZORPAY_CALLBACK_URL
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@login_required(login_url='login_page')
def index(request):
    tasks = Tasks.objects.filter((Q(task_owner=request.user) | Q(task_creater=request.user)) & Q(task_active=True))
    name=request.user.get_full_name()
    x = Tasks.objects.filter(task_owner__id=request.user.id,task_status='todo').count()
    y = Tasks.objects.filter(task_owner__id=request.user.id,task_status='in_progress').count()
    z = Tasks.objects.filter(task_owner__id=request.user.id,task_status='done').count()
    print(x)
    print(y)
    print(z)
    context = {'tasks': tasks, 'name':name, 'x':x,'y':y,'z':z}
    print(request.user.get_full_name())
    return render(request, 'index.html', context)
    # return render(request, 'index.html', context = {})

def about(request):
    return render(request, 'about.html')

def register(request):
    print("in register")
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if first_name == "" or last_name=="" or email=="" or password=="" or phone_number=="":
            messages.warning(request, "All Fields are mandatory")
            return redirect('/register/')


        hotel_user = TaskUser.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/register/')

        hotel_user = TaskUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
        )
        hotel_user.set_password(password)
        hotel_user.save()

        messages.success(request, "Registered successfully")
        return redirect('/login/')

    return render(request, 'register.html')

def login_page(request):    
    if request.method == "POST":
        print("in login accounts.view")
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')

        hotel_user = TaskUser.objects.filter(email = email)


        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('login_page')

        # if not hotel_user[0].is_verified:
        #     messages.warning(request, "Account not verified")
        #     return redirect('login_page')

        hotel_user = authenticate(username = hotel_user[0].username , password=password)

        if hotel_user:
            login(request , hotel_user)
            return redirect('/')

        messages.warning(request, "Invalid credentials")
        return redirect('login_page')
    print("not in if")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logout Success")

    return redirect('/')

def generateSlug(task_name):
    slug = f"{slugify(task_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Tasks.objects.filter(task_slug = slug).exists():
        return generateSlug(task_name)
    return slug

@login_required(login_url='login_page')
def add_task(request):
    name=request.user.get_full_name()
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        task_owner=  TaskUser.objects.get(id = request.user.id)
        task_creater = TaskUser.objects.get(id = request.user.id)
        task_status  =  request.POST.get('task_status')
        task_priority  =  request.POST.get('task_priority')
        task_slug = generateSlug(task_name)
        task_due_date = request.POST.get('task_due_date')

        # tasks_owner= TaskUser.objects.filter(email = task_owner_email)
        # task_owner=  TaskUser.objects.get(id = tasks_owner.id)

        Tasks_obj = Tasks.objects.create(
            task_name = task_name,
            task_description = task_description,
            task_owner = task_owner,
            task_creater = task_creater,
            task_status = task_status,
            task_priority = task_priority,
            task_slug = task_slug,
            task_due_date=task_due_date
        )
        Tasks_obj.save()
        messages.success(request, "Task Created")
        return redirect('/add-task/')

    return render(request, 'add_task.html', context = {'name':name})


@login_required(login_url='login_page')
def assign_task(request):
    name=request.user.get_full_name()
    context = {
        "assign_flag": True,
        "name":name
    }
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        task_assignee_mail=  request.POST.get('task_assignee_mail')
        task_creater = TaskUser.objects.get(id = request.user.id)
        task_status  =  request.POST.get('task_status')
        task_priority  =  request.POST.get('task_priority')
        task_slug = generateSlug(task_name)
        task_due_date = request.POST.get('task_due_date')

        print(task_assignee_mail)
        tasks_owner = get_object_or_404(TaskUser, email=task_assignee_mail)
        # tasks_owner= TaskUser.objects.filter(email = task_assignee_mail)
        # task_owner=  TaskUser.objects.get(id = tasks_owner.id)
        if not tasks_owner :
            messages.warning(request, "No Assignee Found.")
            return redirect('/assign-task/')
        
        Tasks_obj = Tasks.objects.create(
            task_name = task_name,
            task_description = task_description,
            task_owner = tasks_owner,
            task_creater = task_creater,
            task_status = task_status,
            task_priority = task_priority,
            task_slug = task_slug,
            task_due_date=task_due_date
        )
        Tasks_obj.save()
        messages.success(request, "Task Assigned")
        return redirect('/add-task/')

    return render(request, 'add_task.html', context)

@login_required(login_url='login_page')
def edit_task(request, slug):
    task_obj = Tasks.objects.get(task_slug=slug)
    if task_obj.task_active == False:
        return render(request, 'index.html', context)

    # Check if the current user is the owner of the hotel
    # if request.user not in [task_obj.task_creater, task_obj.task_owner]:
    if request.user.id not in [task_obj.task_creater.id, task_obj.task_owner.id]:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        task_status = request.POST.get('task_status')
        task_priority = request.POST.get('task_priority')
        task_due_date = request.POST.get('task_due_date')
        print(task_name)
        print(task_description)
        print(task_status)
        print(task_priority)
        print(task_due_date)
        # Update hotel object with new details
        task_obj.task_name = task_name
        task_obj.task_description = task_description
        task_obj.task_status = task_status
        task_obj.task_priority = task_priority
        task_obj.task_due_date = task_due_date
        task_obj.save()
        
        messages.success(request, "Task Updated")
        return HttpResponseRedirect(request.path_info)

    assign_flag=False
    assigner_flag=False
    if task_obj.task_owner != task_obj.task_creater:
        assign_flag=True
        if request.user.id == task_obj.task_creater.id:
            assigner_flag=True
    return render(request, 'edit_task.html', context={'task': task_obj , "assign_flag":assign_flag, "assigner_flag":assigner_flag})

@login_required(login_url='login_page')
def all_task(request):
    name=request.user.get_full_name()
    task_obj = Tasks.objects.filter(
        Q(task_creater__id=request.user.id) | Q(task_owner__id=request.user.id),task_active=True
    )

    return render(request, 'all_task.html',context={'task_list':task_obj,'name':name})




@login_required(login_url='login_page')
def delete_task(request, slug):
    print("in delete")
    task_obj = Tasks.objects.get(task_slug=slug)


    if request.user.id not in [task_obj.task_creater.id, task_obj.task_owner.id]:
        return HttpResponse("You are not authorized")

    if task_obj.task_owner != task_obj.task_creater:
        if request.user.id == task_obj.task_creater.id:
            task_obj.task_active = False
            task_obj.save()
            print("task active",task_obj.task_active)
            return redirect('/')
    
    if task_obj.task_owner == task_obj.task_creater:
        if request.user.id == task_obj.task_creater.id:
            task_obj.task_active = False
            task_obj.save()
            print("task active",task_obj.task_active)
            return redirect('/')
    messages.warning(request, "Unauthorized Action")
    return redirect('edit_task', slug=task_obj.task_slug)

