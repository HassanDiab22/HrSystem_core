from django.urls import path

from . import views
from django.contrib.auth.decorators import login_required



app_name = "core"
urlpatterns = [
    path("", views.indexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name='logout'),
    path("employees/", views.EmployeesView.as_view(), name="employees"),
     path("roles/",views.RolesView.as_view(), name="roles"),
    path("leaves/", views.LeavesView.as_view(), name="leaves"),
    path("adminpage/", views.AdminView.as_view(), name="admin"),
    path("employees/<str:pk>/", views.EmployeesView.updateEmployeeView, name="editEmployee"),
    path("role/<str:pk>/", views.RolesView.updateRoleView, name="editRole"),
    path("leaves/<str:pk>/", views.LeavesView.updateLeaveView, name="editLeave"),
    path("employees/search", views.EmployeesView.searchEmployee, name="searchEmployee"),
    path("leaves/search", views.LeavesView.searchLeaves, name="searchLeave"),
    path("role/search", views.RolesView.searchRoles, name="searchRole"),
    path("<str:pk>/delete", views.EmployeesView.deleteEmployee, name="deleteEmployee"),
    path("<str:pk>/delete", views.RolesView.deleteRole, name="deleteRole"),
    path("<str:pk>/delete", views.LeavesView.deleteLeave, name="deleteLeave"),
]