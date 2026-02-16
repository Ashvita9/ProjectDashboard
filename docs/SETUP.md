# Development Setup Guide

Complete instructions for setting up the Project Dashboard application locally.

## Prerequisites

- **Node.js** v16+ and npm
- **Python** 3.8+
- **MongoDB** (local or MongoDB Atlas)

## Backend Setup

### 1. Navigate to backend directory
```bash
cd project-dashboard/backend
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
MONGODB_URI=mongodb://localhost:27017
```

> **Note:** For MongoDB Atlas, use your connection string:
> `MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net`

### 5. Run the server
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend/dashboard
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure API URL (optional)
Edit `src/services/api.js` if your backend runs on a different port:
```javascript
baseURL: 'http://localhost:8000/api'
```

### 4. Run development server
```bash
npm run serve
```

Frontend will be available at `http://localhost:8080`

## Running Both Servers

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd project-dashboard/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend/dashboard
npm run serve
```

## Verifying Setup

1. Open `http://localhost:8080` in your browser
2. Register a new account
3. Create a project
4. Add tasks and drag them between columns

## Common Issues

### CORS Errors
If you see CORS errors in the browser console:
1. Check that backend is running on port 8000
2. Verify `CORS_ALLOWED_ORIGINS` in `settings.py` includes your frontend URL

### MongoDB Connection Failed
1. Ensure MongoDB is running locally, or
2. Check your Atlas connection string in `.env`
3. Whitelist your IP in MongoDB Atlas (if using Atlas)

### Port Already in Use
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 8080 (Windows)
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

## Build for Production

### Frontend
```bash
cd frontend/dashboard
npm run build
```
Output will be in `dist/` folder.

### Backend
```bash
# Set DEBUG=False in .env
DEBUG=False

# Use gunicorn for production
pip install gunicorn
gunicorn backend.wsgi:application
```

## Testing

### Run Frontend Linting
```bash
cd frontend/dashboard
npm run lint
```

### Test API with Postman
Import `project-dashboard/postman_collection.json` into Postman for pre-configured API requests.
