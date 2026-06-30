from database import db

admin_data = {
    "username": "admin",
    "password": "admin123",
    "role": "super_admin"
}

if db.admins.find_one({"username": "admin"}):
    print("✅ Admin already exists!")
else:
    db.admins.insert_one(admin_data)
    print("✅ Admin created successfully!")
    print("   Username: admin")
    print("   Password: admin123")