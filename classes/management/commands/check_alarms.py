"""
Django management command to check and send alarm notifications.
"""

from django.core.management.base import BaseCommand
from classes.notification_service import NotificationService


class Command(BaseCommand):
    help = 'Check for classes that need alarm notifications and send them'

    def handle(self, *args, **options):
        self.stdout.write('Checking for alarm notifications...')
        
        notifications_sent = NotificationService.check_and_send_alarms()
        
        if notifications_sent:
            self.stdout.write(
                self.style.SUCCESS(f'Sent {len(notifications_sent)} alarm notifications')
            )
            for notification in notifications_sent:
                self.stdout.write(f'  - {notification["user"]}: {notification["class"]} ({notification["time"]}m)')
        else:
            self.stdout.write('No alarm notifications to send')
