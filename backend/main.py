from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Form
from fastapi.staticfiles import StaticFiles  # ✅ ADDED
from database import db
from auth import create_access_token
from schemas import *
import os
from datetime import timedelta
from bson import ObjectId
import shutil  # ✅ ADDED
# ===== ADD THESE IMPORTS AT TOP =====
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt  # ✅ FIXED: jwt import add kiya
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ===== CORS UPDATED =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://study-routeedu.vercel.app",
        "https://studyrouteedu.netlify.app",
        "https://studyrouteedu.onrender.com",
        "https://studyroute-portal.onrender.com",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ===== STATIC FILES (Uploads) ===== ✅ ADDED
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "admissions"), exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ===== EMAIL CONFIG =====
EMAIL_USER = os.getenv("EMAIL_USER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")

def send_otp_email(to_email, otp):
    print(f"📧 Attempting to send OTP to: {to_email}")  # 👈 YEH ADD KARO
    print(f"🔑 OTP: {otp}")  # 👈 YEH ADD KARO
    try:
        subject = "🔐 StudyRoute - OTP for Account Unlock"
        body = f"""
        <html>
        <body>
            <h2>StudyRoute Admin Panel</h2>
            <p>Your account has been locked due to multiple failed login attempts.</p>
            <p><strong>OTP to unlock your account: {otp}</strong></p>
            <p>This OTP is valid for 10 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <hr>
            <p style="color: #94a3b8;">StudyRoute Education Portal</p>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")  # 👈 YEH ADD KARO
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")  # 👈 YEH ADD KARO
        print(f"❌ Email error: {e}")
        return False

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== ADMIN LOGIN (WITH LOCK & OTP + DEBUG) =====
@app.post("/api/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"🔍 Login attempt: username={username}, password={password}")  # 👈 DEBUG LINE
    admin = db.admins.find_one({"username": username})
    if not admin:
        print("❌ Admin not found")  # 👈 DEBUG
        raise HTTPException(status_code=401, detail="Invalid credentials")
    print(f"📦 DB Password: {admin.get('password')}")  # 👈 DEBUG
    print(f"📦 DB Email: {admin.get('email')}")  # 👈 DEBUG
    
    # Check if account is locked
    if admin.get("is_locked", False):
        lock_until = admin.get("lock_until")
        if lock_until and datetime.now() < lock_until:
            remaining = int((lock_until - datetime.now()).total_seconds() / 60)
            raise HTTPException(status_code=423, detail=f"Account locked. Try after {remaining} minutes.")
        else:
            # Lock expired, reset
            db.admins.update_one(
                {"username": username},
                {"$set": {"is_locked": False, "failed_attempts": 0, "lock_until": None}}
            )
    
    # Check password
    if password != admin.get("password"):
        print("❌ Password mismatch")  # 👈 DEBUG
        # Increment failed attempts
        failed = admin.get("failed_attempts", 0) + 1
        update_data = {"failed_attempts": failed}
        
        if failed >= 3:
            # Lock account for 15 minutes
            lock_until = datetime.now() + timedelta(minutes=15)
            update_data["is_locked"] = True
            update_data["lock_until"] = lock_until
            
            # Generate OTP
            otp = generate_otp()
            update_data["otp"] = otp
            update_data["otp_expires"] = datetime.now() + timedelta(minutes=10)
            
            db.admins.update_one({"username": username}, {"$set": update_data})
            
            # Send OTP email
            email_sent = send_otp_email(admin.get("email", EMAIL_USER), otp)
            print(f"📧 OTP sent: {otp}, Status: {email_sent}")  # 👈 DEBUG
            
            raise HTTPException(status_code=423, detail="Account locked. OTP sent to your email.")
        else:
            db.admins.update_one({"username": username}, {"$set": update_data})
            remaining = 3 - failed
            raise HTTPException(status_code=401, detail=f"Invalid credentials. {remaining} attempts remaining.")
    
    # Login success - reset attempts
    print("✅ Login successful!")  # 👈 DEBUG
    db.admins.update_one(
        {"username": username},
        {"$set": {"failed_attempts": 0, "is_locked": False, "lock_until": None, "otp": None, "otp_expires": None}}
    )
    token = create_access_token(data={"sub": username})
    return {"access_token": token, "token_type": "bearer"}

# ===== VERIFY OTP =====
@app.post("/api/auth/verify-otp")
async def verify_otp(username: str = Form(...), otp: str = Form(...)):
    print(f"🔍 OTP verify: username={username}, otp={otp}")  # 👈 DEBUG
    admin = db.admins.find_one({"username": username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    if not admin.get("is_locked", False):
        raise HTTPException(status_code=400, detail="Account is not locked")
    
    stored_otp = admin.get("otp")
    otp_expires = admin.get("otp_expires")
    
    if not stored_otp or not otp_expires:
        raise HTTPException(status_code=400, detail="No OTP found. Please try login again.")
    
    if datetime.now() > otp_expires:
        raise HTTPException(status_code=400, detail="OTP expired. Please try login again.")
    
    if otp != stored_otp:
        print(f"❌ OTP mismatch: {otp} != {stored_otp}")  # 👈 DEBUG
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    print("✅ OTP verified!")  # 👈 DEBUG
    # Unlock account
    db.admins.update_one(
        {"username": username},
        {"$set": {"is_locked": False, "failed_attempts": 0, "lock_until": None, "otp": None, "otp_expires": None}}
    )
    return {"status": "success", "message": "Account unlocked successfully"}

# ===== SEND OTP FOR PASSWORD CHANGE (ADDED) =====
@app.post("/api/auth/send-change-otp")
async def send_change_otp(username: str = Depends(verify_token)):
    admin = db.admins.find_one({"username": username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    otp = generate_otp()
    otp_expires = datetime.now() + timedelta(minutes=5)
    
    db.admins.update_one(
        {"username": username},
        {"$set": {"change_otp": otp, "change_otp_expires": otp_expires}}
    )
    
    email_sent = send_otp_email(admin.get("email"), otp)
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")
    
    return {"status": "success"}

# ===== CHANGE PASSWORD WITH OTP (UPDATED) =====
@app.post("/api/admin/change-password")
async def change_password(
    request: dict,
    username: str = Depends(verify_token)
):
    current = request.get("currentPassword")
    new = request.get("newPassword")
    otp = request.get("otp")
    
    admin = db.admins.find_one({"username": username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Verify OTP
    stored_otp = admin.get("change_otp")
    otp_expires = admin.get("change_otp_expires")
    
    if not stored_otp or not otp_expires:
        raise HTTPException(status_code=400, detail="No OTP found. Please request a new OTP.")
    
    if datetime.now() > otp_expires:
        raise HTTPException(status_code=400, detail="OTP expired. Please request a new OTP.")
    
    if otp != stored_otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    if current != admin.get("password"):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    if len(new) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    db.admins.update_one(
        {"username": username},
        {"$set": {"password": new, "change_otp": None, "change_otp_expires": None}}
    )
    return {"status": "success", "message": "Password changed successfully"}

# ===== COLLEGES =====
@app.get("/api/colleges/")
async def get_colleges(search: str = "", district: str = ""):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if district:
        query["district"] = district
    return list(db.colleges.find(query, {"_id": 0}))

@app.post("/api/colleges/")
async def create_college(college: CollegeBase):
    db.colleges.insert_one(college.dict())
    return {"status": "created"}

@app.put("/api/colleges/{name}")
async def update_college(name: str, college: CollegeBase):
    db.colleges.update_one({"name": name}, {"$set": college.dict()})
    return {"status": "updated"}

@app.delete("/api/colleges/{name}")
async def delete_college(name: str):
    db.colleges.delete_one({"name": name})
    return {"status": "deleted"}

# ===== COURSES =====
@app.get("/api/courses/")
async def get_courses(search: str = ""):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    return list(db.courses.find(query, {"_id": 0}))

@app.post("/api/courses/")
async def create_course(course: CourseBase):
    db.courses.insert_one(course.dict())
    return {"status": "created"}

@app.put("/api/courses/{name}")
async def update_course(name: str, course: CourseBase):
    db.courses.update_one({"name": name}, {"$set": course.dict()})
    return {"status": "updated"}

@app.delete("/api/courses/{name}")
async def delete_course(name: str):
    db.courses.delete_one({"name": name})
    return {"status": "deleted"}

# ===== BSCC =====
@app.get("/api/bscc/")
async def get_bscc(search: str = ""):
    query = {}
    if search:
        query["course_name"] = {"$regex": search, "$options": "i"}
    return list(db.bscc_courses.find(query, {"_id": 0}))

@app.post("/api/bscc/")
async def create_bscc(bscc: BSCCBase):
    db.bscc_courses.insert_one(bscc.dict())
    return {"status": "created"}

@app.put("/api/bscc/{course_name}")
async def update_bscc(course_name: str, bscc: BSCCBase):
    db.bscc_courses.update_one({"course_name": course_name}, {"$set": bscc.dict()})
    return {"status": "updated"}

@app.delete("/api/bscc/{course_name}")
async def delete_bscc(course_name: str):
    db.bscc_courses.delete_one({"course_name": course_name})
    return {"status": "deleted"}

# ===== PARTNERS =====
@app.get("/api/partners/")
async def get_partners(search: str = ""):
    query = {}
    if search:
        query["district"] = {"$regex": search, "$options": "i"}
    return list(db.partners.find(query, {"_id": 0}))

@app.post("/api/partners/")
async def create_partner(partner: PartnerBase):
    db.partners.insert_one(partner.dict())
    return {"status": "created"}

@app.put("/api/partners/{name}")
async def update_partner(name: str, partner: PartnerBase):
    db.partners.update_one({"name": name}, {"$set": partner.dict()})
    return {"status": "updated"}

@app.delete("/api/partners/{name}")
async def delete_partner(name: str):
    db.partners.delete_one({"name": name})
    return {"status": "deleted"}

# ===== FEEDBACKS =====
@app.get("/api/feedbacks/")
async def get_feedbacks(approved: bool = None):
    query = {}
    if approved is not None:
        query["approved"] = approved
    feedbacks = list(db.feedbacks.find(query))
    for fb in feedbacks:
        if "_id" in fb:
            fb["_id"] = str(fb["_id"])
    return feedbacks

@app.post("/api/feedbacks/")
async def create_feedback(fb: dict):
    required = ["name", "district", "rating", "message"]
    for field in required:
        if field not in fb:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    fb["approved"] = fb.get("approved", False)
    result = db.feedbacks.insert_one(fb)
    return {"status": "created", "id": str(result.inserted_id)}

@app.put("/api/feedbacks/{id}")
async def update_feedback(id: str, update_data: dict):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        update = {}
        if "approved" in update_data:
            update["approved"] = update_data["approved"]
        if "reply" in update_data:
            update["reply"] = update_data["reply"]
        if not update:
            raise HTTPException(status_code=400, detail="No fields to update")
        result = db.feedbacks.update_one({"_id": ObjectId(id)}, {"$set": update})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/feedbacks/{id}")
async def delete_feedback(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        result = db.feedbacks.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== CONTENT =====
@app.get("/api/content/")
async def get_content():
    content = db.website_content.find_one({}, {"_id": 0})
    if not content:
        return {"google_form_link": "#"}
    return {"google_form_link": content.get("google_form_link", "#")}

@app.post("/api/content/")
async def update_content(content: dict):
    db.website_content.update_one(
        {},
        {"$set": {"google_form_link": content.get("google_form_link", "")}},
        upsert=True
    )
    return {"status": "updated"}

# ===== ADMIN STATS =====
@app.get("/api/admin/stats")
async def get_stats():
    return {
        "colleges": db.colleges.count_documents({}),
        "courses": db.courses.count_documents({}),
        "bscc": db.bscc_courses.count_documents({}),
        "partners": db.partners.count_documents({}),
        "feedbacks": db.feedbacks.count_documents({}),
        "admissions": db.admissions.count_documents({})
    }

# ===== ADMISSIONS (FILE SIZE FIXED) =====
@app.post("/api/admissions/")
async def create_admission(
    referralSource: str = Form(...),
    referrerName: str = Form(""),
    fullName: str = Form(...),
    fatherName: str = Form(...),
    motherName: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    mobile: str = Form(...),
    altMobile: str = Form(""),
    email: str = Form(...),
    address: str = Form(...),
    block: str = Form(...),
    district: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    tenthYear: str = Form(...),
    tenthPercent: str = Form(...),
    twelfthYear: str = Form(...),
    twelfthPercent: str = Form(...),
    twelfthStream: str = Form(...),
    gradYear: str = Form(""),
    gradPercent: str = Form(""),
    gradStream: str = Form(""),
    preferredCourse: str = Form(...),
    preferredCollege: str = Form(...),
    bsccInterest: str = Form(...),
    tenthMarksheet: UploadFile = File(...),
    twelfthMarksheet: UploadFile = File(...),
    gradMarksheet: UploadFile = File(None),
    aadhar: UploadFile = File(...),
    photo: UploadFile = File(...),
    signature: UploadFile = File(...),
    residentialCert: UploadFile = File(None),
    casteCert: UploadFile = File(None)
):
    from datetime import datetime
    import os, shutil
    try:
        # ===== FILE SIZE CHECKS (FIXED - SEEK METHOD) =====
        # Photo & Signature: 10-50 KB
        if photo:
            photo.file.seek(0, 2)
            photo_size = photo.file.tell()
            photo.file.seek(0)
            if photo_size > 51200:
                raise HTTPException(status_code=400, detail="Photo exceeds 50KB limit")
            if photo_size < 10240:
                raise HTTPException(status_code=400, detail="Photo is too small (min 10 KB)")

        if signature:
            signature.file.seek(0, 2)
            sig_size = signature.file.tell()
            signature.file.seek(0)
            if sig_size > 51200:
                raise HTTPException(status_code=400, detail="Signature exceeds 50KB limit")
            if sig_size < 10240:
                raise HTTPException(status_code=400, detail="Signature is too small (min 10 KB)")

        # Other documents: 100-600 KB
        docs = [
            ("10th Marksheet", tenthMarksheet),
            ("12th Marksheet", twelfthMarksheet),
            ("Aadhar", aadhar)
        ]
        if gradMarksheet:
            docs.append(("Graduation Marksheet", gradMarksheet))
        if residentialCert:
            docs.append(("Residential Certificate", residentialCert))
        if casteCert:
            docs.append(("Caste Certificate", casteCert))

        for name, file in docs:
            if file:
                file.file.seek(0, 2)
                file_size = file.file.tell()
                file.file.seek(0)
                if file_size > 614400:
                    raise HTTPException(status_code=400, detail=f"{name} exceeds 600KB limit")
                if file_size < 102400:
                    raise HTTPException(status_code=400, detail=f"{name} is too small (min 100 KB)")

        # ===== SAVE FILES =====
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads", "admissions")
        os.makedirs(upload_dir, exist_ok=True)
        
        def save_file(file: UploadFile, prefix: str):
            if not file: 
                return None
            safe_name = fullName.replace(" ", "_")
            ext = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
            filename = f"{prefix}_{safe_name}.{ext}"
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, "wb") as f:
                shutil.copyfileobj(file.file, f)
            return filepath
        
        admission_data = {
            "referralSource": referralSource, 
            "referrerName": referrerName,
            "fullName": fullName, 
            "fatherName": fatherName, 
            "motherName": motherName,
            "dob": dob, 
            "gender": gender, 
            "mobile": mobile, 
            "altMobile": altMobile,
            "email": email, 
            "address": address, 
            "block": block, 
            "district": district,
            "state": state, 
            "pincode": pincode,
            "tenthYear": tenthYear, 
            "tenthPercent": tenthPercent,
            "twelfthYear": twelfthYear, 
            "twelfthPercent": twelfthPercent, 
            "twelfthStream": twelfthStream,
            "gradYear": gradYear, 
            "gradPercent": gradPercent, 
            "gradStream": gradStream,
            "preferredCourse": preferredCourse, 
            "preferredCollege": preferredCollege,
            "bsccInterest": bsccInterest,
            "tenthMarksheet": save_file(tenthMarksheet, "tenth"),
            "twelfthMarksheet": save_file(twelfthMarksheet, "twelfth"),
            "gradMarksheet": save_file(gradMarksheet, "grad") if gradMarksheet else None,
            "aadhar": save_file(aadhar, "aadhar"),
            "photo": save_file(photo, "photo"),
            "signature": save_file(signature, "signature"),
            "residentialCert": save_file(residentialCert, "residential") if residentialCert else None,
            "casteCert": save_file(casteCert, "caste") if casteCert else None,
            "submittedAt": datetime.now().isoformat()
        }
        result = db.admissions.insert_one(admission_data)
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admissions/")
async def get_admissions():
    admissions = list(db.admissions.find())
    for a in admissions:
        if "_id" in a: a["_id"] = str(a["_id"])
    return admissions

@app.delete("/api/admissions/{id}")
async def delete_admission(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = db.admissions.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admission not found")
    return {"status": "deleted"}


# Admission section se download krne ke liye 
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    # Absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "uploads", "admissions", filename)
    
    print(f"🔍 Looking for: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    return FileResponse(
        file_path,
        filename=filename,
        media_type="application/octet-stream"
    )