# 🚀 START HERE - ElderConnect Quick Setup

## ✅ You're just ONE command away from running the app!

### Step 1: Run This Command
```bash
docker-compose up --build
```

### Step 2: Wait for Success Messages
You'll see:
```
✅ Database initialization complete! (6 tables created)
Running on http://0.0.0.0:5000
```

### Step 3: Open Your Browser
**Frontend:** http://localhost:5173

---

## 🎯 What Just Happened?

The system automatically:
1. ✅ Started PostgreSQL database
2. ✅ Created all 6 database tables
3. ✅ Started Flask backend (port 5000)
4. ✅ Started React frontend (port 5173)

**No manual setup needed!**

---

## 🆘 Got an Error?

### Error: "Cannot import name 'pprint' from marshmallow"
**Fixed!** Just rebuild:
```bash
docker-compose down
docker-compose up --build
```

### Error: "Port already in use"
```bash
# Kill the process and retry
docker-compose down
docker-compose up --build
```

### Any Other Error?
```bash
# Complete reset (removes all data)
docker-compose down -v
docker-compose up --build
```

---

## 📱 First Time Using the App?

### Create an Elder Account
1. Open http://localhost:5173
2. Click "create a new account"
3. Choose "Elder" role
4. Fill in details and register

### Create a Caregiver Account
1. Logout from the elder account
2. Click "create a new account"
3. Choose "Caregiver" role
4. Fill in details and register

### Test the Features
- **Elder**: Browse caregivers, book services, make payments
- **Caregiver**: Update profile, accept bookings, track earnings

---

## 📚 More Information

- **Full Guide**: See `README.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **API Docs**: See `API_REFERENCE.md`
- **Database Info**: See `DATABASE_SETUP.md`

---

## ✨ Pro Tips

### View Logs
```bash
docker-compose logs -f
```

### Stop the App
```bash
docker-compose down
```

### Restart After Code Changes
```bash
docker-compose restart
```

### Complete Clean Restart
```bash
docker-compose down -v
docker-compose up --build
```

---

## 🎉 That's It!

Your ElderConnect application is now running at:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5000/api/health

**Happy coding! 🚀**
