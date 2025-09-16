from django.contrib import admin
from .models import ClassSchedule, ClassAttachment, AlarmSettings, NotificationLog


class ClassAttachmentInline(admin.TabularInline):
    """Inline admin for class attachments."""
    model = ClassAttachment
    extra = 0
    readonly_fields = ('file_size', 'uploaded_at')


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    """Admin for class schedules."""
    list_display = ('subject', 'venue', 'date', 'time', 'created_by', 'created_at')
    list_filter = ('subject', 'venue', 'date', 'created_by', 'created_at')
    search_fields = ('subject', 'venue', 'note', 'created_by__email')
    ordering = ('-created_at',)
    inlines = [ClassAttachmentInline]
    
    fieldsets = (
        ('Class Details', {
            'fields': ('subject', 'venue', 'date', 'time')
        }),
        ('Additional Info', {
            'fields': ('note', 'created_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClassAttachment)
class ClassAttachmentAdmin(admin.ModelAdmin):
    """Admin for class attachments."""
    list_display = ('original_filename', 'class_schedule', 'file_size_mb', 'uploaded_at')
    list_filter = ('uploaded_at', 'class_schedule__subject')
    search_fields = ('original_filename', 'class_schedule__subject')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('File Info', {
            'fields': ('class_schedule', 'file', 'original_filename', 'file_size')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('file_size', 'uploaded_at')


@admin.register(AlarmSettings)
class AlarmSettingsAdmin(admin.ModelAdmin):
    """Admin for alarm settings."""
    list_display = ('user', 'class_schedule', 'is_enabled', 'alarm_minutes_before', 'created_at')
    list_filter = ('is_enabled', 'alarm_minutes_before', 'created_at')
    search_fields = ('user__email', 'class_schedule__subject')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Alarm Settings', {
            'fields': ('user', 'class_schedule', 'is_enabled', 'alarm_minutes_before')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """Admin for notification logs."""
    list_display = ('user', 'class_schedule', 'notification_type', 'sent_at')
    list_filter = ('notification_type', 'sent_at', 'user')
    search_fields = ('user__email', 'class_schedule__subject', 'message')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at',)
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'class_schedule', 'notification_type', 'message')
        }),
        ('Timestamps', {
            'fields': ('sent_at',),
            'classes': ('collapse',)
        }),
    )