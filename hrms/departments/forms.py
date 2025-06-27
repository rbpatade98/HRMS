from django import forms
from .models import Department
from .models import Role
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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
