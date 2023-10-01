from django.contrib import admin
from .models import Employee,Leaves,Country,Role

# Register your models here
class RoleAdmin(admin.ModelAdmin):
    list_display=['role_name','off_days']
    search_fields=['role_name']
    list_filter=['off_days']
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','phone_number','role','start_date','leaves_left','employment_type']
    search_fields=['first_name','last_name','email','phone_number']
    list_filter=['role','start_date','leaves_left','role','employment_type']

class LeavesAdmin(admin.ModelAdmin):
    list_display=['employee','date','reason']
    search_fields=['employee','date']
    list_filter=['date','reason']   


class CountryAdmin(admin.ModelAdmin):
    list_display=['name','ioc']
    search_fields=['name']
    list_filter=['name']       

admin.site.register(Role, RoleAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Leaves,LeavesAdmin)
admin.site.register(Country,CountryAdmin)