from django.forms import ModelForm,Select,TextInput,DateInput
from .models import Employee,Role,Leaves

class EmployeeForm(ModelForm):
    
    class Meta:
        
        model = Employee
        fields = ['first_name','last_name','email','phone_number','role','start_date','employment_type','address','hourly_rate']
        widgets = {
            'employment_type': Select(attrs={
                'class': "form-control"
                }),
            'role': Select(attrs={
                'class': "form-control"
                }),
            'first_name': TextInput(attrs={
                'class': "form-control"
                }),
            'last_name': TextInput(attrs={
                'class': "form-control"
                }),
            'email': TextInput(attrs={
                'class': "form-control"
                }),
            'address': TextInput(attrs={
                'class': "form-control"
                }),
            'phone_number': TextInput(attrs={
                'class': "form-control"
                }),
            'start_date': DateInput(attrs={
                'class': "form-control"
                }),
            'hourly_rate': TextInput(attrs={
                'class': "form-control"
                }),
            'id': TextInput(attrs={
                'style': "display:none"
                }),
        }

class RoleForm(ModelForm):
    
    class Meta:
        
        model = Role
        fields = ['role_name','off_days']
        widgets = {
                     
           
            'role_name': TextInput(attrs={
                'class': "form-control"
                }),
            'off_days': TextInput(attrs={
                'class': "form-control"
                }),
           
        }

class LeaveForm(ModelForm):
    
    class Meta:
        
        model = Leaves
        fields = ['employee','date','reason']
        widgets = {
                     
           
                'employee': Select(attrs={
                'class': "form-control"
                }),
                'reason': Select(attrs={
                'class': "form-control"
                }),
                'date': DateInput(attrs={
                'class': "form-control"
                }),
           
        }

     