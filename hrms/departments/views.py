from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import View
from django.db import models
from .models import Department
from .forms import DepartmentForm
import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .forms import ForgotPasswordForm, OTPForm, ResetPasswordForm
import smtplib
from django.core.mail import EmailMessage, get_connection


from .models import Task, TaskAssignment, CustomUser
from .forms import TaskForm
from django.db.models import Q, Count
from django.utils import timezone





# ✅ Home Page (Public)
def home(request):
    return render(request, 'departments/home.html')


# ✅ Admin-only check
def admin_check(user):
    return user.is_authenticated and user.is_superuser


# ✅ Admin Login View
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Access denied. Only admin users allowed.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'departments/login.html', {'form': form})


# ✅ Admin Logout View
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')


# ✅ Admin Dashboard
@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    return render(request, 'departments/dashboard.html')


# ✅ Department List
@login_required
@user_passes_test(admin_check)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})


# ✅ Create Department
@login_required
@user_passes_test(admin_check)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})


# ✅ Update Department
@login_required
@user_passes_test(admin_check)
def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'departments/department_form.html', {'form': form})


# ✅ Delete Department
@login_required
@user_passes_test(admin_check)
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, "Department deleted.")
        return redirect('department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': dept})


from .models import Department

def department_list(request):
    query = request.GET.get('q')  # Get search query
    if query:
        departments = Department.objects.filter(dept_name__icontains=query)
    else:
        departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments, 'query': query})


#Roles view
from .models import Role
from .forms import RoleForm

@login_required
@user_passes_test(admin_check)
def role_list(request):
    roles = Role.objects.all()
    return render(request, 'departments/role_list.html', {'roles': roles})

@login_required
@user_passes_test(admin_check)
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role added successfully.")
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'departments/role_form.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Role updated successfully.")
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'departments/role_form.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, "Role deleted successfully.")
        return redirect('role_list')
    return render(request, 'departments/role_confirm_delete.html', {'role': role})


def role_list(request):
    query = request.GET.get('q')
    if query:
        roles = Role.objects.filter(role_name__icontains=query)
    else:
        roles = Role.objects.all()
    return render(request, 'departments/role_list.html', {'roles': roles, 'query': query})


#employee
from .models import CustomUser
from .forms import EmployeeForm

@login_required
@user_passes_test(admin_check)
def employee_list(request):
    employees = CustomUser.objects.all()
    return render(request, 'departments/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(admin_check)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'departments/employee_form.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def employee_update(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'departments/employee_form.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def employee_delete(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted.")
        return redirect('employee_list')
    return render(request, 'departments/employee_confirm_delete.html', {'employee': employee})


@login_required
@user_passes_test(admin_check)
def employee_list(request):
    query = request.GET.get('q')
    if query:
        employees = CustomUser.objects.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(username__icontains=query) |
            models.Q(email__icontains=query)
        )
    else:
        employees = CustomUser.objects.all()
    return render(request, 'departments/employee_list.html', {'employees': employees, 'query': query})





User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['reset_email'] = email

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is: {otp}',
                    'your-email@gmail.com',
                    [email],
                    fail_silently=False
                )

                messages.success(request, 'OTP sent to your email.')
                return redirect('verify_otp')

            except User.DoesNotExist:
                messages.error(request, 'Email not found!')
    else:
        form = ForgotPasswordForm()
    return render(request, 'departments/forgot_password.html', {'form': form})


def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = request.session.get('otp')

            if entered_otp == session_otp:
                messages.success(request, 'OTP verified.')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP.')
    else:
        form = OTPForm()
    return render(request, 'departments/verify_otp.html', {'form': form})

from django.contrib.auth import get_user_model
User = get_user_model()

def reset_password_view(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Session expired. Please request OTP again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            confirm = form.cleaned_data['confirm_password']

            if password != confirm:
                messages.error(request, 'Passwords do not match!')
                return redirect('reset_password')

            try:
                user = User.objects.get(email=email)
                user.set_password(password)  # ✅ This securely hashes the password
                user.save()

                messages.success(request, 'Password reset successful. Please login.')
                request.session.flush()
                return redirect('login')

            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()

    return render(request, 'departments/reset_password.html', {'form': form})

#task
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task, TaskAssignment, CustomUser
from .forms import TaskForm, TaskAssignmentForm
from django.core.paginator import Paginator


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        assign_form = TaskAssignmentForm(request.POST, user=request.user)

        if form.is_valid() and assign_form.is_valid():
            task = form.save(commit=False)
            task.created_at = timezone.now()
            task.updated_at = timezone.now()
            task.save()

            assignment = assign_form.save(commit=False)
            assignment.task = task
            assignment.assigned_by = request.user
            assignment.assigned_date = timezone.now()
            assignment.save()

            messages.success(request, 'Task created and assigned successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
        assign_form = TaskAssignmentForm(user=request.user)

    return render(request, 'departments/task_form.html', {
        'form': form,
        'assign_form': assign_form
    })

@login_required
def task_list(request):
    tasks = TaskAssignment.objects.select_related('task', 'employee')

    # Filtering parameters
    employee_id = request.GET.get('employee')
    status = request.GET.get('status')
    from_date = request.GET.get('start_date')
    to_date = request.GET.get('end_date')

    # Filter only tasks assigned by the logged-in user (Team Leader/Admin)
    tasks = tasks.filter(assigned_by=request.user)

    # Apply filters safely
    if employee_id and employee_id != 'all':
        tasks = tasks.filter(employee_id=employee_id)

    if status and status != 'all':
        tasks = tasks.filter(status=status)

    if from_date:
        tasks = tasks.filter(task__start_date__gte=from_date)

    if to_date:
        tasks = tasks.filter(task__end_date__lte=to_date)

    # 📊 Statistics
    total = tasks.count()
    completed = tasks.filter(status='Completed').count()
    pending = tasks.filter(status='Pending').count()
    in_progress = tasks.filter(status='In Progress').count()

    stats = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
    }

    # Get subordinates of current user
    employees = CustomUser.objects.filter(reporting_manager=request.user)

    return render(request, 'departments/task_list.html', {
        'tasks': tasks,
        'employees': employees,
        'stats': stats,
        'request': request  # for template filter dropdowns
    })


@login_required
def task_detail(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, pk=assignment_id)
    task_assignments = TaskAssignment.objects.filter(task=assignment.task)
    return render(request, 'departments/task_detail.html', {
        'task': assignment.task,
        'task_assignments': task_assignments
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        assign_form = TaskAssignmentForm(request.POST, user=request.user)
        if form.is_valid() and assign_form.is_valid():
            form.save()
            TaskAssignment.objects.filter(task=task).delete()
            TaskAssignment.objects.create(
                task=task,
                employee=assign_form.cleaned_data['employee'],
                assigned_by=request.user,
                assigned_date=timezone.now(),
                status='Pending'
            )
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        assign_form = TaskAssignmentForm(user=request.user)
    return render(request, 'departments/task_form.html', {'form': form, 'assign_form': assign_form, 'edit_mode': True})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'departments/task_confirm_delete.html', {'task': task})

@login_required
def mark_task_completed(request, pk):
    assignment = get_object_or_404(TaskAssignment, pk=pk)
    assignment.status = 'Completed'
    assignment.completed_at = timezone.now()
    assignment.save()
    messages.success(request, "Task marked as completed.")
    return redirect('task_list')

@login_required
def task_edit(request, pk):
    assignment = get_object_or_404(TaskAssignment, pk=pk)
    task = assignment.task

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        assign_form = TaskAssignmentForm(request.POST, instance=assignment, user=request.user)

        if form.is_valid() and assign_form.is_valid():
            task = form.save(commit=False)
            task.updated_at = timezone.now()
            task.save()

            assignment = assign_form.save(commit=False)
            assignment.task = task
            assignment.assigned_by = request.user
            assignment.save()

            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        assign_form = TaskAssignmentForm(instance=assignment, user=request.user)

    return render(request, 'departments/task_form.html', {
        'form': form,
        'assign_form': assign_form
    })

@login_required
def task_detail(request, pk):
    assignment = get_object_or_404(TaskAssignment, pk=pk)
    task = assignment.task
    task_assignments = TaskAssignment.objects.filter(task=task)

    return render(request, 'departments/task_detail.html', {
        'task': task,
        'task_assignments': task_assignments
    })
