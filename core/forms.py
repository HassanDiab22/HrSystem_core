
from django.forms import DateField, ModelForm,Select,TextInput,DateInput,NumberInput,Textarea,DateTimeInput,PasswordInput
from .models import Employee,Role,Leaves, Timesheet,Task

class EmployeeForm(ModelForm):
    
    class Meta:
        
        model = Employee
        fields = ['first_name','last_name','email','phone_number','role','start_date','employment_type','address','hourly_rate','password']
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
                'class': "form-control",
                'type':'date'
                }),
            'hourly_rate': TextInput(attrs={
                'class': "form-control"
                }),
            'id': TextInput(attrs={
                'style': "display:none"
                }),
            'password': PasswordInput(attrs={
                'class': "form-control"
                }),
        }

class TimesheetForm(ModelForm):
    class Meta:
        model = Timesheet
        fields = ['employee','startdate','enddate']
        widgets = {
                'startdate': DateInput(attrs={
                'class': "form-control",
                'type':'date'
                }),
                'enddate': DateInput(attrs={
                'class': "form-control",
                'type':'date'
                }),   
        }



       

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['timesheet','description','duration']
          
        widgets = {
                'description': Textarea(attrs={
                'class': "form-control",
                'rows':'3',
                'placeholder':"Enter description..",
                'required': 'required' 
                }),
                'duration': NumberInput(attrs={
                'class': "form-control",
                'required': 'required' 
                }),   
        }
        
       


class ProfileForm(ModelForm):
    class Meta:
    
        model = Employee
        fields = ['first_name','last_name','email','phone_number','role','start_date','employment_type','address','hourly_rate','password','profile_picture',]
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
                'class': "form-control",
                'type':'date'
                }),
            'hourly_rate': TextInput(attrs={
                'class': "form-control"
                }),
            'id': TextInput(attrs={
                'style': "display:none"
                }),
            'password': PasswordInput(attrs={
                'class': "form-control"
                }),
            # 'profile_picture': FileInput(attrs={
            #     'class': "form-control",
            #     "class":"custom-file-input",
            #      'id':"exampleInputFile",
            #        'accept':"image/*"
            #     }),
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
        fields = ['employee','start_date','end_date','leaving_days','reason',]
        widgets = {
                     
           
                'employee': Select(attrs={
                'class': "form-control"
                }),
                'reason': Select(attrs={
                'class': "form-control"
                }),
                'start_date': DateInput(attrs={
                'class': "form-control",
                'type':'date'
                }),
                'end_date': DateInput(attrs={
                'class': "form-control",
                'type':'date'
                }),
               
                
                
           
        }

     