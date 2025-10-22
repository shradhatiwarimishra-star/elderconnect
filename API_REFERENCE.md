# ElderConnect API Reference

Base URL: `http://localhost:5000/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Response Formats

### Success Response
```json
{
  "data": {},
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": "Error message"
}
```

---

## 🔐 Authentication Endpoints

### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe",
  "phone": "5551234567",
  "role": "elder"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "elder",
    "kyc_status": "pending"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### POST /auth/login
Login and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {...},
  "profile": {...},
  "access_token": "...",
  "refresh_token": "..."
}
```

### GET /auth/me
Get current user information. Requires authentication.

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "elder",
    "kyc_status": "verified"
  },
  "profile": {...}
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200):**
```json
{
  "access_token": "new_access_token"
}
```

### POST /auth/upload-kyc
Upload KYC verification document.

**Request (multipart/form-data):**
```
document: <file>
```

**Response (200):**
```json
{
  "message": "KYC document uploaded successfully",
  "kyc_status": "pending"
}
```

---

## 👴 Elder Endpoints

### GET /elder/profile
Get elder profile.

**Response (200):**
```json
{
  "user": {...},
  "profile": {
    "id": 1,
    "user_id": 1,
    "age": 75,
    "gender": "male",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "medical_notes": "..."
  }
}
```

### PUT /elder/profile
Update elder profile.

**Request Body:**
```json
{
  "age": 75,
  "gender": "male",
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "medical_notes": "Has diabetes",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "5559876543"
}
```

### GET /elder/caregivers
Browse available caregivers.

**Query Parameters:**
- `service` - Filter by service type (e.g., "in_home_care")
- `city` - Filter by city
- `min_rating` - Minimum average rating (e.g., 4.0)
- `max_rate` - Maximum hourly rate
- `sort` - Sort by "rating" or "rate"

**Example:**
```
GET /elder/caregivers?service=in_home_care&city=NewYork&min_rating=4&sort=rating
```

**Response (200):**
```json
{
  "caregivers": [
    {
      "user": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com"
      },
      "profile": {
        "bio": "Experienced caregiver...",
        "rate_per_hour": 25.00,
        "average_rating": 4.5,
        "total_bookings": 42,
        "services_offered": ["in_home_care", "hospital_visits"],
        "city": "New York",
        "verified": true
      },
      "recent_reviews": [...]
    }
  ],
  "total": 15
}
```

### GET /elder/caregivers/{caregiver_id}
Get detailed caregiver profile.

**Response (200):**
```json
{
  "user": {...},
  "profile": {...},
  "reviews": [...],
  "total_reviews": 10
}
```

---

## 👨‍⚕️ Caregiver Endpoints

### GET /caregiver/profile
Get caregiver profile.

### PUT /caregiver/profile
Update caregiver profile.

**Request Body:**
```json
{
  "bio": "Experienced caregiver with 5 years...",
  "experience_years": 5,
  "rate_per_hour": 30.00,
  "services_offered": ["in_home_care", "hospital_visits", "social_outings"],
  "address": "456 Oak Ave",
  "city": "Los Angeles",
  "state": "CA",
  "zip_code": "90001",
  "is_available": true,
  "certifications": "CNA, CPR Certified"
}
```

### GET /caregiver/dashboard
Get caregiver dashboard statistics.

**Response (200):**
```json
{
  "statistics": {
    "total_bookings": 50,
    "upcoming_bookings": 3,
    "completed_bookings": 45,
    "total_earnings": 2250.00
  },
  "recent_bookings": [...]
}
```

### GET /caregiver/bookings
Get caregiver's bookings.

**Query Parameters:**
- `status` - Filter by status
- `upcoming` - Boolean for upcoming bookings

### POST /caregiver/bookings/{booking_id}/accept
Accept a booking request.

**Response (200):**
```json
{
  "message": "Booking accepted successfully",
  "booking": {...}
}
```

### POST /caregiver/bookings/{booking_id}/complete
Mark booking as completed.

**Request Body (optional):**
```json
{
  "caregiver_notes": "Service completed successfully. Patient was cooperative."
}
```

### PUT /caregiver/availability
Update availability status.

**Request Body:**
```json
{
  "is_available": true
}
```

---

## 📅 Booking Endpoints

### POST /bookings
Create a new booking.

**Request Body:**
```json
{
  "caregiver_id": 2,
  "service_type": "in_home_care",
  "service_date": "2024-12-20",
  "start_time": "09:00",
  "duration_hours": 4,
  "service_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "elder_notes": "Please bring medical equipment"
}
```

**Response (201):**
```json
{
  "message": "Booking created successfully",
  "booking": {
    "id": 10,
    "elder_id": 1,
    "caregiver_id": 2,
    "service_type": "in_home_care",
    "service_date": "2024-12-20",
    "start_time": "09:00:00",
    "duration_hours": 4.0,
    "status": "pending",
    "hourly_rate": 25.00,
    "total_cost": 100.00
  },
  "payment": {
    "id": 10,
    "booking_id": 10,
    "amount": 100.00,
    "status": "pending"
  }
}
```

### GET /bookings
Get user's bookings.

**Query Parameters:**
- `status` - Filter by status (pending, confirmed, completed, cancelled)
- `upcoming` - Boolean for upcoming bookings

**Response (200):**
```json
{
  "bookings": [...],
  "total": 10
}
```

### GET /bookings/{booking_id}
Get specific booking details.

### POST /bookings/{booking_id}/cancel
Cancel a booking.

**Request Body (optional):**
```json
{
  "reason": "Schedule conflict"
}
```

---

## 💳 Payment Endpoints

### POST /payments/process
Process payment for a booking.

**Request Body:**
```json
{
  "booking_id": 10,
  "payment_method": "card",
  "stripe_token": "tok_xxx"
}
```

**Response (200):**
```json
{
  "message": "Payment processed successfully",
  "payment": {
    "id": 10,
    "booking_id": 10,
    "amount": 100.00,
    "status": "completed",
    "transaction_id": "TXN_ABC123",
    "completed_at": "2024-01-15T10:30:00"
  },
  "booking": {
    "id": 10,
    "status": "confirmed"
  }
}
```

### GET /payments/{payment_id}
Get payment details.

### POST /payments/{payment_id}/refund
Refund a payment.

**Request Body:**
```json
{
  "reason": "Service cancelled",
  "amount": 100.00
}
```

### GET /payments/history
Get payment history for current user.

**Response (200):**
```json
{
  "payments": [
    {
      "id": 10,
      "booking_id": 10,
      "amount": 100.00,
      "status": "completed",
      "transaction_id": "TXN_ABC123",
      "booking": {...}
    }
  ],
  "total": 5
}
```

### POST /payments/create-payment-intent
Create Stripe payment intent.

**Request Body:**
```json
{
  "booking_id": 10
}
```

**Response (200):**
```json
{
  "client_secret": "pi_xxx_secret_yyy",
  "amount": 100.00,
  "currency": "usd"
}
```

---

## 📊 Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

---

## 🔑 Data Enumerations

### User Roles
- `elder`
- `caregiver`

### KYC Status
- `pending`
- `verified`
- `rejected`

### Booking Status
- `pending`
- `confirmed`
- `in_progress`
- `completed`
- `cancelled`

### Payment Status
- `pending`
- `completed`
- `failed`
- `refunded`

### Service Types
- `in_home_care`
- `hospital_visits`
- `bank_visits`
- `social_outings`
- `medical_assistance`

### Payment Methods
- `card`
- `bank_transfer`
- `cash`
- `stripe`

---

## 🧪 Testing with cURL

### Register and Login Flow
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User",
    "role": "elder",
    "phone": "5551234567"
  }'

# Save the access_token from response

# Get current user
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Booking Flow
```bash
# Browse caregivers
curl -X GET "http://localhost:5000/api/elder/caregivers?service=in_home_care" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create booking
curl -X POST http://localhost:5000/api/bookings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "caregiver_id": 2,
    "service_type": "in_home_care",
    "service_date": "2024-12-20",
    "start_time": "09:00",
    "duration_hours": 4,
    "service_address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
  }'

# Process payment
curl -X POST http://localhost:5000/api/payments/process \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 10,
    "payment_method": "card"
  }'
```

---

## 📞 Support

For API questions or issues, contact: api@elderconnect.com
