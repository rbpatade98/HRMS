from django.contrib import admin
from .models import Department
from .models import Role
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Task 
from .models import TaskAssignment 

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'status', 'created_at', 'updated_at')
    search_fields = ('dept_name',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'created_at', 'updated_at')
    search_fields = ('role_name',)
    ordering = ('-created_at',)




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('employee_id', 'username', 'first_name', 'last_name', 'email', 'dept', 'role', 'reporting_manager','created_at', 'updated_at')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('mobile', 'dept', 'role', 'reporting_manager', 'date_of_joining','created_at', 'updated_at')
        }),
    )



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_id', 'task_title', 'task_priority', 'task_type',
        'start_date', 'end_date', 'created_at', 'updated_at'
    )
    search_fields = ('task_title', 'task_priority', 'task_type')
    list_filter = ('task_priority', 'task_type', 'start_date')
    ordering = ('-created_at',)


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'assignment_id', 'task', 'employee', 'assigned_by',
        'status', 'assigned_date', 'completed_at'
    )
    search_fields = ('task__task_title', 'employee__username', 'status')
    list_filter = ('status', 'assigned_date')
    ordering = ('-assigned_date',)
