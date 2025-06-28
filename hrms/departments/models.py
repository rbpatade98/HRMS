from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date


class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.dept_name


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


class CustomUser(AbstractUser):
    employee_id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    date_of_joining = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"




# class Task(models.Model):
#     task_id = models.AutoField(primary_key=True)
#     task_title = models.CharField(max_length=100)
#     task_description = models.TextField(max_length=300)
#     task_priority = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
#     start_date = models.DateField()
#     end_date = models.DateField()
#     task_type = models.CharField(max_length=50, choices=[('Individual', 'Individual'), ('Team', 'Team')])
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class TaskAssignment(models.Model):
#     assignment_id = models.AutoField(primary_key=True)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks')
#     assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
#     assigned_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In progress', 'In progress'), ('Completed', 'Completed')], default='Pending')
#     completed_at = models.DateTimeField(null=True, blank=True)

class Task(models.Model):
    TASK_PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    TASK_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Team', 'Team'),
    ]

    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()
    task_priority = models.CharField(max_length=20, choices=TASK_PRIORITY_CHOICES)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    assignment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_date = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

# models.py
from django.db import models
from django.conf import settings

REVIEW_PERIOD_CHOICES = [
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Annual', 'Annual'),
]

RATING_CHOICES = [
    (1, '1 - Poor'),
    (2, '2 - Fair'),
    (3, '3 - Good'),
    (4, '4 - Very Good'),
    (5, '5 - Excellent'),
]

class PerformanceReview(models.Model):
    review_title = models.CharField(max_length=200)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received')
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given')
    review_period = models.CharField(max_length=50, choices=REVIEW_PERIOD_CHOICES)
    rating = models.IntegerField()
    comments = models.TextField()
    review_date = models.DateField()


# LeaveRequest Model
class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
        ('LWP', 'Leave Without Pay'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=4, choices=LEAVE_TYPE_CHOICES)
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total_days
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)




# LeaveQuota Model
class LeaveQuota(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
        ('LWP', 'Leave Without Pay'),
    ]
    leave_quota_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_quotas')
    leave_type = models.CharField(max_length=4, choices=LEAVE_TYPE_CHOICES)
    total_quota = models.PositiveIntegerField(default=0)
    used_quota = models.PositiveIntegerField(default=0)
    remain_quota = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.remain_quota = self.total_quota - self.used_quota
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('employee', 'leave_type')