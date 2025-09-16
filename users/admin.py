from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, CRAssignment


@admin.register(CRAssignment)
class CRAssignmentAdmin(admin.ModelAdmin):
    """Admin for CR assignments."""
    list_display = ('email', 'assigned_by', 'assigned_at', 'is_active', 'status_display')
    list_filter = ('is_active', 'assigned_at', 'assigned_by')
    search_fields = ('email', 'assigned_by__email')
    ordering = ('-assigned_at',)
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('email', 'assigned_by', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('assigned_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('assigned_at',)
    
    def status_display(self, obj):
        """Display status with color coding."""
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        else:
            return format_html('<span style="color: red;">✗ Inactive</span>')
    status_display.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        """Override save to update user role if user exists."""
        super().save_model(request, obj, form, change)
        
        # Update existing user if exists
        try:
            user = User.objects.get(email=obj.email)
            user.save()  # This will auto-assign role based on CR assignment
        except User.DoesNotExist:
            pass  # User will get correct role when they sign up


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom user admin."""
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('role', 'created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        """Make role readonly for non-superusers."""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields.append('role')
        return readonly_fields
