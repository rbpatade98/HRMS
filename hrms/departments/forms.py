from django import forms
from .models import Department
from .models import Role
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Task, TaskAssignment






class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'description', 'status']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'description']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




class EmployeeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'mobile',
            'dept', 'role', 'reporting_manager', 'date_of_joining','password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'reporting_manager': forms.Select(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        def save(self, commit=True):
                user = super().save(commit=False)
                password = self.cleaned_data.get('password')

                if password:
                    user.set_password(password)  # 🔐 Securely hash password
                elif self.instance.pk:
                    # keep old password
                    user.password = CustomUser.objects.get(pk=self.instance.pk).password

                if commit:
                    user.save()
                return user
        



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Registered Email')

class OTPForm(forms.Form):
    otp = forms.CharField(label='Enter OTP')

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')






class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_priority', 'task_type', 'start_date', 'end_date']
        widgets = {
            'task_title': forms.TextInput(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'task_priority': forms.Select(attrs={'class': 'form-select'}),
            'task_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
]

class TaskAssignmentForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect,  # 👈 this shows radio buttons
        initial='Pending'  # default value
    )

    class Meta:
        model = TaskAssignment
        fields = ['employee', 'status']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['employee'].queryset = CustomUser.objects.filter(reporting_manager=user)





from .models import PerformanceReview

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['review_title', 'employee', 'review_period', 'rating', 'comments', 'review_date']  # ✅ Add here
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }
          
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ✅ Extract user from kwargs
        super().__init__(*args, **kwargs)

        if user:
            # ✅ Filter employees to only those who report to the logged-in manager
            self.fields['employee'].queryset = CustomUser.objects.filter(reporting_manager=user)


from django import forms
from .models import LeaveRequest, LeaveQuota

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

class LeaveQuotaForm(forms.ModelForm):
    class Meta:
        model = LeaveQuota
        fields = ['employee', 'leave_type', 'total_quota', 'used_quota']




