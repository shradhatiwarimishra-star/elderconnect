# 🔧 Troubleshooting: No Tables in Database

## Problem
After running `docker-compose down -v`, the database has no tables and you're getting 422 errors when browsing caregivers.

---

## ✅ **Solution: Use the Automated Fix Script**

### **Option 1: Complete Automated Fix (EASIEST)**

In PowerShell, run:

```powershell
.\fix_database.bat
```

This will:
1. ✅ Stop and remove all containers
2. ✅ Delete old volumes
3. ✅ Start fresh containers
4. ✅ Create all database tables
5. ✅ Seed test data
6. ✅ Verify everything works

**Total time:** ~60 seconds

---

### **Option 2: Manual Step-by-Step Fix**

If the script doesn't work, follow these manual steps:

#### **Step 1: Stop Everything**
```powershell
docker compose down -v
```

#### **Step 2: Start Containers**
```powershell
docker compose up -d
```

#### **Step 3: Wait for Backend to be Ready (30 seconds)**
```powershell
Start-Sleep -Seconds 30
```

Or just wait and watch:
```powershell
docker logs elderconnect_backend -f
```
Wait until you see: `Running on http://0.0.0.0:5000`

#### **Step 4: Create Database Tables**
```powershell
docker exec -it elderconnect_backend python init_db.py
```

**Expected output:**
```
============================================================
ElderConnect Database Initialization
============================================================

🗑️  Dropping existing tables (if any)...
📦 Creating database tables...
✓ Database tables created successfully!

📋 Available tables:
  ✓ users
  ✓ elder_profiles
  ✓ caregiver_profiles
  ✓ bookings
  ✓ reviews
  ✓ payments

✅ Total: 6 tables created
```

#### **Step 5: Seed Test Data**
```powershell
docker exec -it elderconnect_backend python seed_data.py
```

**Expected output:**
```
============================================================
ElderConnect Database Seeding
============================================================

👴 Creating Elder users...
✓ Created 3 elder users

👨‍⚕️ Creating Caregiver users...
✓ Created 5 caregiver users

📅 Creating Bookings...
✓ Created 6 bookings

💳 Creating Payments...
✓ Created 6 payments

⭐ Creating Reviews...
✓ Created 4 reviews

✅ DATABASE SEEDING COMPLETE!
```

#### **Step 6: Verify Tables in pgAdmin**

1. **Open pgAdmin**
2. **Right-click** on `elderconnect_db` → **Refresh**
3. **Expand:** Databases → elderconnect_db → Schemas → public → Tables
4. **You should see 6 tables:**
   - bookings
   - caregiver_profiles
   - elder_profiles
   - payments
   - reviews
   - users

#### **Step 7: Verify Data via Command Line**

```powershell
# Check if tables exist
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "\dt"

# Count users by role
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT role, COUNT(*) FROM users GROUP BY role;"
```

**Expected output:**
```
 role      | count
-----------+-------
 caregiver |     5
 elder     |     3
```

#### **Step 8: Test the Application**

1. **Open:** http://localhost:5173
2. **Login as Elder:**
   - Email: `john.smith@email.com`
   - Password: `Elder123!`
3. **Click:** "Find Caregivers"
4. **You should see:** 4 verified caregivers

---

## 🔍 **Diagnostic Commands**

### **Check if containers are running:**
```powershell
docker ps
```

You should see 3 containers:
- elderconnect_db
- elderconnect_backend
- elderconnect_frontend

### **Check backend logs:**
```powershell
docker logs elderconnect_backend --tail 50
```

Look for:
- ✅ "Creating database tables..."
- ✅ "6 tables created"
- ✅ "Running on http://0.0.0.0:5000"

### **Check if database is accessible:**
```powershell
docker exec elderconnect_db pg_isready -U elderconnect_user
```

Should output: `accepting connections`

### **Connect to database directly:**
```powershell
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db
```

Then run:
```sql
-- List all tables
\dt

-- Count users
SELECT COUNT(*) FROM users;

-- View all users
SELECT id, name, email, role, kyc_status FROM users;

-- Exit
\q
```

---

## ❌ **Common Issues and Fixes**

### **Issue 1: "No such container: elderconnect_backend"**

**Fix:**
```powershell
docker compose up -d
# Wait 30 seconds, then try again
```

---

### **Issue 2: "relation 'users' does not exist"**

**Cause:** Tables weren't created

**Fix:**
```powershell
docker exec -it elderconnect_backend python init_db.py
```

---

### **Issue 3: Tables created but still 422 error**

**Cause:** Tables exist but are empty (no caregivers)

**Fix:**
```powershell
docker exec -it elderconnect_backend python seed_data.py
```

---

### **Issue 4: "Could not connect to server" in pgAdmin**

**Cause:** Wrong connection settings

**Fix:** In pgAdmin, use these connection details:
- **Host:** `localhost` (NOT `db`)
- **Port:** `5432`
- **Database:** `elderconnect_db`
- **Username:** `elderconnect_user`
- **Password:** `elderconnect_pass`

---

### **Issue 5: init_db.py says "0 tables created"**

**Cause:** Models not imported properly

**Fix:** The updated `init_db.py` should now import all models. If still not working:

```powershell
# Rebuild backend container
docker compose up -d --build backend

# Then try creating tables again
docker exec -it elderconnect_backend python init_db.py
```

---

### **Issue 6: Backend won't start**

**Fix:**
```powershell
# Check backend logs
docker logs elderconnect_backend

# Common causes:
# - Port 5000 already in use
# - Database not ready yet
# - Syntax error in code

# Solution: Restart
docker compose restart backend
```

---

## 🎯 **Quick Health Check**

Run this to check everything at once:

```powershell
# Run the troubleshoot script
.\troubleshoot.bat
```

Or manually:

```powershell
# 1. Check containers
docker ps

# 2. Check backend health
curl http://localhost:5000/api/health

# 3. Check tables
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "\dt"

# 4. Check data
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT COUNT(*) FROM users;"
```

---

## 🚀 **Expected Final State**

After completing all steps, you should have:

✅ **3 running containers:**
- elderconnect_db (PostgreSQL)
- elderconnect_backend (Flask)
- elderconnect_frontend (React)

✅ **6 database tables:**
- users
- elder_profiles
- caregiver_profiles
- bookings
- reviews
- payments

✅ **8 test users:**
- 3 elders
- 5 caregivers

✅ **6 bookings** (various statuses)

✅ **4 reviews**

✅ **6 payments**

✅ **Frontend accessible at:** http://localhost:5173

✅ **Backend API at:** http://localhost:5000

✅ **Can browse caregivers without 422 error**

---

## 📞 **Still Having Issues?**

### **Nuclear Option: Complete Reset**

If nothing else works, do a complete clean restart:

```powershell
# 1. Stop everything
docker compose down -v

# 2. Remove any leftover containers
docker container prune -f

# 3. Remove any leftover volumes
docker volume prune -f

# 4. Rebuild from scratch
docker compose up -d --build

# 5. Wait 30 seconds
Start-Sleep -Seconds 30

# 6. Create tables
docker exec -it elderconnect_backend python init_db.py

# 7. Seed data
docker exec -it elderconnect_backend python seed_data.py

# 8. Test
curl http://localhost:5000/api/health
```

---

## 📋 **Checklist**

Use this checklist to verify everything:

- [ ] Docker Desktop is running
- [ ] 3 containers are running (`docker ps`)
- [ ] Backend logs show "Running on http://0.0.0.0:5000"
- [ ] Database is accessible (`docker exec elderconnect_db pg_isready`)
- [ ] 6 tables exist in database (`\dt` in psql)
- [ ] Users table has 8 rows (`SELECT COUNT(*) FROM users;`)
- [ ] pgAdmin shows all 6 tables
- [ ] http://localhost:5173 loads
- [ ] Can login as john.smith@email.com / Elder123!
- [ ] "Find Caregivers" shows 4 caregivers
- [ ] No 422 errors in browser console

---

## 🎉 **Success!**

Once all checks pass:

1. **Open:** http://localhost:5173
2. **Login:** john.smith@email.com / Elder123!
3. **Click:** "Find Caregivers"
4. **See:** 4 caregivers with ratings and prices
5. **Enjoy testing!** 🚀

---

**Need more help?** Check the backend logs with:
```powershell
docker logs elderconnect_backend -f
```
