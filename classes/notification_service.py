"""
Notification service for ClassAlarm system.
"""

import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache
from .models import ClassSchedule, AlarmSettings, NotificationLog


class NotificationService:
    """Service for managing notifications and alarms."""
    
    @staticmethod
    def check_and_send_alarms():
        """Check for classes that need alarm notifications and send them."""
        now = timezone.now()
        
        # Get all classes happening today
        today = now.date()
        classes_today = ClassSchedule.objects.filter(date=today)
        
        notifications_sent = []
        
        for class_schedule in classes_today:
            class_time = datetime.combine(today, class_schedule.time)
            class_datetime = timezone.make_aware(class_time)
            
            # Get all alarm settings for this class
            alarm_settings = AlarmSettings.objects.filter(
                class_schedule=class_schedule,
                is_enabled=True
            )
            
            for alarm_setting in alarm_settings:
                alarm_time = class_datetime - timedelta(minutes=alarm_setting.alarm_minutes_before)
                
                # Check if it's time to send the alarm
                if now >= alarm_time:
                    # Check if we already sent this alarm
                    cache_key = f"alarm_sent_{alarm_setting.id}_{alarm_time.date()}"
                    if not cache.get(cache_key):
                        NotificationService.send_alarm_notification(alarm_setting)
                        cache.set(cache_key, True, 3600)  # Cache for 1 hour
                        notifications_sent.append({
                            'user': alarm_setting.user.email,
                            'class': class_schedule.get_subject_display(),
                            'time': alarm_setting.alarm_minutes_before
                        })
        
        return notifications_sent
    
    @staticmethod
    def send_alarm_notification(alarm_setting):
        """Send alarm notification to user."""
        class_schedule = alarm_setting.class_schedule
        user = alarm_setting.user
        
        message = f"🔔 Class Reminder!\n{class_schedule.get_subject_display()} starts in {alarm_setting.alarm_minutes_before} minutes!\n📍 {class_schedule.get_venue_display()} at {class_schedule.time}"
        
        # Log the notification
        NotificationLog.objects.create(
            user=user,
            class_schedule=class_schedule,
            notification_type='alarm',
            message=message
        )
        
        # Store notification in cache for frontend to pick up
        cache_key = f"notification_{user.id}"
        notifications = cache.get(cache_key, [])
        notifications.append({
            'id': len(notifications) + 1,
            'type': 'alarm',
            'title': 'ClassAlarm - Class Reminder',
            'message': message,
            'timestamp': timezone.now().isoformat(),
            'class_id': class_schedule.id
        })
        cache.set(cache_key, notifications, 3600)  # Cache for 1 hour
    
    @staticmethod
    def send_test_notification(user, class_schedule):
        """Send test notification to user."""
        message = f"🔔 Test Notification!\n{class_schedule.get_subject_display()} - This is a test notification.\n📍 {class_schedule.get_venue_display()} at {class_schedule.time}"
        
        # Log the notification
        NotificationLog.objects.create(
            user=user,
            class_schedule=class_schedule,
            notification_type='test',
            message=message
        )
        
        # Store notification in cache for frontend to pick up
        cache_key = f"notification_{user.id}"
        notifications = cache.get(cache_key, [])
        notifications.append({
            'id': len(notifications) + 1,
            'type': 'test',
            'title': 'ClassAlarm - Test Notification',
            'message': message,
            'timestamp': timezone.now().isoformat(),
            'class_id': class_schedule.id
        })
        cache.set(cache_key, notifications, 3600)
    
    @staticmethod
    def get_user_notifications(user):
        """Get pending notifications for user."""
        cache_key = f"notification_{user.id}"
        notifications = cache.get(cache_key, [])
        return notifications
    
    @staticmethod
    def clear_user_notifications(user):
        """Clear all notifications for user."""
        cache_key = f"notification_{user.id}"
        cache.delete(cache_key)
    
    @staticmethod
    def schedule_alarm_check():
        """Schedule periodic alarm checks."""
        # This would be called by a cron job or Celery task
        return NotificationService.check_and_send_alarms()
