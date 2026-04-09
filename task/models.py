from django.db import models
from django.contrib.auth.models import User
class TaskUser(User):
    phone_number =  models.CharField(unique = True , max_length= 100)
    email_token = models.CharField(max_length = 100 ,null = True , blank=True)
    # otp = models.CharField(max_length = 10 , null = True , blank = True)
    # is_verified = models.BooleanField(default = False)
    # otp = models.CharField(max_length = 10 , null = True , blank = True)

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name
    
class Tasks(models.Model):
    task_name  = models.CharField(max_length = 100)
    task_description = models.TextField()
    task_slug = models.SlugField(max_length = 1000 , unique  = True)
    task_owner = models.ForeignKey(TaskUser, on_delete = models.CASCADE , related_name = "owned_task")
    task_creater = models.ForeignKey(TaskUser, on_delete = models.CASCADE , related_name = "created_task")
    task_status  = models.CharField(max_length = 100)
    task_priority  = models.CharField(max_length = 100)
    task_active = models.BooleanField(default=True)
    task_due_date = models.DateField()

    def __str__(self) -> str:
        return self.task_name

