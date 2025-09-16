# 🎓 ClassAlarm Setup Guide - GIKI Domain Restriction

## 🚀 Quick Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py migrate
```

### **3. Create Admin & Demo Data**
```bash
python setup_admin.py
```

### **4. Start Server**
```bash
python manage.py runserver
```

### **5. Access Applications**
- **Admin Panel**: `admin-panel.html`
- **User Interface**: `frontend-with-backend.html`
- **Django Admin**: `http://localhost:8000/admin/`

---

## 🔐 **Authentication System**

### **Domain Restriction**
- ✅ **Only @giki.edu.pk emails allowed**
- ✅ **Automatic role assignment based on admin assignments**
- ✅ **Superuser admin for CR management**

### **User Roles**
- **Admin**: Superuser with CR assignment privileges
- **CR**: Class Representative (assigned by admin)
- **Student**: Regular student (default role)

---

## 👨‍💼 **Admin Features**

### **Superuser Admin** (`admin@giki.edu.pk`)
- **Password**: `admin123`
- **Access**: Django admin panel + custom admin panel
- **Permissions**: Assign/revoke CR roles, manage users

### **CR Assignment Process**
1. Admin assigns CR email via admin panel
2. User with that email automatically gets CR role
3. CR can create/edit/delete classes
4. Admin can revoke CR role anytime

---

## 📱 **User Interface**

### **Login Process**
1. User enters `@giki.edu.pk` email
2. System validates domain
3. User gets appropriate role (CR/Student)
4. Access to relevant features

### **CR Features**
- Create/edit/delete classes
- Upload attachments
- View all classes

### **Student Features**
- View today's classes
- Download attachments
- See alarm notifications

---

## 🗄️ **Database Models**

### **User Model**
```python
- email (giki.edu.pk domain only)
- username
- role (auto-assigned based on CR assignments)
- is_staff, is_superuser
```

### **CRAssignment Model**
```python
- email (giki.edu.pk domain only)
- assigned_by (admin user)
- assigned_at
- is_active
```

### **ClassSchedule Model**
```python
- created_by (CR user)
- subject, venue, date, time
- note (optional)
- attachments
```

---

## 🔧 **API Endpoints**

### **Authentication**
- `POST /api/auth/demo-login/` - Login with giki.edu.pk email
- `POST /api/auth/login/` - Regular login
- `POST /api/auth/register/` - User registration

### **Admin CR Management**
- `GET /api/auth/admin/cr-list/` - List CR assignments
- `POST /api/auth/admin/assign-cr/` - Assign CR role
- `POST /api/auth/admin/revoke-cr/` - Revoke CR role

### **Classes**
- `GET /api/classes/` - List classes
- `POST /api/classes/` - Create class (CR only)
- `PUT /api/classes/{id}/` - Update class (CR only)
- `DELETE /api/classes/{id}/` - Delete class (CR only)

---

## 🎯 **Usage Examples**

### **Admin Workflow**
1. Login to admin panel with `admin@giki.edu.pk`
2. Assign CR role to `student1@giki.edu.pk`
3. User `student1@giki.edu.pk` automatically becomes CR
4. CR can now create classes and manage schedule

### **CR Workflow**
1. Login with assigned CR email
2. Navigate to CR Panel
3. Create classes with subjects/venues
4. Upload attachments
5. Edit/delete classes as needed

### **Student Workflow**
1. Login with any `@giki.edu.pk` email
2. View today's classes
3. Download attachments
4. See alarm notifications

---

## 🔒 **Security Features**

### **Domain Validation**
- Email validation at model level
- API endpoint validation
- Frontend validation

### **Role-Based Access**
- Admin: Full access to CR management
- CR: Class management only
- Student: Read-only access

### **JWT Authentication**
- Secure token-based auth
- Role information in tokens
- Automatic token refresh

---

## 📊 **Admin Panel Features**

### **CR Assignment Interface**
- Assign CR role to any `@giki.edu.pk` email
- View all CR assignments
- Revoke CR roles
- Track assignment history

### **User Management**
- View all users
- See user roles
- Manage user status
- Track user activity

---

## 🚀 **Deployment**

### **Development**
```bash
python manage.py runserver
# Access: http://localhost:8000/
```

### **Production**
```bash
# Set environment variables
export SECRET_KEY="your-secret-key"
export DEBUG=False
export DATABASE_URL="postgresql://user:pass@host:port/db"

# Run migrations
python manage.py migrate

# Create superuser
python setup_admin.py

# Deploy with Gunicorn
gunicorn classalarm_backend.wsgi:application
```

---

## 🎉 **Ready to Use!**

The system is now configured with:
- ✅ GIKI domain restriction
- ✅ Admin CR assignment system
- ✅ Automatic role assignment
- ✅ Secure authentication
- ✅ Role-based access control

**Start the server and begin managing your class schedules!**
