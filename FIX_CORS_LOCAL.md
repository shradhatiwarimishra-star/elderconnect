# 🔧 Fix CORS Issue (Local Setup)

You're SO close! Let's fix this CORS issue once and for all.

---

## ⚡ **Quick Fix - Just Restart Backend**

I've simplified the CORS configuration. Just restart your backend:

### **Step 1: Stop Backend**

In the terminal where backend is running:
- Press `Ctrl + C`

### **Step 2: Start Backend Again**

```powershell
python run.py
```

### **Step 3: Test**

1. Refresh browser (F5)
2. Try "Find Caregivers" again

**Should work now!** ✅

---

## 🔍 **If Still Not Working - Debug Steps**

### **Test 1: Check CORS Configuration**

```powershell
cd backend
.\venv\Scripts\activate
python test_cors.py
```

**You should see:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
```

If you DON'T see these headers, there's an issue with Flask-CORS.

---

### **Test 2: Check Backend Logs**

When you click "Find Caregivers", look at the backend terminal.

**You should see:**
```
127.0.0.1 - - [timestamp] "OPTIONS /api/elder/caregivers HTTP/1.1" 200 -
127.0.0.1 - - [timestamp] "GET /api/elder/caregivers HTTP/1.1" 200 -
```

**If you see 401 or 403 instead of 200**, the issue is authentication, not CORS.

---

### **Test 3: Check Browser Console**

Press F12 → Console tab

After clicking "Find Caregivers", what do you see?

**Case A: CORS Error**
```
Access to XMLHttpRequest at 'http://localhost:5000/api/elder/caregivers' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```
→ Backend CORS not configured (restart backend)

**Case B: 401 Error**
```
GET http://localhost:5000/api/elder/caregivers 401 (Unauthorized)
```
→ Token issue (see below)

**Case C: 403 Error**
```
GET http://localhost:5000/api/elder/caregivers 403 (Forbidden)
```
→ Role or KYC issue (see below)

---

## 🔑 **If Getting Logged Out - Token Issue**

### **Check LocalStorage**

1. Press F12
2. Go to: Application tab
3. Left sidebar: Storage → Local Storage → http://localhost:5173
4. Look for: `access_token` and `refresh_token`

**Are both there after login?**
- ✅ YES → Tokens saved correctly
- ❌ NO → Login not saving tokens

### **Fix: Check Login Response**

Add this to see what's happening:

1. Open `frontend/src/contexts/AuthContext.jsx`
2. Find the `login` function
3. Add console.log:

```javascript
const login = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials)
    const { access_token, refresh_token, user } = response.data
    
    console.log('Login response:', response.data)  // ADD THIS
    console.log('Tokens:', { access_token, refresh_token })  // ADD THIS
    
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    setUser(user)
    navigate(user.role === 'elder' ? '/elder/dashboard' : '/caregiver/dashboard')
  } catch (error) {
    console.error('Login failed:', error.response?.data)
    throw error
  }
}
```

Then login again and check console for the output.

---

## 👤 **If 403 Error - Role/KYC Issue**

The user `john.smith@email.com` should be:
- Role: `elder`
- KYC Status: `verified`

### **Verify in Database:**

```powershell
psql -U postgres -d elderconnect_db
```

```sql
SELECT email, role, kyc_status FROM users WHERE email = 'john.smith@email.com';
```

**Should show:**
```
          email           | role  | kyc_status
--------------------------+-------+------------
 john.smith@email.com     | elder | verified
```

**If NOT verified:**
```sql
UPDATE users SET kyc_status = 'verified' WHERE email = 'john.smith@email.com';
\q
```

---

## 🚀 **Alternative: Disable Auth Temporarily**

To test if it's CORS or Auth causing the issue:

### **Test Without Auth**

1. Open `backend/app/routes/elder.py`
2. Find line 77-79:
```python
@bp.route('/caregivers', methods=['GET'])
@jwt_required()
@role_required('elder')
```

3. Comment out decorators temporarily:
```python
@bp.route('/caregivers', methods=['GET'])
# @jwt_required()
# @role_required('elder')
```

4. Restart backend
5. Try "Find Caregivers"

**If it works now:**
→ Issue is authentication, not CORS

**If still fails:**
→ Issue is CORS or network

**IMPORTANT:** Put the decorators back after testing!

---

## 📋 **Complete Debugging Checklist**

Run these and tell me the results:

```powershell
# 1. Check if backend is running
curl http://localhost:5000/api/health

# 2. Test CORS config
cd backend
.\venv\Scripts\activate
python test_cors.py

# 3. Test endpoint directly (will fail with 401, that's ok)
curl http://localhost:5000/api/elder/caregivers

# 4. Check database
psql -U postgres -d elderconnect_db -c "SELECT email, role, kyc_status FROM users WHERE email = 'john.smith@email.com';"

# 5. Count caregivers
psql -U postgres -d elderconnect_db -c "SELECT COUNT(*) FROM caregiver_profiles WHERE verified = true;"
```

Share the output of all 5 commands!

---

## 🎯 **Most Likely Fix**

Based on your description, it's probably one of these:

### **Option 1: Backend Not Restarted**

After I changed the CORS config, you need to:
```powershell
# Stop backend (Ctrl+C)
# Start again
python run.py
```

### **Option 2: Token Not Being Sent**

Check browser console and look at the request headers:

1. F12 → Network tab
2. Click "Find Caregivers"
3. Click on the `caregivers` request
4. Look at "Request Headers"

**Should have:**
```
Authorization: Bearer eyJ...
```

**If missing Authorization header:**
→ Token not being sent, check `api.js` interceptor

---

## 💡 **Quick Test - Use Postman/Thunder Client**

1. Login via browser first
2. Open DevTools → Application → Local Storage
3. Copy the `access_token` value
4. In Postman:
   - GET `http://localhost:5000/api/elder/caregivers`
   - Add Header: `Authorization: Bearer YOUR_TOKEN`
   - Send

**If this works:**
→ Backend is fine, issue is in frontend

**If this fails:**
→ Backend issue

---

**Try restarting the backend first, then tell me what you see in the browser console!** 🚀
