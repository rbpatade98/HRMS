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

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_update, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),

    #forgotpassword
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

   
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('tasks/mark-completed/<int:pk>/', views.mark_task_completed, name='mark_task_completed'),
    path('tasks/detail/<int:pk>/', views.task_detail, name='task_detail'),

    #performance
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.review_create, name='review_create'),
    path('reviews/edit/<int:pk>/', views.review_edit, name='review_edit'),
    path('reviews/delete/<int:pk>/', views.review_delete, name='review_delete'),
    path('reviews/detail/<int:pk>/', views.review_detail, name='review_detail'),

     # Leave Dashboard
    path('leave/dashboard/', views.leave_dashboard, name='leave_dashboard'),

    # Apply and Edit Leave
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/edit/<int:pk>/', views.edit_leave, name='edit_leave'),

    # Leave Approval by Manager/Admin
    path('leave/approval/', views.leave_approval_list, name='leave_approval_list'),
    path('leave/approve/<int:pk>/', views.approve_leave, name='approve_leave'),

    # Leave Quota Management
    path('leave/quota/', views.leave_quota_list, name='leave_quota_list'),
    path('leave/quota/add/', views.add_leave_quota, name='add_leave_quota'),
    path('leave/quota/edit/<int:pk>/', views.edit_leave_quota, name='edit_leave_quota'),
    path('leave/quota/delete/<int:pk>/', views.delete_leave_quota, name='delete_leave_quota'),

]

    




