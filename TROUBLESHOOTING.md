# ElderConnect - Troubleshooting Guide

## 🔧 Database Issues

### Error: "No such command 'db'"

This error occurs because Flask-Migrate needs initialization. We use a simpler approach with `init_db.py`.

**Solution:**
The `docker-compose.yml` is already configured to run `python init_db.py` automatically.

If you're running manually:
```bash
cd backend
python init_db.py
python run.py
```

### Error: "Database connection refused"

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes (this clears the database)
docker-compose down -v

# Restart
docker-compose up --build
```

### Error: "relation does not exist"

This means tables haven't been created yet.

**Solution:**
```bash
# Access the backend container
docker exec -it elderconnect_backend bash

# Inside container, run:
python init_db.py

# Exit and restart
exit
docker-compose restart backend
```

---

## 🐳 Docker Issues

### Ports Already in Use

**Error:** `Bind for 0.0.0.0:5000 failed: port is already allocated`

**Solution:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# For port 5173 (frontend)
lsof -ti:5173 | xargs kill -9

# For port 5432 (postgres)
lsof -ti:5432 | xargs kill -9
```

### Container Keeps Restarting

**Solution:**
```bash
# View logs to see the error
docker-compose logs backend

# Common fix: rebuild containers
docker-compose down
docker-compose up --build
```

### Volume Permission Issues

**Solution:**
```bash
# On Linux/Mac, fix permissions
sudo chown -R $USER:$USER backend/uploads

# Or remove and recreate volumes
docker-compose down -v
docker-compose up --build
```

---

## 🔐 Authentication Issues

### Can't Login After Registration

**Check:**
1. Are you using the correct email/password?
2. Check browser console for errors (F12)
3. Check backend logs: `docker-compose logs backend`

**Solution:**
```bash
# Reset database and try again
docker-compose down -v
docker-compose up --build
```

### JWT Token Errors

**Error:** `Token has expired` or `Invalid token`

**Solution:**
- Logout and login again
- Clear browser localStorage:
  ```javascript
  // In browser console (F12)
  localStorage.clear()
  ```

---

## 🎨 Frontend Issues

### Blank Page / White Screen

**Solution:**
```bash
# Check browser console (F12) for errors
# Usually means backend is not running

# Verify backend is up
curl http://localhost:5000/api/health

# If backend is down, restart it
docker-compose restart backend
```

### "Failed to fetch" errors

**Check:**
1. Is backend running? `curl http://localhost:5000/api/health`
2. Check CORS settings in `.env`
3. Verify `FRONTEND_URL=http://localhost:5173` in `.env`

**Solution:**
```bash
# Restart both services
docker-compose restart backend frontend
```

### Changes Not Showing

**Solution:**
```bash
# Hard refresh browser
# Mac: Cmd + Shift + R
# Windows/Linux: Ctrl + Shift + R

# Or clear cache and reload
```

---

## 📦 Installation Issues

### npm install fails

**Solution:**
```bash
cd frontend

# Clear cache
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still fails, try:
npm install --legacy-peer-deps
```

### pip install fails

**Solution:**
```bash
cd backend

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# If specific package fails, install individually
pip install flask==3.0.0
```

---

## 🔄 Migration Issues (If using Flask-Migrate)

### Want to use Flask-Migrate instead of init_db.py?

**Setup:**
```bash
cd backend

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

**Update docker-compose.yml:**
```yaml
command: >
  sh -c "flask db upgrade &&
         python run.py"
```

---

## 🌐 Network Issues

### Can't Access localhost:5173

**Check:**
```bash
# Verify frontend is running
docker ps | grep frontend

# Check frontend logs
docker-compose logs frontend

# Verify port binding
netstat -an | grep 5173
```

**Solution:**
```bash
# Restart frontend
docker-compose restart frontend

# Or access via 127.0.0.1:5173
```

---

## 💾 Data Issues

### Need to Reset Everything

**Complete Reset:**
```bash
# Stop and remove everything
docker-compose down -v

# Remove all images (optional)
docker-compose down --rmi all -v

# Rebuild from scratch
docker-compose up --build
```

### Want to Keep Some Data

**Backup Database:**
```bash
# Export database
docker exec elderconnect_db pg_dump -U elderconnect_user elderconnect_db > backup.sql

# Import later
docker exec -i elderconnect_db psql -U elderconnect_user elderconnect_db < backup.sql
```

---

## 🔍 Debugging Tips

### View All Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Access Container Shell
```bash
# Backend
docker exec -it elderconnect_backend bash

# Frontend
docker exec -it elderconnect_frontend sh

# Database
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db
```

### Check Environment Variables
```bash
# Inside backend container
docker exec elderconnect_backend env | grep FLASK
docker exec elderconnect_backend env | grep DATABASE
```

### Test Database Connection
```bash
# From host machine
psql -h localhost -U elderconnect_user -d elderconnect_db

# Inside backend container
docker exec -it elderconnect_backend python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     from sqlalchemy import inspect
...     print(inspect(db.engine).get_table_names())
```

---

## 🚨 Common Error Messages

### "ModuleNotFoundError: No module named 'app'"

**Solution:**
```bash
# Make sure you're in the right directory
cd backend
python run.py

# Or set PYTHONPATH
export PYTHONPATH=/app:$PYTHONPATH
python run.py
```

### "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution:**
Check `.env` file has:
```bash
FRONTEND_URL=http://localhost:5173
```

Restart backend:
```bash
docker-compose restart backend
```

### "SQLALCHEMY_DATABASE_URI was not set"

**Solution:**
Check `.env` file exists and has:
```bash
DATABASE_URL=postgresql://elderconnect_user:elderconnect_pass@db:5432/elderconnect_db
```

---

## 💡 Performance Issues

### Slow Queries

**Solution:**
```bash
# Access database
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db

# Check slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

# Add indexes if needed
CREATE INDEX idx_bookings_elder ON bookings(elder_id);
CREATE INDEX idx_bookings_caregiver ON bookings(caregiver_id);
```

### High Memory Usage

**Solution:**
```bash
# Limit container resources in docker-compose.yml
services:
  backend:
    mem_limit: 512m
    cpus: 1
```

---

## 📞 Getting More Help

### Still Having Issues?

1. **Check logs thoroughly:**
   ```bash
   docker-compose logs -f
   ```

2. **Search for error message** in browser console and terminal

3. **Verify all files exist:**
   ```bash
   ./verify_setup.sh
   ```

4. **Try complete reset:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

5. **Check system requirements:**
   - Docker Desktop running?
   - Enough disk space?
   - Enough RAM (4GB+ recommended)?

### Useful Commands Summary
```bash
# Full restart
docker-compose restart

# Complete reset
docker-compose down -v && docker-compose up --build

# View logs
docker-compose logs -f backend

# Access container
docker exec -it elderconnect_backend bash

# Check health
curl http://localhost:5000/api/health
```

---

## ✅ Health Check Checklist

Before asking for help, verify:

- [ ] Docker Desktop is running
- [ ] Ports 5000, 5173, 5432 are not in use
- [ ] `.env` file exists with correct values
- [ ] All containers are running: `docker ps`
- [ ] Backend health check works: `curl http://localhost:5000/api/health`
- [ ] Frontend loads in browser: `http://localhost:5173`
- [ ] No errors in browser console (F12)
- [ ] No errors in `docker-compose logs`

---

**Most issues can be fixed with a clean restart:**
```bash
docker-compose down -v
docker-compose up --build
```
