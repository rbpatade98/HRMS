from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import View

from .models import Department
from .forms import DepartmentForm


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
