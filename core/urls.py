from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.indexView.as_view(), name="index"),
    path("newrole/", views.CreateRoleView.as_view(), name="create_role"),
    path("login/", views.Login.as_view(), name="login"),
    path("employees/", views.EmployeesView.as_view(), name="employees"),
    path("roles/", views.RolesView.as_view(), name="roles"),
    path("adminpage/", views.AdminView.as_view(), name="admin"),
    path("editEmployee/<str:pk>/", views.EmployeesView.updateEmployeeView, name="editEmployee"),
    path("editRole/<str:pk>/", views.RolesView.updateRole, name="editRole"),
    path("updateEmployee/", views.updateEmployee, name="updateEmployee"),
    path("deleteEmployee/<str:pk>/", views.EmployeesView.deleteEmployee, name="deleteEmployee"),
    path("deleteRole/<str:pk>/", views.RolesView.deleteRole, name="deleteRole"),
]