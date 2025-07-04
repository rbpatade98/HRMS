from django.contrib import admin
from .models import Department
from .models import Role
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Task 
from .models import TaskAssignment 
from .models import PerformanceReview
from .models import LeaveRequest
from .models import LeaveQuota

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




@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_title', 'employee', 'review_period', 'rating', 'get_reviewer', 'review_date')
    list_filter = ('review_period', 'rating')
    search_fields = ('review_title', 'employee__username', 'reviewed_by__username')

    def get_reviewer(self, obj):
        return obj.reviewed_by.get_full_name() if obj.reviewed_by else '-'
    get_reviewer.short_description = 'Reviewed By'



from django.contrib import admin
from .models import LeaveRequest, LeaveQuota

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'approved_by', 'applied_at']
    list_filter = ['leave_type', 'status', 'start_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'leave_type']
    readonly_fields = ['applied_at', 'updated_at']

@admin.register(LeaveQuota)
class LeaveQuotaAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'total_quota', 'used_quota', 'remain_quota']
    list_filter = ['leave_type']
    search_fields = ['employee__first_name', 'employee__last_name']
