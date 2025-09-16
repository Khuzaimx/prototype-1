#!/usr/bin/env python
"""
Simple alarm checker that runs every minute.
Run this in a separate terminal: python run_alarm_checker.py
"""

import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classalarm_backend.settings')
django.setup()

from classes.notification_service import NotificationService

def run_alarm_checker():
    """Run alarm checker every minute."""
    print("🔔 Alarm Checker Started - Checking every 60 seconds...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            notifications_sent = NotificationService.check_and_send_alarms()
            
            if notifications_sent:
                print(f"[{time.strftime('%H:%M:%S')}] Sent {len(notifications_sent)} notifications")
                for notification in notifications_sent:
                    print(f"  - {notification['user']}: {notification['class']} ({notification['time']}m)")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] No notifications to send")
            
            time.sleep(60)  # Wait 60 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Alarm Checker Stopped")

if __name__ == '__main__':
    run_alarm_checker()
