from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.indexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("employees/", views.EmployeesView.as_view(), name="employees"),
    path("roles/", views.RolesView.as_view(), name="roles"),
    path("leaves/", views.LeavesView.as_view(), name="leaves"),
    path("adminpage/", views.AdminView.as_view(), name="admin"),
    path("editEmployee/<str:pk>/", views.EmployeesView.updateEmployeeView, name="editEmployee"),
    path("editRole/<str:pk>/", views.RolesView.updateRoleView, name="editRole"),
    path("editLeave/<str:pk>/", views.LeavesView.updateLeaveView, name="editLeave"),
    path("searchEmployee/", views.EmployeesView.searchEmployee, name="searchEmployee"),
    path("searchLeave/", views.LeavesView.searchLeaves, name="searchLeave"),
    path("searchRole/", views.RolesView.searchRoles, name="searchRole"),
    path("updateEmployee/", views.updateEmployee, name="updateEmployee"),
  
    path("deleteEmployee/<str:pk>/", views.EmployeesView.deleteEmployee, name="deleteEmployee"),
    path("deleteRole/<str:pk>/", views.RolesView.deleteRole, name="deleteRole"),
    path("deleteLeave/<str:pk>/", views.LeavesView.deleteLeave, name="deleteLeave"),
]