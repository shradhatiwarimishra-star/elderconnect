# ElderConnect - Test Data Guide

## 🎯 Quick Setup with Test Data

### **Step 1: Start the Application**
```powershell
docker-compose up -d
```

### **Step 2: Run the Seed Script**

**On Windows:**
```powershell
docker exec -it elderconnect_backend python seed_data.py
```

**On Mac/Linux:**
```bash
./seed_database.sh
```

### **Step 3: Login and Test!**
Open http://localhost:5173

---

## 🔐 Test Accounts Created

### **👴 ELDER ACCOUNTS**

#### **1. John Smith** (Verified, Active User)
- **Email:** `john.smith@email.com`
- **Password:** `Elder123!`
- **Age:** 72
- **Location:** New York, NY
- **Medical:** Diabetes Type 2, uses walker
- **Status:** Fully verified ✅
- **Bookings:** 3 (1 completed, 2 upcoming)

#### **2. Mary Johnson** (Verified, Active User)
- **Email:** `mary.johnson@email.com`
- **Password:** `Elder123!`
- **Age:** 68
- **Location:** Los Angeles, CA
- **Medical:** Arthritis, recent hip surgery
- **Status:** Fully verified ✅
- **Bookings:** 3 (1 completed, 1 pending, 1 cancelled)

#### **3. Robert Williams** (KYC Pending)
- **Email:** `robert.williams@email.com`
- **Password:** `Elder123!`
- **Age:** 75
- **Location:** Chicago, IL
- **Medical:** Early stage dementia
- **Status:** KYC Pending ⏳
- **Bookings:** None (can't book until verified)

---

### **👨‍⚕️ CAREGIVER ACCOUNTS**

#### **1. Sarah Davis** (Top Rated CNA)
- **Email:** `sarah.davis@email.com`
- **Password:** `Caregiver123!`
- **Experience:** 8 years
- **Rate:** $35/hour
- **Location:** New York, NY
- **Services:** In-home care, Hospital visits, Medical assistance
- **Rating:** 4.8 ⭐ (42 bookings)
- **Certifications:** CNA, CPR, First Aid
- **Current Bookings:** 1 completed, 1 cancelled

#### **2. Michael Brown** (EMT Background)
- **Email:** `michael.brown@email.com`
- **Password:** `Caregiver123!`
- **Experience:** 5 years
- **Rate:** $40/hour
- **Location:** New York, NY
- **Services:** In-home care, Hospital visits, Social outings, Medical
- **Rating:** 4.9 ⭐ (28 bookings)
- **Certifications:** EMT-B, Physical Therapy Aide, CPR
- **Current Bookings:** 1 upcoming (hospital visit)

#### **3. Emily Wilson** (Dementia Specialist)
- **Email:** `emily.wilson@email.com`
- **Password:** `Caregiver123!`
- **Experience:** 10 years
- **Rate:** $38/hour
- **Location:** Los Angeles, CA
- **Services:** In-home care, Social outings, Bank visits
- **Rating:** 4.7 ⭐ (65 bookings)
- **Certifications:** Dementia Care Specialist, CNA, CPR
- **Current Bookings:** 1 pending

#### **4. David Martinez** (New Caregiver - KYC Pending)
- **Email:** `david.martinez@email.com`
- **Password:** `Caregiver123!`
- **Experience:** 1 year
- **Rate:** $25/hour
- **Location:** Chicago, IL
- **Services:** In-home care, Social outings
- **Rating:** N/A (0 bookings)
- **Certifications:** CNA (In Progress)
- **Status:** KYC Pending ⏳

#### **5. Lisa Anderson** (Premium RN)
- **Email:** `lisa.anderson@email.com`
- **Password:** `Caregiver123!`
- **Experience:** 15 years
- **Rate:** $55/hour
- **Location:** New York, NY
- **Services:** In-home care, Hospital visits, Medical assistance
- **Rating:** 4.95 ⭐ (103 bookings)
- **Certifications:** RN, Geriatric Nursing, CPR, ACLS
- **Current Bookings:** 1 completed, 1 upcoming (tomorrow)

---

## 📅 Sample Bookings Created

### **Booking #1 - COMPLETED** ✅
- **Elder:** John Smith
- **Caregiver:** Sarah Davis
- **Service:** In-home care
- **Date:** 7 days ago
- **Duration:** 4 hours
- **Cost:** $140.00
- **Status:** Completed with 5-star review
- **Payment:** Completed

### **Booking #2 - CONFIRMED** (Upcoming)
- **Elder:** John Smith
- **Caregiver:** Michael Brown
- **Service:** Hospital visit
- **Date:** 3 days from now
- **Duration:** 4 hours
- **Cost:** $160.00
- **Status:** Confirmed
- **Payment:** Completed

### **Booking #3 - PENDING** (Awaiting Caregiver)
- **Elder:** Mary Johnson
- **Caregiver:** Emily Wilson
- **Service:** Social outing (museum)
- **Date:** 5 days from now
- **Duration:** 3 hours
- **Cost:** $114.00
- **Status:** Pending caregiver acceptance
- **Payment:** Pending

### **Booking #4 - COMPLETED** ✅
- **Elder:** Mary Johnson
- **Caregiver:** Lisa Anderson (RN)
- **Service:** Medical assistance (wound care)
- **Date:** 14 days ago
- **Duration:** 4 hours
- **Cost:** $220.00
- **Status:** Completed with 5-star review
- **Payment:** Completed

### **Booking #5 - CONFIRMED** (Tomorrow!)
- **Elder:** John Smith
- **Caregiver:** Lisa Anderson (RN)
- **Service:** In-home care (insulin injection)
- **Date:** Tomorrow
- **Duration:** 4 hours
- **Cost:** $220.00
- **Status:** Confirmed
- **Payment:** Completed

### **Booking #6 - CANCELLED** ❌
- **Elder:** Mary Johnson
- **Caregiver:** Sarah Davis
- **Service:** In-home care
- **Date:** 3 days ago
- **Status:** Cancelled (Elder not feeling well)
- **Payment:** Refunded ($105.00)

---

## 🧪 Test Scenarios You Can Try

### **As Elder (John Smith):**

1. **View Your Dashboard**
   - Login with: `john.smith@email.com` / `Elder123!`
   - See 3 bookings, stats, and quick actions

2. **Browse Caregivers**
   - Click "Find Caregivers"
   - Filter by service type, location, rating
   - See 4 verified caregivers (David is pending KYC)

3. **View Booking History**
   - Go to "My Bookings"
   - See completed, upcoming, and all bookings
   - Filter by status

4. **Book a New Service**
   - Click on any caregiver
   - Fill out booking form
   - Process payment (demo mode)

5. **View Booking Details**
   - Click on any booking
   - See full details
   - Options to cancel (if applicable)

### **As Caregiver (Sarah Davis):**

1. **View Dashboard**
   - Login with: `sarah.davis@email.com` / `Caregiver123!`
   - See earnings: $140 from 1 completed booking
   - View statistics and recent bookings

2. **Manage Profile**
   - Go to "My Profile"
   - Update bio, rate, services offered
   - Toggle availability on/off

3. **View Bookings**
   - See completed and cancelled bookings
   - View payment history

4. **Accept Bookings** (Try with Emily Wilson)
   - Login as: `emily.wilson@email.com` / `Caregiver123!`
   - See 1 pending booking from Mary Johnson
   - Accept the booking

### **As Premium Caregiver (Lisa Anderson):**

1. **High Earnings Dashboard**
   - Login with: `lisa.anderson@email.com` / `Caregiver123!`
   - See $440 total earnings from 2 bookings
   - 4.95 star rating
   - 103 total bookings (lifetime)

2. **Upcoming Booking Tomorrow**
   - View booking with John Smith
   - See details for insulin injection service

3. **Complete Booking**
   - After "tomorrow" passes, mark as completed
   - Add caregiver notes

---

## 📊 Database Stats After Seeding

- **Total Users:** 8
  - Elders: 3 (2 verified, 1 pending)
  - Caregivers: 5 (4 verified, 1 pending)

- **Total Bookings:** 6
  - Completed: 2
  - Confirmed: 2
  - Pending: 1
  - Cancelled: 1

- **Total Payments:** 6
  - Completed: 4
  - Pending: 1
  - Refunded: 1

- **Total Reviews:** 4
  - Average rating: 4.75 stars

- **Total Revenue:** $959.00 (excluding refunds)

---

## 🔄 Testing Complete Flows

### **Flow 1: Elder Books a Caregiver**

1. Login as John Smith
2. Browse caregivers
3. Click on Emily Wilson
4. Book social outing service
5. Select date/time
6. Process payment
7. View confirmation

### **Flow 2: Caregiver Accepts and Completes Booking**

1. Login as Emily Wilson
2. See pending booking from Mary Johnson
3. Click "Accept Booking"
4. View in upcoming bookings
5. After service, click "Mark as Completed"
6. Add service notes

### **Flow 3: Elder Reviews Caregiver**

1. Login as John Smith
2. Go to completed booking
3. Click "Write Review"
4. Rate 5 stars
5. Add comment
6. Submit review
7. Review appears on caregiver's profile

### **Flow 4: Payment and Refund**

1. Login as Mary Johnson
2. View cancelled booking
3. See refund status: Completed ($105.00)
4. Check payment history

---

## 🗺️ Data Relationships Visualized

```
John Smith (Elder)
├── Booking #1 → Sarah Davis (Completed) → Payment (Completed) → Review (5★)
├── Booking #2 → Michael Brown (Upcoming) → Payment (Completed)
└── Booking #5 → Lisa Anderson (Tomorrow) → Payment (Completed)

Mary Johnson (Elder)
├── Booking #3 → Emily Wilson (Pending) → Payment (Pending)
├── Booking #4 → Lisa Anderson (Completed) → Payment (Completed) → Review (5★)
└── Booking #6 → Sarah Davis (Cancelled) → Payment (Refunded)

Sarah Davis (Caregiver)
├── 42 lifetime bookings, 4.8★ rating
├── Received review from John Smith (5★)
└── Available for new bookings

Emily Wilson (Caregiver)
├── 65 lifetime bookings, 4.7★ rating
├── Has 1 pending booking awaiting acceptance
└── Available for new bookings
```

---

## 🎨 Caregiver Diversity

The test data includes various caregiver types:

- **Entry Level:** David Martinez ($25/hr, 1 year)
- **Mid Level:** Sarah Davis ($35/hr, 8 years)
- **Experienced:** Emily Wilson ($38/hr, 10 years), Michael Brown ($40/hr, 5 years)
- **Premium/RN:** Lisa Anderson ($55/hr, 15 years)

---

## 📍 Geographic Distribution

- **New York, NY:** 3 caregivers (Sarah, Michael, Lisa) + 1 elder (John)
- **Los Angeles, CA:** 1 caregiver (Emily) + 1 elder (Mary)
- **Chicago, IL:** 1 caregiver (David) + 1 elder (Robert)

---

## 💡 Advanced Testing Scenarios

### **Test Filters:**
- Search for caregivers in "New York"
- Filter by "hospital_visits" service
- Filter by minimum rating 4.8
- Filter by max rate $40/hour
- Sort by rating vs. rate

### **Test Booking Status Workflow:**
1. Create booking (status: pending)
2. Caregiver accepts (status: confirmed)
3. Payment processed (payment: completed)
4. Service date arrives
5. Caregiver completes (status: completed)
6. Elder leaves review

### **Test Different Service Types:**
- In-home care (daily assistance)
- Hospital visits (medical appointments)
- Social outings (museum, movies)
- Bank visits (financial errands)
- Medical assistance (wound care, injections)

---

## 🔧 Reseed Database

If you want to reset and reseed:

```powershell
# Clear and reseed
docker exec -it elderconnect_backend python seed_data.py
```

The script automatically clears existing data before creating new test data.

---

## 📊 View Data in pgAdmin

After seeding, you can run these queries in pgAdmin:

### **View All Users:**
```sql
SELECT id, name, email, role, kyc_status 
FROM users 
ORDER BY role, name;
```

### **View Caregivers with Ratings:**
```sql
SELECT 
    u.name,
    cp.rate_per_hour,
    cp.average_rating,
    cp.total_bookings,
    cp.city || ', ' || cp.state as location
FROM users u
JOIN caregiver_profiles cp ON u.id = cp.user_id
WHERE u.kyc_status = 'verified'
ORDER BY cp.average_rating DESC;
```

### **View All Bookings with Details:**
```sql
SELECT 
    b.id,
    e.name as elder,
    c.name as caregiver,
    b.service_type,
    b.service_date,
    b.status,
    b.total_cost,
    p.status as payment_status
FROM bookings b
JOIN users e ON b.elder_id = e.id
JOIN users c ON b.caregiver_id = c.id
LEFT JOIN payments p ON p.booking_id = b.id
ORDER BY b.service_date DESC;
```

### **View Reviews with Ratings:**
```sql
SELECT 
    u.name as caregiver,
    r.rating,
    r.comment,
    r.created_at
FROM reviews r
JOIN users u ON r.caregiver_id = u.id
ORDER BY r.created_at DESC;
```

---

## 🎯 Feature Testing Checklist

Use this checklist to test all features:

### **Authentication:**
- [ ] Register new elder account
- [ ] Register new caregiver account
- [ ] Login as elder
- [ ] Login as caregiver
- [ ] Logout
- [ ] Token refresh (browse for 30+ minutes)

### **Elder Features:**
- [ ] View dashboard with stats
- [ ] Browse caregivers
- [ ] Filter caregivers by service type
- [ ] Filter by location
- [ ] Filter by rating
- [ ] Filter by max rate
- [ ] View caregiver profile
- [ ] Read reviews
- [ ] Create new booking
- [ ] Process payment
- [ ] View booking history
- [ ] View booking details
- [ ] Cancel upcoming booking
- [ ] Update profile
- [ ] Upload KYC document

### **Caregiver Features:**
- [ ] View dashboard stats
- [ ] See total earnings
- [ ] View upcoming bookings
- [ ] Accept pending booking
- [ ] Complete booking
- [ ] Add service notes
- [ ] Update profile (bio, rate)
- [ ] Change services offered
- [ ] Toggle availability
- [ ] View payment history
- [ ] Upload KYC document

### **Payment Features:**
- [ ] Create payment for booking
- [ ] Process card payment
- [ ] View payment history
- [ ] View refunded payment
- [ ] Check transaction IDs

### **Review Features:**
- [ ] View reviews on caregiver profile
- [ ] See average rating
- [ ] See detailed ratings (professionalism, etc.)
- [ ] Verified booking badge

---

## 📝 Sample Test Cases

### **Test Case 1: Complete Booking Flow**

**Scenario:** Elder books a caregiver for in-home care

**Steps:**
1. Login as `mary.johnson@email.com`
2. Click "Find Caregivers"
3. Select "Sarah Davis"
4. Click "Book Now"
5. Fill in details:
   - Service: In-home care
   - Date: Tomorrow
   - Time: 09:00
   - Duration: 4 hours
   - Address: Use profile address
6. Click "Proceed to Payment"
7. Enter card details (demo)
8. Click "Pay"
9. See confirmation

**Expected Result:**
- ✅ Booking created with status "pending"
- ✅ Payment completed
- ✅ Visible in elder's bookings
- ✅ Visible in caregiver's pending bookings

### **Test Case 2: Caregiver Accepts Booking**

**Scenario:** Caregiver accepts a pending booking

**Steps:**
1. Login as `emily.wilson@email.com`
2. Go to Dashboard
3. See pending booking from Mary Johnson
4. Click on the booking
5. Click "Accept Booking"

**Expected Result:**
- ✅ Booking status changes to "confirmed"
- ✅ Visible in caregiver's upcoming bookings
- ✅ Elder receives confirmation

### **Test Case 3: Browse and Filter Caregivers**

**Scenario:** Elder searches for caregivers

**Steps:**
1. Login as `john.smith@email.com`
2. Click "Find Caregivers"
3. Filter by:
   - Service: Hospital visits
   - City: New York
   - Min Rating: 4.5
4. Sort by: Rating

**Expected Result:**
- ✅ Shows 3 caregivers (Sarah, Michael, Lisa)
- ✅ All in New York
- ✅ All offer hospital visits
- ✅ Sorted by rating (Lisa 4.95, Michael 4.9, Sarah 4.8)

---

## 🎉 Demo Presentation Script

### **5-Minute Demo Flow:**

1. **Show Elder Dashboard** (John Smith)
   - "3 bookings, upcoming and completed"
   - "Quick access to find caregivers"

2. **Browse Caregivers**
   - "5 verified caregivers available"
   - "Filter by New York, in-home care"
   - "See ratings and reviews"

3. **View Caregiver Profile** (Lisa Anderson)
   - "Premium RN with 4.95 stars"
   - "103 bookings completed"
   - "Read 5-star reviews"

4. **Show Booking Details**
   - "Upcoming hospital visit in 3 days"
   - "Payment already processed"
   - "All details clearly displayed"

5. **Switch to Caregiver Dashboard** (Emily Wilson)
   - "1 pending booking awaiting acceptance"
   - "$2,470 total lifetime earnings"
   - "65 completed bookings"

6. **Accept Booking**
   - "Accept Mary's museum visit request"
   - "Booking confirmed instantly"

---

## 🔄 Reset Test Data

To start fresh with clean test data:

```powershell
# Method 1: Reseed (keeps database structure)
docker exec -it elderconnect_backend python seed_data.py

# Method 2: Complete reset
docker-compose down -v
docker-compose up -d
docker exec -it elderconnect_backend python init_db.py
docker exec -it elderconnect_backend python seed_data.py
```

---

## 📞 Quick Reference

**All passwords:** `Elder123!` or `Caregiver123!`

**Quick logins:**
- Elder: `john.smith@email.com` / `Elder123!`
- Caregiver: `sarah.davis@email.com` / `Caregiver123!`

**Database access:**
```powershell
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db
```

**View all users:**
```sql
SELECT name, email, role, kyc_status FROM users;
```

---

## 🎯 Now You're Ready!

Your database is populated with:
- ✅ 8 realistic users (3 elders, 5 caregivers)
- ✅ Complete profiles with medical info and certifications
- ✅ 6 bookings covering all statuses
- ✅ 6 payments including refunds
- ✅ 4 reviews with detailed ratings
- ✅ Various scenarios to test

**Open http://localhost:5173 and start testing!** 🚀
