from django.shortcuts import render,redirect
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import Employee,Role
from .forms import EmployeeForm,RoleForm
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
    def post(self,request):
        try:
                    email = request.POST.get('email')
                    print(email)
                    password = request.POST.get('password')
                    print(password)
                    user = authenticate(email=email, password=password)
                    user = Employee.objects.get(email=email, password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse("core:admin"))
                    return HttpResponseRedirect(reverse("core:index"))
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

class AdminView(View):
    template_name = "adminPage.html"

    def get(self,request):
        if request.user:
            return render(request,self.template_name)
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
    
    def updateRole(request, pk):
        if request.user:
            pk = int(pk)
            role = Role.objects.get(id=pk)
            form = RoleForm(instance=role)
            context = {'form': form}
            return render(request, 'adminAccessibilities/editRole.html', context)
        else:
            return HttpResponseRedirect(reverse("core:index"))


        
class EmployeesView(generic.ListView):
    template_name="adminAccessibilities/employees.html"
    def get(self,request):
        if request.user:
            
            employees=Employee.objects.all()
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
   
    def put(self,request):
        print('hello')
    
 
    
    def updateEmployeeView(request, pk):
        pk = int(pk)
        employee = Employee.objects.get(id=pk)
        form = EmployeeForm(instance=employee)
        context = {'form': form}
        return render(request, 'adminAccessibilities/editEmployee.html', context)
    
    def deleteEmployee(request, pk):
        pk = int(pk) 
        employee = Employee.objects.get(id=pk)
        employee.delete()
        return HttpResponseRedirect(reverse("core:employees"))

def updateEmployee(request):
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



   
        
        
        

