from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'description', 'status']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
