# 🚀 ElderConnect - Local Setup (No Docker)

Running locally will be MUCH easier to debug and work with!

---

## 📋 **Prerequisites**

You'll need to install:

1. **Python 3.10+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download here](https://nodejs.org/)
3. **PostgreSQL 15** - [Download here](https://www.postgresql.org/download/windows/)

---

## ✅ **STEP 1: Install PostgreSQL**

### **Download & Install:**
1. Go to: https://www.postgresql.org/download/windows/
2. Download the installer
3. Run installer
4. **IMPORTANT:** Remember the password you set for `postgres` user!
5. Default port: `5432` (keep this)

### **Create Database:**

After installation, open **pgAdmin** (comes with PostgreSQL):

1. Right-click "Databases" → "Create" → "Database"
2. Name: `elderconnect_db`
3. Owner: `postgres`
4. Click "Save"

**OR use command line:**
```powershell
# Open Command Prompt and run:
psql -U postgres
# Enter your postgres password

# Then in psql:
CREATE DATABASE elderconnect_db;
\q
```

---

## ✅ **STEP 2: Setup Backend**

### **Open PowerShell in the project folder:**

```powershell
cd backend
```

### **Create Virtual Environment:**

```powershell
python -m venv venv
```

### **Activate Virtual Environment:**

```powershell
.\venv\Scripts\Activate
```

You should see `(venv)` in your prompt now.

### **Install Dependencies:**

```powershell
pip install -r requirements.txt
```

### **Create .env file:**

Create a file `backend/.env` with this content:

```env
# Database
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/elderconnect_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# CORS
FRONTEND_URL=http://localhost:5173

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Flask
FLASK_APP=run.py
FLASK_ENV=development
```

**IMPORTANT:** Replace `YOUR_POSTGRES_PASSWORD` with your actual postgres password!

### **Create Database Tables:**

```powershell
python init_db.py
```

You should see:
```
============================================================
ElderConnect Database Initialization
============================================================
✓ users
✓ elder_profiles
✓ caregiver_profiles
✓ bookings
✓ reviews
✓ payments
✅ Total: 6 tables created
```

### **Seed Test Data:**

```powershell
python seed_data.py
```

You should see:
```
✅ DATABASE SEEDING COMPLETE!
📊 Summary:
  • 3 Elder users
  • 5 Caregiver users
  • 6 Bookings
```

### **Start Backend Server:**

```powershell
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

**✅ Keep this terminal open! Backend is now running!**

---

## ✅ **STEP 3: Setup Frontend**

### **Open NEW PowerShell window:**

```powershell
cd frontend
```

### **Install Dependencies:**

```powershell
npm install
```

This might take a few minutes...

### **Create .env.local file:**

Create a file `frontend/.env.local` with this content:

```env
VITE_API_URL=http://localhost:5000
```

### **Start Frontend Server:**

```powershell
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**✅ Keep this terminal open too! Frontend is now running!**

---

## 🎉 **STEP 4: Test the Application**

### **Open Browser:**

1. Go to: **http://localhost:5173**
2. You should see the login page

### **Login:**
- Email: `john.smith@email.com`
- Password: `Elder123!`

### **Test:**
- Dashboard should load
- Click "Find Caregivers"
- You should see 4 caregivers!
- **NO CORS ERRORS!**

---

## 📊 **Verify in pgAdmin**

1. Open pgAdmin
2. Expand: Servers → PostgreSQL 15 → Databases → elderconnect_db → Schemas → public → Tables
3. You should see all 6 tables!
4. Right-click `users` → View/Edit Data → All Rows
5. You should see 8 users!

---

## 🔧 **Common Issues & Fixes**

### **Issue: "pip: command not found"**

Python not installed or not in PATH.

**Fix:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation

### **Issue: "psql: command not found"**

PostgreSQL not in PATH.

**Fix:**
Add to PATH: `C:\Program Files\PostgreSQL\15\bin`

### **Issue: "password authentication failed"**

Wrong password in `.env` file.

**Fix:**
1. Check your postgres password
2. Update `DATABASE_URL` in `backend/.env`

### **Issue: "Port 5000 already in use"**

Something else using port 5000.

**Fix:**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### **Issue: "Port 5173 already in use"**

Docker frontend still running.

**Fix:**
```powershell
docker compose down
```

### **Issue: Backend starts but crashes immediately**

Check logs in the terminal. Usually database connection issue.

**Fix:**
1. Make sure PostgreSQL is running
2. Check DATABASE_URL in `.env`
3. Make sure database `elderconnect_db` exists

---

## 🎯 **Quick Start Commands**

### **Every time you want to run the app:**

**Terminal 1 (Backend):**
```powershell
cd backend
.\venv\Scripts\Activate
python run.py
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev
```

**Then open:** http://localhost:5173

---

## 🔄 **Reset Database**

If you need to start fresh:

```powershell
cd backend
.\venv\Scripts\Activate
python init_db.py
python seed_data.py
```

---

## 📝 **Development Tips**

### **Backend Auto-Reload:**
Flask auto-reloads when you change Python files!

### **Frontend Hot-Reload:**
Vite auto-reloads when you change React files!

### **Check Backend Logs:**
Just look at the terminal where `python run.py` is running

### **Check Database:**
Use pgAdmin or:
```powershell
psql -U postgres -d elderconnect_db
SELECT * FROM users;
```

---

## ✅ **Advantages of Local Setup**

1. ✅ **No Docker issues**
2. ✅ **Easier to debug** - see logs directly
3. ✅ **Faster startup** - no container overhead
4. ✅ **No CORS issues** - everything on localhost
5. ✅ **Can use IDE debuggers**
6. ✅ **Can see database in pgAdmin immediately**

---

## 🎉 **You're Ready!**

Now you have:
- ✅ PostgreSQL database running locally
- ✅ Backend API on http://localhost:5000
- ✅ Frontend on http://localhost:5173
- ✅ No Docker, no containers, no CORS headaches!
- ✅ Full test data seeded and ready

**Just run the backend and frontend, then login and test!** 🚀
