from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_add'),
    path('departments/edit/<int:pk>/', views.department_update, name='department_edit'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),

    # Roles
    path('roles/', views.role_list, name='role_list'),
    path('roles/add/', views.role_create, name='role_add'),
    path('roles/edit/<int:pk>/', views.role_update, name='role_edit'),
    path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),

]
