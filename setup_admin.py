#!/usr/bin/env python
"""
Setup script to create superuser admin for ClassAlarm.
Run this after migrations: python setup_admin.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classalarm_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import CRAssignment

User = get_user_model()

def create_superuser():
    """Create superuser admin."""
    email = 'admin@giki.edu.pk'
    username = 'admin'
    password = 'admin123'
    
    try:
        # Check if superuser already exists
        if User.objects.filter(email=email).exists():
            print(f"Superuser {email} already exists!")
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password
        )
        
        print(f"✅ Superuser created successfully!")
        print(f"   Email: {email}")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Role: {user.role}")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

def create_demo_cr():
    """Create demo CR assignment."""
    email = 'cr@giki.edu.pk'
    
    try:
        # Check if CR assignment already exists
        if CRAssignment.objects.filter(email=email, is_active=True).exists():
            print(f"CR assignment for {email} already exists!")
            return
        
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Create superuser first.")
            return
        
        # Create CR assignment
        cr_assignment = CRAssignment.objects.create(
            email=email,
            assigned_by=admin_user
        )
        
        print(f"✅ Demo CR assignment created!")
        print(f"   Email: {email}")
        print(f"   Assigned by: {admin_user.email}")
        
    except Exception as e:
        print(f"❌ Error creating CR assignment: {e}")

def main():
    """Main setup function."""
    print("🚀 Setting up ClassAlarm Admin...")
    print("=" * 50)
    
    # Create superuser
    print("\n1. Creating superuser admin...")
    create_superuser()
    
    # Create demo CR assignment
    print("\n2. Creating demo CR assignment...")
    create_demo_cr()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://localhost:8000/admin/")
    print("3. Login with: admin@giki.edu.pk / admin123")
    print("4. Open: admin-panel.html for CR management")
    print("5. Open: frontend-with-backend.html for user interface")

if __name__ == '__main__':
    main()
