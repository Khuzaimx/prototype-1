from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import date
from .models import ClassSchedule, ClassAttachment, AlarmSettings
from .serializers import (
    ClassScheduleSerializer, 
    ClassScheduleCreateSerializer,
    ClassScheduleListSerializer,
    ClassAttachmentSerializer,
    ClassAttachmentCreateSerializer,
    AlarmSettingsSerializer,
    AlarmSettingsUpdateSerializer
)


class ClassScheduleListCreateView(generics.ListCreateAPIView):
    """List and create class schedules."""
    
    def get_queryset(self):
        """Filter classes based on user role and date."""
        user = self.request.user
        
        # Get query parameters
        date_filter = self.request.query_params.get('date', None)
        today_only = self.request.query_params.get('today', None)
        
        queryset = ClassSchedule.objects.all()
        
        # CR can see all classes, students see all classes
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        elif today_only:
            queryset = queryset.filter(date=date.today())
        
        return queryset.order_by('date', 'time')
    
    def get_serializer_class(self):
        """Use different serializers for list and create."""
        if self.request.method == 'GET':
            return ClassScheduleListSerializer
        return ClassScheduleCreateSerializer
    
    def get_permissions(self):
        """Set permissions based on method."""
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Create class schedule with current user."""
        serializer.save(created_by=self.request.user)


class ClassScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a class schedule."""
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    
    def get_permissions(self):
        """CR can edit/delete, students can only view."""
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        """Only CR can update their own classes."""
        if not self.request.user.is_cr:
            raise permissions.PermissionDenied("Only CR can update classes.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only CR can delete their own classes."""
        if not self.request.user.is_cr:
            raise permissions.PermissionDenied("Only CR can delete classes.")
        instance.delete()


class ClassAttachmentListCreateView(generics.ListCreateAPIView):
    """List and create class attachments."""
    
    def get_queryset(self):
        """Get attachments for specific class."""
        class_schedule_id = self.kwargs['class_schedule_id']
        return ClassAttachment.objects.filter(class_schedule_id=class_schedule_id)
    
    def get_serializer_class(self):
        """Use different serializers for list and create."""
        if self.request.method == 'GET':
            return ClassAttachmentSerializer
        return ClassAttachmentCreateSerializer
    
    def get_permissions(self):
        """CR can create, all authenticated users can view."""
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Create attachment for specific class."""
        class_schedule_id = self.kwargs['class_schedule_id']
        class_schedule = get_object_or_404(ClassSchedule, id=class_schedule_id)
        
        # Only CR can add attachments
        if not self.request.user.is_cr:
            raise permissions.PermissionDenied("Only CR can add attachments.")
        
        serializer.save(class_schedule=class_schedule)


class ClassAttachmentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete a class attachment."""
    queryset = ClassAttachment.objects.all()
    serializer_class = ClassAttachmentSerializer
    
    def get_permissions(self):
        """CR can delete, all authenticated users can view."""
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_destroy(self, instance):
        """Only CR can delete attachments."""
        if not self.request.user.is_cr:
            raise permissions.PermissionDenied("Only CR can delete attachments.")
        instance.delete()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def todays_classes_view(request):
    """Get today's classes."""
    today = date.today()
    classes = ClassSchedule.objects.filter(date=today).order_by('time')
    serializer = ClassScheduleListSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upcoming_classes_view(request):
    """Get upcoming classes."""
    today = date.today()
    classes = ClassSchedule.objects.filter(date__gte=today).order_by('date', 'time')
    serializer = ClassScheduleListSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_classes_view(request):
    """Get classes created by current user (CR only)."""
    if not request.user.is_cr:
        return Response(
            {'error': 'Only CR can view their created classes'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    classes = ClassSchedule.objects.filter(created_by=request.user).order_by('-created_at')
    serializer = ClassScheduleListSerializer(classes, many=True)
    return Response(serializer.data)


class AlarmSettingsListCreateView(generics.ListCreateAPIView):
    """List and create alarm settings for a user."""
    
    def get_queryset(self):
        """Get alarm settings for current user."""
        return AlarmSettings.objects.filter(user=self.request.user)
    
    serializer_class = AlarmSettingsSerializer
    
    def perform_create(self, serializer):
        """Create alarm setting with current user."""
        serializer.save(user=self.request.user)


class AlarmSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete alarm settings."""
    
    def get_queryset(self):
        """Get alarm settings for current user."""
        return AlarmSettings.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use update serializer for updates."""
        if self.request.method in ['PUT', 'PATCH']:
            return AlarmSettingsUpdateSerializer
        return AlarmSettingsSerializer


@api_view(['POST'])
def toggle_alarm_view(request, class_schedule_id):
    """Toggle alarm for a specific class."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    class_schedule = get_object_or_404(ClassSchedule, id=class_schedule_id)
    
    alarm_setting, created = AlarmSettings.objects.get_or_create(
        user=request.user,
        class_schedule=class_schedule,
        defaults={'is_enabled': True, 'alarm_minutes_before': 20}
    )
    
    if not created:
        alarm_setting.is_enabled = not alarm_setting.is_enabled
        alarm_setting.save()
    
    serializer = AlarmSettingsSerializer(alarm_setting)
    return Response(serializer.data)


@api_view(['POST'])
def update_alarm_timing_view(request, class_schedule_id):
    """Update alarm timing for a specific class."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    class_schedule = get_object_or_404(ClassSchedule, id=class_schedule_id)
    alarm_minutes_before = request.data.get('alarm_minutes_before', 20)
    
    alarm_setting, created = AlarmSettings.objects.get_or_create(
        user=request.user,
        class_schedule=class_schedule,
        defaults={'is_enabled': True, 'alarm_minutes_before': alarm_minutes_before}
    )
    
    if not created:
        alarm_setting.alarm_minutes_before = alarm_minutes_before
        alarm_setting.save()
    
    serializer = AlarmSettingsSerializer(alarm_setting)
    return Response(serializer.data)


@api_view(['GET'])
def get_notifications_view(request):
    """Get pending notifications for user."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    from .notification_service import NotificationService
    notifications = NotificationService.get_user_notifications(request.user)
    return Response({'notifications': notifications})


@api_view(['POST'])
def send_test_notification_view(request, class_schedule_id):
    """Send test notification for a specific class."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    from .notification_service import NotificationService
    class_schedule = get_object_or_404(ClassSchedule, id=class_schedule_id)
    
    NotificationService.send_test_notification(request.user, class_schedule)
    
    return Response({'message': 'Test notification sent successfully'})


@api_view(['POST'])
def clear_notifications_view(request):
    """Clear all notifications for user."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    from .notification_service import NotificationService
    NotificationService.clear_user_notifications(request.user)
    return Response({'message': 'Notifications cleared successfully'})


@api_view(['POST'])
def check_alarms_view(request):
    """Manually check and send alarms."""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    from .notification_service import NotificationService
    notifications_sent = NotificationService.check_and_send_alarms()
    return Response({
        'message': f'Sent {len(notifications_sent)} alarm notifications',
        'notifications': notifications_sent
    })
