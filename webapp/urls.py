from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cr-panel/', views.cr_panel_view, name='cr_panel'),
    path('student-panel/', views.student_panel_view, name='student_panel'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', views.api_login_view, name='api_login'),
]
