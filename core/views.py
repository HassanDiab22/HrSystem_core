from django.shortcuts import render,redirect
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import time
from .models import Employee, Leaves,Role, Timesheet,Task
from .forms import EmployeeForm, LeaveForm,RoleForm,ProfileForm, TaskForm,TimesheetForm
from django.contrib import messages

from django.db.models import Q


class indexView(View):
    template_name = "index.html"
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser :
            return HttpResponseRedirect(reverse("core:admin"))
        elif request.user.is_authenticated:
            return HttpResponseRedirect(reverse("core:timesheets"))

        return render(request, self.template_name)


class CreateRoleView(View):
    template_name = "create/createRole.html"
    def get(self,request):
        return render(request, self.template_name)

class Login(View):
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse("core:admin"))
                else:
                    return HttpResponseRedirect(reverse("core:timesheets"))
            else:
                return HttpResponseRedirect(reverse("core:index"))
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
        
class Logout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("core:index"))
    
class AdminView(View):
    template_name = "dashboard.html"

    def get(self,request):
        # if request.user.is_authenticated and request.user.is_superuser :
        if request.user.is_authenticated :
            admins_count = Employee.objects.filter(is_superuser=True).count()
            employees_count = Employee.objects.filter(is_superuser=False, is_staff=False).count()
            leaves_today_count = Leaves.objects.filter(start_date=time.strftime("%Y-%m-%d")).count()
            roles_count = Role.objects.all().count()

            leaves=Leaves.objects.all()
            employees=Employee.objects.all()

            context = {
                'active_menu': 'dashboard',
                'leaves': leaves,
                'employees': employees,
                'admins_count': admins_count,
                'employees_count': employees_count,
                'leaves_count': leaves_today_count,
                'roles_count': roles_count,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
        


class RolesView(generic.ListView):
    
    template_name="adminAccessibilities/roles.html"
    
    def get(self,request):
        
        if request.user.is_authenticated and request.user.is_superuser :
            print(request.user.is_authenticated and request.user.is_superuser )
            roles=Role.objects.all()
            form=RoleForm()
            context={
                'active_menu': 'roles',
                'roles':roles,
             'form':form,
            }
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    def post(self,request):
        if request.user.is_authenticated and request.user.is_superuser :
            form=RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:roles"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def deleteRole(request, pk):
        if request.user.is_authenticated and request.user.is_superuser :
            pk = int(pk) 
            role = Role.objects.get(id=pk)
            role.delete()
            return HttpResponseRedirect(reverse("core:roles"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
    
    def updateRoleView(request, pk):
        if request.user.is_authenticated and request.user.is_superuser :
            if request.method == "GET":
                pk = int(pk)
                role = Role.objects.get(id=pk)
                form = RoleForm(instance=role)
                context = {'form': form}
                return render(request, 'adminAccessibilities/editRole.html', context)
            elif request.method == "POST":
                pk = int(pk)
                try:
                    role = Role.objects.get(id=pk)
                except Role.DoesNotExist:
                    role = None
                if role:
                    form = RoleForm(request.POST, instance=role)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect(reverse("core:roles"))
            else:
                return HttpResponseRedirect(reverse("core:index"))
    def searchRoles(request):
        if request.method == "GET":
            search_input = request.GET.get('table_search') 
            print(search_input)
            if search_input:
                roles = Role.objects.filter(Q(role_name__icontains=search_input) )
            else:
                roles = Role.objects.all()
            
            form=RoleForm()
            context={
                'roles':roles,
             'form':form,
            }
    
            return render(request,'adminAccessibilities/roles.html',context)
        
    
class ProfileView (generic.ListView):
    template_name="adminAccessibilities/profile.html"
    def get(self,request):
        if request.user.is_authenticated:
            context = {
                'active_menu': '',
                
            }
            return render(request,self.template_name,context)
    def updateProfile(request, pk):
        if request.user.is_authenticated :
            if request.method == "GET":
                pk = int(pk)
                employee = Employee.objects.get(id=pk)
                form = ProfileForm(instance=employee)
                context = {'form': form,
                           'active_menu': 'employees',}
                return render(request, 'adminAccessibilities/editProfile.html', context)
            if request.method == "POST":    
                email = request.POST.get('email')
                
                try:
                    employee = Employee.objects.get(email=email)
                except Employee.DoesNotExist:
                    employee = None
                if employee:
                    profiel_image= request.FILES.get('profile_picture')

                    if profiel_image: 
                         profiel_image_name = profiel_image.name
                    else:
                        profiel_image_name = "defaultProfielPicture.jpg"
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    phone_number = request.POST.get('phone_number')
                    address = request.POST.get('address')
                    employee.first_name=first_name
                    employee.last_name=last_name
                    employee.phone_number=phone_number
                    employee.address=address
                    employee.profile_picture_title=profiel_image_name
                    employee.profile_picture=profiel_image
                    print(profiel_image_name)
                    employee.save(update_fields=['first_name', 'last_name','phone_number','address','profile_picture_title','profile_picture'])     
                    return HttpResponseRedirect(reverse("core:profile"))
        else:
            return HttpResponseRedirect(reverse("core:index"))         

class TimesheetView(generic.ListView):
    template_name="adminAccessibilities/timesheet.html"
    
    def get(self,request):
        if request.user.is_authenticated:
            
            timesheets=Timesheet.objects.filter(employee=request.user)
            form = TimesheetForm()
            context = {
                'active_menu': 'timesheet',
                'form':form,
                'timesheets':timesheets,
            }
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    def post(self,request):
        if request.user.is_authenticated:
            post = request.POST.copy()
            post['employee'] = Employee.objects.get(email=request.user)
            request.POST = post
            form=TimesheetForm(request.POST) 
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("core:timesheets"))
            else:
                # print(form.errors.as_data())
                # print(form.errors.as_text())
                error_text = form.errors.as_text()
                error_messages = error_text.split('*')
                error_message = error_messages[2].strip()
                context = {
                    'active_menu': 'timesheet',
                    'form': form,
                    'timesheets': Timesheet.objects.filter(employee=request.user),
                    'error':error_message
                }
                return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
class TasksView(generic.ListView):
    template_name="adminAccessibilities/tasks.html"

    def get(self,request,pk):
        if request.user.is_authenticated:
            pk = int(pk) 
            tasks=Task.objects.filter(timesheet=pk)
            timesheet=Timesheet.objects.get(id=pk)
            form = TaskForm()
            context = {
                'active_menu': 'timesheet',
                'form':form,
                'tasks':tasks,
                'timesheet':timesheet
            }
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    def post(self,request,pk):
        if request.user.is_authenticated:
            post = request.POST.copy()
            pk = int(pk) 
            post['timesheet'] = Timesheet.objects.get(id=pk)
            request.POST = post
            form=TaskForm(request.POST) 

            if form.is_valid():
                form.save()
                timesheet=Timesheet.objects.get(id=pk)
                tasks=Task.objects.filter(timesheet=timesheet)
                total_hours=0.0
                for task in tasks:
                    total_hours+=task.duration
                timesheet.total_hours=total_hours
                timesheet.save()
                tasks_url = reverse("core:tasks", kwargs={'pk': pk})
                return HttpResponseRedirect(tasks_url)
            return HttpResponse(status=400)
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def updateTaskView(request, pk):
        if request.user.is_authenticated :
            if request.method == "GET":
                pk = int(pk)
                print(pk)
                task = Task.objects.get(id=pk)
                form = TaskForm(instance=task)
                context = {'form': form,
                           'active_menu': 'timesheet',}
                return render(request, 'adminAccessibilities/editTask.html', context)
            if request.method == "POST":    
                post = request.POST.copy()
                pk = int(pk) 
                print(pk)
                task = Task.objects.get(id=pk)
                post['timesheet'] = task.timesheet
                request.POST = post
                if task:
                    form = TaskForm(request.POST, instance=task)
                    if form.is_valid():
                        form.save()
                        timesheet=task.timesheet
                        tasks=Task.objects.filter(timesheet=timesheet)
                        total_hours=0.0
                        for task in tasks:
                            total_hours+=task.duration
                        timesheet.total_hours=total_hours
                        print(timesheet.total_hours)
                        timesheet.save()
                        tasks_url = reverse("core:tasks", kwargs={'pk': timesheet.id})
                        return HttpResponseRedirect(tasks_url)
                else:
                    return HttpResponseRedirect(reverse("core:index"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def deleteTask(request, pk):
           
           if request.user.is_authenticated :
               pk = int(pk) 
               task = Task.objects.get(id=pk)
               id=task.timesheet.id
               timesheet=task.timesheet
               task.delete()
               tasks=Task.objects.filter(timesheet=timesheet)
               total_hours=0.0
               for task in tasks:
                   total_hours+=task.duration
               timesheet.total_hours=total_hours
               timesheet.save()
               tasks_url = reverse("core:tasks", kwargs={'pk': id})
               return HttpResponseRedirect(tasks_url)
           else:
            return HttpResponseRedirect(reverse("core:index"))



        
class EmployeesView(generic.ListView):
    template_name="adminAccessibilities/employees.html"
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser :
            
            employees=Employee.objects.filter(is_superuser=False,is_staff=False)
            
            roles=Role.objects.all()
            employment_type = Employee.EMPLOYMENT_TYPES
            print(employment_type)
            form = EmployeeForm()
            context = {
                'active_menu': 'employees',
                'form':form,
                'Employees':employees,
                'roles':roles,
                'employment_type':employment_type,
            }
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def post(self,request): 
        if request.user.is_authenticated and request.user.is_superuser :
            country_code=request.POST.get('countryCode')
            phone_nb=request.POST.get('phone')
            post = request.POST.copy()
            post['phone_number'] = '+'+country_code+phone_nb
            post['hourly_rate'] = float(request.POST.get('hourly_rate'))
            request.POST = post
            form=EmployeeForm(request.POST) 
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(post['password'])
                form.save()
                return HttpResponseRedirect(reverse("core:employees"))
            else:
                error_text = form.errors.as_text()
                error_messages = error_text.split('*')
                error_message = error_messages[2].strip()
                print(error_message)
                context = {
                'active_menu': 'employees',
                'form':form,
                'Employees':Employee.objects.filter(is_superuser=False,is_staff=False),
                'roles':Role.objects.all(),
                'employment_type':Employee.EMPLOYMENT_TYPES,
                'error':error_message
                }
                return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))

    
    def searchEmployee(request):
        if request.user.is_authenticated and request.user.is_superuser :
            if request.method == "GET":
                search_input = request.GET.get('table_search') 
                print(search_input)
                if search_input:
                    employees = Employee.objects.filter(
                        Q(email__icontains=search_input) |
                        Q(first_name__icontains=search_input) |
                        Q(last_name__icontains=search_input) |
                        Q(phone_number__icontains=search_input)
                    )
                else:
                    employees = Employee.objects.all()
                roles = Role.objects.all()
                employment_type = Employee.EMPLOYMENT_TYPES
                form = EmployeeForm()
                context = {
                    'active_menu': 'employees',
                    'form': form,
                    'Employees': employees,
                    'roles': roles,
                    'employment_type': employment_type,
                }
                return render(request, 'adminAccessibilities/employees.html', context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    

    
    def updateEmployeeView(request, pk):
        if request.user.is_authenticated and request.user.is_superuser :
            if request.method == "GET":
                pk = int(pk)
                employee = Employee.objects.get(id=pk)
                form = EmployeeForm(instance=employee)
                context = {'form': form,
                           'active_menu': 'employees',}
                return render(request, 'adminAccessibilities/editEmployee.html', context)
            if request.method == "POST":    
                email = request.POST.get('email')
                try:
                    employee = Employee.objects.get(email=email)
                except Employee.DoesNotExist:
                    employee = None
                if employee:
                    form = EmployeeForm(request.POST, instance=employee)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect(reverse("core:employees"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
    
    def deleteEmployee(request, pk):
        if request.user.is_authenticated and request.user.is_superuser :
            pk = int(pk) 
            employee = Employee.objects.get(id=pk)
            employee.delete()
            return HttpResponseRedirect(reverse("core:employees"))
        else:
            return HttpResponseRedirect(reverse("core:index"))


        
        
        
class LeavesView(generic.ListView):
    template_name = "adminAccessibilities/leaves.html"

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser :
            leaves = Leaves.objects.all()
            reasons = Leaves.LEAVE_CHOICES
            form = LeaveForm()
            context = {
                'active_menu': 'leaves',
                'form': form,
                'reasons': reasons,
                'leaves': leaves,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("core:index"))

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser :
            print("in the post view")
            form = LeaveForm(request.POST)
            employee_id = request.POST.get('employee')
            leaving_days = request.POST.get('leaving_days')
            employee = Employee.objects.get(id=employee_id)
            employee_leaves_left = employee.leaves_left

            
            if form.is_valid():
                employee.leaves_left = employee_leaves_left - int(leaving_days)
                employee.save()
                form.save()
                return HttpResponseRedirect(reverse("core:leaves"))
            else:
                return HttpResponseRedirect(reverse("core:leaves"))
        else:
                return HttpResponseRedirect(reverse("core:index"))

    
    def updateLeaveView(request, pk):
       if request.user.is_authenticated and request.user.is_superuser :
           if request.method == "GET":
               pk = int(pk)
               leave = Leaves.objects.get(id=pk)
               form = LeaveForm(instance=leave)
               context = {'form': form,
                          'active_menu': 'leaves',}
               return render(request, 'adminAccessibilities/editLeave.html', context)
           elif request.method == "POST":
               pk = int(pk)
               try:
                   leave = Leaves.objects.get(id=pk)
               except Role.DoesNotExist:
                   leave = None
               if leave:
                   form = LeaveForm(request.POST, instance=leave)
                   employee_id = request.POST.get('employee')
                   leaving_days = request.POST.get('leaving_days')
                   diffrance_days = request.POST.get('diffrance_days')
                   employee = Employee.objects.get(id=employee_id)
                   employee_leaves_left = employee.leaves_left
                   if form.is_valid():
                       
                       employee.leaves_left = employee_leaves_left - int(diffrance_days)
                       employee.save()
                       form.save()
                       return HttpResponseRedirect(reverse("core:leaves"))
           else:
               return HttpResponseRedirect(reverse("core:index"))
           
    def deleteLeave(request, pk):
        if request.user.is_authenticated and request.user.is_superuser :
            pk = int(pk) 
            leave = Leaves.objects.get(id=pk)
            leave.delete()
            return HttpResponseRedirect(reverse("core:leaves"))
        else:
            return HttpResponseRedirect(reverse("core:index"))

    

    def searchLeaves(request):
        if request.user.is_authenticated and request.user.is_superuser :
            if request.method == "GET":
                search_input = request.GET.get('table_search') 
                print(search_input)
                if search_input:
                    leaves = Leaves.objects.filter( Q(employee__email__icontains=search_input))
                else:
                    leaves = Leaves.objects.all()
                reasons=Leaves.LEAVE_CHOICES
                form = LeaveForm()
                
                context = {
                    'active_menu': 'leaves',
                    'form':form,
                    'reasons':reasons,
                    'leaves':leaves,
                }

                return render(request,'adminAccessibilities/leaves.html',context)
        else:
            return HttpResponseRedirect(reverse("core:index"))