from django.shortcuts import render,redirect
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
import time
from .models import Employee, Leaves,Role
from .forms import EmployeeForm, LeaveForm,RoleForm
from django.contrib import messages

from django.db.models import Q
# Create your views here.


class indexView(View):
    template_name = "index.html"
    def get(self,request):
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
                return HttpResponseRedirect(reverse("core:admin"))
            else:
                return HttpResponseRedirect(reverse("core:index"))
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

class AdminView(View):
    template_name = "adminPage.html"

    def get(self,request):
        if request.user:
            admins_count = Employee.objects.filter(is_superuser=True).count()
            employees_count = Employee.objects.filter(is_superuser=False, is_staff=False).count()
            leaves_today_count = Leaves.objects.filter(start_date=time.strftime("%Y-%m-%d")).count()
            roles_count = Role.objects.all().count()

            leaves=Leaves.objects.all()
            employees=Employee.objects.all()

            context = {
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
        if request.user:
            roles=Role.objects.all()
            form=RoleForm()
            context={
                'roles':roles,
             'form':form,
            }
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    def post(self,request):
        if request.user:
            form=RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:roles"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def deleteRole(request, pk):
        if request.user:
            pk = int(pk) 
            role = Role.objects.get(id=pk)
            role.delete()
            return HttpResponseRedirect(reverse("core:roles"))
        else:
            return HttpResponseRedirect(reverse("core:index"))
    
    def updateRoleView(request, pk):
        if request.user:
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
        
    


        
class EmployeesView(generic.ListView):
    template_name="adminAccessibilities/employees.html"
    def get(self,request):
        if request.user:
            
            employees=Employee.objects.filter(is_superuser=False,is_staff=False)
            
            roles=Role.objects.all()
            employment_type = Employee.EMPLOYMENT_TYPES
            print(employment_type)
            form = EmployeeForm()
            context = {
                'form':form,
                'Employees':employees,
                'roles':roles,
                'employment_type':employment_type,
            }
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
        
    def post(self,request): 
        if request.user:
            country_code=request.POST.get('countryCode')
            phone_nb=request.POST.get('phone')
            post = request.POST.copy()
            post['phone_number'] = '+'+country_code+phone_nb
            post['hourly_rate'] = float(request.POST.get('hourly_rate'))
            request.POST = post
            form=EmployeeForm(request.POST) 
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("core:employees"))
            return HttpResponse(status=400)
        else:
            return HttpResponseRedirect(reverse("core:index"))

    
    def searchEmployee(request):
        if request.user:
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
                    'form': form,
                    'Employees': employees,
                    'roles': roles,
                    'employment_type': employment_type,
                }
                return render(request, 'adminAccessibilities/employees.html', context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    

    
    def updateEmployeeView(request, pk):
        if request.user:
            pk = int(pk)
            employee = Employee.objects.get(id=pk)
            form = EmployeeForm(instance=employee)
            context = {'form': form}
            return render(request, 'adminAccessibilities/editEmployee.html', context)
        else:
            return HttpResponseRedirect(reverse("core:index"))
    
    def deleteEmployee(request, pk):
        if request.user:
            pk = int(pk) 
            employee = Employee.objects.get(id=pk)
            employee.delete()
            return HttpResponseRedirect(reverse("core:employees"))
        else:
            return HttpResponseRedirect(reverse("core:index"))

def updateEmployee(request):
    if request.user:
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

        return HttpResponse(status=400)
    else:
        return HttpResponseRedirect(reverse("core:index"))



   
        
        
        
class LeavesView(generic.ListView):
    template_name = "adminAccessibilities/leaves.html"

    def get(self, request):
        if request.user:
            leaves = Leaves.objects.all()
            reasons = Leaves.LEAVE_CHOICES
            form = LeaveForm()
            context = {
                'form': form,
                'reasons': reasons,
                'leaves': leaves,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("core:index"))

    def post(self, request):
        if request.user:
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
       if request.user:
           if request.method == "GET":
               pk = int(pk)
               leave = Leaves.objects.get(id=pk)
               form = LeaveForm(instance=leave)
               context = {'form': form}
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
        if request.user:
            pk = int(pk) 
            leave = Leaves.objects.get(id=pk)
            leave.delete()
            return HttpResponseRedirect(reverse("core:leaves"))
        else:
            return HttpResponseRedirect(reverse("core:index"))

    

    def searchLeaves(request):
        if request.user:
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
                    'form':form,
                    'reasons':reasons,
                    'leaves':leaves,
                }

                return render(request,'adminAccessibilities/leaves.html',context)
        else:
            return HttpResponseRedirect(reverse("core:index"))