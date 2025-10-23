# 🚀 ElderConnect - Complete Setup with Test Data

## ⚡ Quick Start (3 Commands)

### **Step 1: Start Docker**
```powershell
docker-compose up -d
```

### **Step 2: Create Tables**
```powershell
docker exec -it elderconnect_backend python init_db.py
```

### **Step 3: Add Test Data**
```powershell
docker exec -it elderconnect_backend python seed_data.py
```

---

## 🎉 You're Done!

Open **http://localhost:5173** and login with:

### **Elder Account:**
```
Email: john.smith@email.com
Password: Elder123!
```

### **Caregiver Account:**
```
Email: sarah.davis@email.com
Password: Caregiver123!
```

---

## 📊 What Test Data Was Created?

### **8 Users:**
- 3 Elders (John Smith, Mary Johnson, Robert Williams)
- 5 Caregivers (Sarah, Michael, Emily, David, Lisa)

### **6 Bookings:**
- 2 Completed (with reviews)
- 2 Confirmed/Upcoming
- 1 Pending
- 1 Cancelled

### **4 Reviews:**
- All 4-5 stars
- Detailed comments
- Verified bookings

### **6 Payments:**
- 4 Completed
- 1 Pending
- 1 Refunded

---

## 🔍 View in pgAdmin

After seeding, refresh pgAdmin and run:

```sql
-- View all users
SELECT name, email, role, kyc_status FROM users;

-- View all bookings with details
SELECT 
    b.id,
    (SELECT name FROM users WHERE id = b.elder_id) as elder,
    (SELECT name FROM users WHERE id = b.caregiver_id) as caregiver,
    b.service_type,
    b.service_date,
    b.status,
    b.total_cost
FROM bookings b
ORDER BY b.service_date DESC;

-- View caregiver ratings
SELECT 
    u.name,
    cp.rate_per_hour,
    cp.average_rating,
    cp.total_bookings
FROM users u
JOIN caregiver_profiles cp ON u.id = cp.user_id
ORDER BY cp.average_rating DESC;
```

---

## 🧪 Test Different User Journeys

### **Journey 1: New Elder Experience**
1. Login as: `john.smith@email.com` / `Elder123!`
2. See dashboard with 3 bookings
3. Browse 4 verified caregivers
4. View completed booking with 5-star review
5. See upcoming hospital visit

### **Journey 2: Busy Caregiver**
1. Login as: `lisa.anderson@email.com` / `Caregiver123!`
2. See $440 in earnings
4. View 4.95 star rating
5. See tomorrow's booking
6. Manage profile and availability

### **Journey 3: Accept Pending Booking**
1. Login as: `emily.wilson@email.com` / `Caregiver123!`
2. See 1 pending booking
3. Click to view details
4. Accept the booking
5. See it move to upcoming

---

## 🔄 Reset and Reseed

Want to start fresh?

```powershell
# Just reseed (keeps tables)
docker exec -it elderconnect_backend python seed_data.py

# Complete reset
docker-compose down -v
docker-compose up -d
docker exec -it elderconnect_backend python init_db.py
docker exec -it elderconnect_backend python seed_data.py
```

---

## 📋 All Test Credentials

### **Elders (Password: Elder123!)**
| Name | Email | Location | KYC Status |
|------|-------|----------|------------|
| John Smith | john.smith@email.com | New York, NY | ✅ Verified |
| Mary Johnson | mary.johnson@email.com | Los Angeles, CA | ✅ Verified |
| Robert Williams | robert.williams@email.com | Chicago, IL | ⏳ Pending |

### **Caregivers (Password: Caregiver123!)**
| Name | Email | Rate | Rating | Location |
|------|-------|------|--------|----------|
| Sarah Davis | sarah.davis@email.com | $35/hr | 4.8⭐ | New York, NY |
| Michael Brown | michael.brown@email.com | $40/hr | 4.9⭐ | New York, NY |
| Emily Wilson | emily.wilson@email.com | $38/hr | 4.7⭐ | Los Angeles, CA |
| David Martinez | david.martinez@email.com | $25/hr | N/A | Chicago, IL |
| Lisa Anderson | lisa.anderson@email.com | $55/hr | 4.95⭐ | New York, NY |

---

## 🎯 Ready to Demo!

Your ElderConnect application now has:
- ✅ Realistic user data
- ✅ Complete booking workflows
- ✅ Payment transactions
- ✅ Review system populated
- ✅ Various scenarios to explore

**Start testing at:** http://localhost:5173

Enjoy exploring ElderConnect! 🎉
