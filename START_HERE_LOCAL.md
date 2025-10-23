# 🎯 START HERE - Local Setup (No Docker!)

This is the EASIEST way to get ElderConnect running!

---

## 📥 **Step 1: Install Prerequisites** (10 minutes)

### **1.1 - Install Python**
- Download: https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation!
- Verify: Open PowerShell and run `python --version`

### **1.2 - Install Node.js**
- Download: https://nodejs.org/ (LTS version)
- Verify: Open PowerShell and run `node --version`

### **1.3 - Install PostgreSQL**
- Download: https://www.postgresql.org/download/windows/
- During installation:
  - Set password for `postgres` user (REMEMBER THIS!)
  - Port: 5432 (default - keep it)
  - Install pgAdmin (comes with PostgreSQL)

---

## 🗄️ **Step 2: Create Database** (2 minutes)

### **Option A: Using pgAdmin (Easier)**

1. Open **pgAdmin** (should be installed with PostgreSQL)
2. Enter your postgres password
3. Right-click "Databases" → "Create" → "Database"
4. Name: `elderconnect_db`
5. Click "Save"

### **Option B: Using Command Line**

```powershell
psql -U postgres
# Enter your password

CREATE DATABASE elderconnect_db;
\q
```

---

## 🔧 **Step 3: Setup Backend** (5 minutes)

### **3.1 - Run Setup Script**

In PowerShell (in the project folder):

```powershell
.\setup_backend_local.bat
```

### **3.2 - Create .env File**

1. Copy `backend/.env.example.local` to `backend/.env`
2. Open `backend/.env` in a text editor
3. Replace `YOUR_POSTGRES_PASSWORD` with your actual postgres password

Example:
```env
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/elderconnect_db
```

### **3.3 - Initialize Database**

```powershell
cd backend
.\venv\Scripts\activate
python init_db.py
python seed_data.py
```

You should see "6 tables created" and "DATABASE SEEDING COMPLETE!"

---

## 🎨 **Step 4: Setup Frontend** (3 minutes)

In a NEW PowerShell window:

```powershell
cd frontend
npm install
```

Create `frontend/.env.local` with:
```env
VITE_API_URL=http://localhost:5000
```

---

## 🚀 **Step 5: Start the Application**

### **Terminal 1 - Backend:**

```powershell
.\start_backend_local.bat
```

Wait until you see: `Running on http://127.0.0.1:5000`

### **Terminal 2 - Frontend:**

```powershell
.\start_frontend_local.bat
```

Wait until you see: `Local: http://localhost:5173/`

---

## 🎉 **Step 6: Test It!**

1. **Open browser:** http://localhost:5173
2. **Login:**
   - Email: `john.smith@email.com`
   - Password: `Elder123!`
3. **Click:** "Find Caregivers"
4. **Success!** You should see 4 caregivers - NO ERRORS!

---

## ✅ **Checklist**

- [ ] Python installed and in PATH
- [ ] Node.js installed
- [ ] PostgreSQL installed and running
- [ ] Database `elderconnect_db` created
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Backend `.env` file created with correct password
- [ ] Database tables created (init_db.py)
- [ ] Test data seeded (seed_data.py)
- [ ] Frontend dependencies installed (npm install)
- [ ] Frontend `.env.local` file created
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:5173
- [ ] Can login and browse caregivers

---

## 🆘 **Having Issues?**

### **"python: command not found"**
- Python not installed or not in PATH
- Reinstall Python with "Add to PATH" checked

### **"pip install failed"**
- Run PowerShell as Administrator
- Try: `python -m pip install --upgrade pip` first

### **"password authentication failed for user postgres"**
- Wrong password in `backend/.env`
- Check your postgres password in pgAdmin

### **"Port 5000 already in use"**
```powershell
# Stop Docker if running
docker compose down

# Or find and kill the process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### **"Module not found" errors**
- Make sure virtual environment is activated: `.\venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

### **Tables not showing in pgAdmin**
- Right-click `elderconnect_db` → Refresh
- Expand: Databases → elderconnect_db → Schemas → public → Tables

---

## 🎯 **Quick Commands**

### **Start Backend:**
```powershell
cd backend
.\venv\Scripts\activate
python run.py
```

### **Start Frontend:**
```powershell
cd frontend
npm run dev
```

### **Reset Database:**
```powershell
cd backend
.\venv\Scripts\activate
python init_db.py
python seed_data.py
```

### **View Database:**
- Open pgAdmin
- Connect to elderconnect_db
- Browse tables

---

## 💡 **Why Local Setup is Better**

✅ **No Docker complexity**
✅ **No CORS issues**
✅ **Faster startup**
✅ **Easier debugging**
✅ **Can use IDE debuggers**
✅ **See changes instantly**
✅ **Direct database access via pgAdmin**

---

## 🎓 **Test Accounts**

### **Elders:**
- `john.smith@email.com` / `Elder123!`
- `mary.johnson@email.com` / `Elder123!`

### **Caregivers:**
- `sarah.davis@email.com` / `Caregiver123!`
- `emily.wilson@email.com` / `Caregiver123!`
- `lisa.anderson@email.com` / `Caregiver123!`

---

**Follow the steps above and you'll have a working ElderConnect app in 20 minutes!** 🚀

No Docker, no containers, no headaches - just pure development! 😊
