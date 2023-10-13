from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from .managers import CustomUserManger
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group
# Create your models here.




class BaseModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(BaseModel):
    off_days=models.IntegerField(default=0)
    role_name=models.CharField(max_length=50,default="")
    def __str__(self):
        return str(self.role_name)



class Country(BaseModel):
    name=models.CharField(max_length=20)
    ioc=models.CharField(max_length=3)



class Employee(AbstractUser):
    EMPLOYMENT_TYPES = [
       ("part-time", "Part-time"),
       ("full-time", "Full-time")
    ]
    profile_picture_title = models.CharField(max_length=250,blank=True, null=True,default='defaultProfielPicture.jpg')
    profile_picture = models.ImageField(upload_to ='static/uploads/',blank=True, null=True,default='uploads/defaultProfielPicture.jpg')
    username = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=20,null=True,blank=True )
    address = models.CharField(max_length=150,null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)
    hourly_rate= models.FloatField(null=True,blank=True)
    leaves_left = models.IntegerField(default=12,null=True,blank=True)
    phone_number = PhoneNumberField(null=True,blank=True)
    email = models.EmailField(max_length=80, unique=True)
    role= models.ForeignKey(Role, on_delete=models.CASCADE)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManger()

    def __str__(self):
        return self.email
    

class Leaves(models.Model):
    LEAVE_CHOICES = [
        ("sick", "Sick"),
        ("personal", "Personal"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    leaving_days = models.IntegerField(default=0, blank=True, null=True)
    reason = models.CharField(max_length=20, choices=LEAVE_CHOICES)

    def __str__(self):
        return f"{self.employee} - {self.start_date} - {self.end_date} - {self.leaving_days} - {self.get_reason_display()}"



