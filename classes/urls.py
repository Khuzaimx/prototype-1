from django.urls import path
from . import views

urlpatterns = [
    # Class schedules
    path('', views.ClassScheduleListCreateView.as_view(), name='class-list-create'),
    path('<int:pk>/', views.ClassScheduleDetailView.as_view(), name='class-detail'),
    path('today/', views.todays_classes_view, name='today-classes'),
    path('upcoming/', views.upcoming_classes_view, name='upcoming-classes'),
    path('my-classes/', views.my_classes_view, name='my-classes'),
    
    # Class attachments
    path('<int:class_schedule_id>/attachments/', views.ClassAttachmentListCreateView.as_view(), name='attachment-list-create'),
    path('attachments/<int:pk>/', views.ClassAttachmentDetailView.as_view(), name='attachment-detail'),
    
    # Alarm settings
    path('alarms/', views.AlarmSettingsListCreateView.as_view(), name='alarm-settings-list-create'),
    path('alarms/<int:pk>/', views.AlarmSettingsDetailView.as_view(), name='alarm-settings-detail'),
    path('<int:class_schedule_id>/toggle-alarm/', views.toggle_alarm_view, name='toggle-alarm'),
    path('<int:class_schedule_id>/update-alarm-timing/', views.update_alarm_timing_view, name='update-alarm-timing'),
    
    # Notifications
    path('notifications/', views.get_notifications_view, name='get-notifications'),
    path('notifications/clear/', views.clear_notifications_view, name='clear-notifications'),
    path('<int:class_schedule_id>/test-notification/', views.send_test_notification_view, name='test-notification'),
    path('check-alarms/', views.check_alarms_view, name='check-alarms'),
]
