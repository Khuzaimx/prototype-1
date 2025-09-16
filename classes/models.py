from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class ClassSchedule(models.Model):
    """Model for class schedules."""
    
    SUBJECT_CHOICES = [
        ('se221', 'SE221'),
        ('cs221', 'CS221'),
        ('ee201', 'EE201'),
        ('math101', 'MATH101'),
        ('phy201', 'PHY201'),
        ('is301', 'IS301'),
    ]
    
    VENUE_CHOICES = [
        ('acb-lh1', 'ACB-LH1'),
        ('acb-lh2', 'ACB-LH2'),
        ('acb-lh3', 'ACB-LH3'),
        ('acb-lh4', 'ACB-LH4'),
        ('acb-lh5', 'ACB-LH5'),
        ('acb-lh6', 'ACB-LH6'),
        ('acb-lh7', 'ACB-LH7'),
        ('fsce-lh1', 'FSCE-LH1'),
        ('fsce-lh2', 'FSCE-LH2'),
    ]
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classes')
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    venue = models.CharField(max_length=10, choices=VENUE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'class_schedules'
        ordering = ['-created_at']
        verbose_name = 'Class Schedule'
        verbose_name_plural = 'Class Schedules'
    
    def __str__(self):
        return f"{self.get_subject_display()} - {self.get_venue_display()} ({self.date} {self.time})"


class ClassAttachment(models.Model):
    """Model for class attachments."""
    
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(
        upload_to='class_attachments/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'])]
    )
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'class_attachments'
        ordering = ['-uploaded_at']
        verbose_name = 'Class Attachment'
        verbose_name_plural = 'Class Attachments'
    
    def __str__(self):
        return f"{self.original_filename} ({self.class_schedule.get_subject_display()})"
    
    @property
    def file_size_mb(self):
        """Return file size in MB."""
        return round(self.file_size / (1024 * 1024), 2)


class AlarmSettings(models.Model):
    """Model for student alarm preferences for each class."""
    
    ALARM_CHOICES = [
        (5, '5 minutes before'),
        (10, '10 minutes before'),
        (15, '15 minutes before'),
        (20, '20 minutes before'),
        (30, '30 minutes before'),
        (60, '1 hour before'),
        (120, '2 hours before'),
        (180, '3 hours before'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarm_settings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='alarm_settings')
    is_enabled = models.BooleanField(default=True)
    alarm_minutes_before = models.IntegerField(choices=ALARM_CHOICES, default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alarm_settings'
        verbose_name = 'Alarm Setting'
        verbose_name_plural = 'Alarm Settings'
        unique_together = ['user', 'class_schedule']
        ordering = ['-created_at']
    
    def __str__(self):
        status = "ON" if self.is_enabled else "OFF"
        return f"{self.user.email} - {self.class_schedule} - Alarm {status} ({self.alarm_minutes_before}m)"


class NotificationLog(models.Model):
    """Model to track sent notifications."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_logs')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='notification_logs')
    notification_type = models.CharField(max_length=20, choices=[
        ('alarm', 'Alarm Notification'),
        ('reminder', 'Reminder Notification'),
        ('test', 'Test Notification'),
    ])
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    
    class Meta:
        db_table = 'notification_logs'
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.notification_type} - {self.sent_at}"
