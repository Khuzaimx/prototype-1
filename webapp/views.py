from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from users.models import CRAssignment
from classes.models import ClassSchedule, ClassAttachment, AlarmSettings
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()


def home_view(request):
    """Main home page."""
    return render(request, 'webapp/home.html')


def login_view(request):
    """Login page."""
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        
        # Validate email domain
        if not email.endswith('@giki.edu.pk'):
            return render(request, 'webapp/login.html', {
                'error': 'Email must be from giki.edu.pk domain'
            })
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'webapp/login.html', {
                'error': 'Invalid credentials'
            })
    
    return render(request, 'webapp/login.html')


def register_view(request):
    """Registration page."""
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validate email domain
        if not email.endswith('@giki.edu.pk'):
            return render(request, 'webapp/register.html', {
                'error': 'Email must be from giki.edu.pk domain'
            })
        
        # Validate passwords match
        if password != password_confirm:
            return render(request, 'webapp/register.html', {
                'error': 'Passwords do not match'
            })
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'webapp/register.html', {
                'error': 'User with this email already exists'
            })
        
        # Create user
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        
        # Login user
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'webapp/register.html')


@login_required
def dashboard_view(request):
    """Main dashboard."""
    user = request.user
    
    # Get today's classes
    from datetime import date
    today = date.today()
    todays_classes = ClassSchedule.objects.filter(date=today).order_by('time')
    
    # Get user's created classes if CR
    user_classes = []
    if user.is_cr:
        user_classes = ClassSchedule.objects.filter(created_by=user).order_by('-created_at')
    
    context = {
        'user': user,
        'todays_classes': todays_classes,
        'user_classes': user_classes,
    }
    
    return render(request, 'webapp/dashboard.html', context)


@login_required
def cr_panel_view(request):
    """CR panel for class management."""
    if not request.user.is_cr:
        return render(request, 'webapp/error.html', {
            'error': 'Access denied. CR privileges required.'
        })
    
    if request.method == 'POST':
        # Handle class creation
        subject = request.POST.get('subject')
        venue = request.POST.get('venue')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note', '')
        
        ClassSchedule.objects.create(
            created_by=request.user,
            subject=subject,
            venue=venue,
            date=date,
            time=time,
            note=note
        )
        
        return redirect('cr_panel')
    
    # Get CR's classes
    classes = ClassSchedule.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'classes': classes,
    }
    
    return render(request, 'webapp/cr_panel.html', context)


@login_required
def student_panel_view(request):
    """Student panel for viewing classes."""
    from datetime import date
    today = date.today()
    todays_classes = ClassSchedule.objects.filter(date=today).order_by('time')
    
    # Get alarm settings for each class
    alarm_settings = {}
    for class_item in todays_classes:
        try:
            alarm_setting = AlarmSettings.objects.get(user=request.user, class_schedule=class_item)
            alarm_settings[class_item.id] = alarm_setting
        except AlarmSettings.DoesNotExist:
            # Create default alarm setting
            alarm_setting = AlarmSettings.objects.create(
                user=request.user,
                class_schedule=class_item,
                is_enabled=True,
                alarm_minutes_before=20
            )
            alarm_settings[class_item.id] = alarm_setting
    
    context = {
        'todays_classes': todays_classes,
        'alarm_settings': alarm_settings,
    }
    
    return render(request, 'webapp/student_panel.html', context)


@staff_member_required
def admin_panel_view(request):
    """Admin panel for CR management."""
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        action = request.POST.get('action')
        
        if not email.endswith('@giki.edu.pk'):
            return render(request, 'webapp/admin_panel.html', {
                'error': 'Email must be from giki.edu.pk domain'
            })
        
        if action == 'assign':
            # Assign CR role
            if CRAssignment.objects.filter(email=email, is_active=True).exists():
                return render(request, 'webapp/admin_panel.html', {
                    'error': 'This email is already assigned as CR'
                })
            
            CRAssignment.objects.create(
                email=email,
                assigned_by=request.user
            )
            
            # Update existing user if exists
            try:
                user = User.objects.get(email=email)
                user.save()  # This will auto-assign CR role
            except User.DoesNotExist:
                pass
            
            return render(request, 'webapp/admin_panel.html', {
                'success': f'CR role assigned to {email}'
            })
        
        elif action == 'revoke':
            # Revoke CR role
            try:
                cr_assignment = CRAssignment.objects.get(email=email, is_active=True)
                cr_assignment.is_active = False
                cr_assignment.save()
                
                # Update existing user if exists
                try:
                    user = User.objects.get(email=email)
                    user.save()  # This will auto-assign student role
                except User.DoesNotExist:
                    pass
                
                return render(request, 'webapp/admin_panel.html', {
                    'success': f'CR role revoked from {email}'
                })
            except CRAssignment.DoesNotExist:
                return render(request, 'webapp/admin_panel.html', {
                    'error': 'CR assignment not found'
                })
    
    # Get all CR assignments
    cr_assignments = CRAssignment.objects.all().order_by('-assigned_at')
    
    context = {
        'cr_assignments': cr_assignments,
    }
    
    return render(request, 'webapp/admin_panel.html', context)


def logout_view(request):
    """Logout user."""
    logout(request)
    return redirect('home')


@csrf_exempt
def api_login_view(request):
    """API endpoint for login (for AJAX calls)."""
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        if not email.endswith('@giki.edu.pk'):
            return JsonResponse({'error': 'Email must be from giki.edu.pk domain'}, status=400)
        
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)