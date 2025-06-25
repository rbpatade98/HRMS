from django.contrib import admin
from django.urls import path, include
from departments.views import home
from django.contrib.auth import views as auth_views
from departments.views import home, CustomLogoutView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page (root URL)
    path('departments/', include('departments.urls')),  # Department CRUD
    path('login/', auth_views.LoginView.as_view(template_name='departments/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
