from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # User authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('demo-login/', views.demo_login_view, name='demo-login'),
    path('profile/', views.user_profile_view, name='user-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Admin CR management
    path('admin/cr-assignments/', views.CRAssignmentListCreateView.as_view(), name='cr-assignment-list-create'),
    path('admin/cr-assignments/<int:pk>/', views.CRAssignmentDetailView.as_view(), name='cr-assignment-detail'),
    path('admin/assign-cr/', views.assign_cr_view, name='assign-cr'),
    path('admin/revoke-cr/', views.revoke_cr_view, name='revoke-cr'),
    path('admin/cr-list/', views.cr_assignments_view, name='cr-assignments'),
]
