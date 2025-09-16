from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def validate_giki_email(value):
    """Validate that email is from giki.edu.pk domain."""
    if not value.endswith('@giki.edu.pk'):
        raise ValidationError('Email must be from giki.edu.pk domain')


class CRAssignment(models.Model):
    """Model to track CR email assignments by admin."""
    
    email = models.EmailField(unique=True, validators=[validate_giki_email])
    assigned_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='assigned_cr_emails')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cr_assignments'
        verbose_name = 'CR Assignment'
        verbose_name_plural = 'CR Assignments'
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.email} (assigned by {self.assigned_by.email})"


class User(AbstractUser):
    """Custom user model with role-based authentication."""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('cr', 'Class Representative'),
    ]
    
    email = models.EmailField(unique=True, validators=[validate_giki_email])
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    @property
    def is_cr(self):
        return self.role == 'cr'
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    def save(self, *args, **kwargs):
        """Override save to auto-assign CR role based on CR assignments."""
        # Check if this email is assigned as CR
        if CRAssignment.objects.filter(email=self.email, is_active=True).exists():
            self.role = 'cr'
        else:
            self.role = 'student'
        
        super().save(*args, **kwargs)
