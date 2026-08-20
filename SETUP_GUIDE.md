# XYZ AI School Assistant - Setup & Deployment Guide

## 🚀 Quick Start (Local)

### 1. Prerequisites
- Python 3.8+
- pip package manager
- Git (optional)

### 2. Installation Steps

```bash
# Clone or download the project
cd xyz-ai-school-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Gemini API Key

**Get Your API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

**Add API Key to Streamlit:**

Create/edit `.streamlit/secrets.toml`:
```toml
gemini_api_key = "your-api-key-here"
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📋 Demo Credentials

Use these to test the app:

| Role | Email | Password |
|------|-------|----------|
| Student | student@school.com | student123 |
| Parent | parent@school.com | parent123 |
| Teacher | teacher@school.com | teacher123 |
| Principal | principal@school.com | principal123 |

Or click **"Demo Mode"** for instant access.

---

## ☁️ Deploy to Streamlit Cloud

### 1. Prepare Repository

```bash
# Initialize git if not done
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repository
4. Set main file: `app.py`
5. Click "Deploy"

### 3. Add Secrets

In Streamlit Cloud dashboard:
1. Go to App → Settings → Secrets
2. Add:
```toml
gemini_api_key = "your-api-key-here"
```

---

## 🌐 Deploy to Heroku

### 1. Create Procfile

Create `Procfile` in project root:
```
web: streamlit run --server.port $PORT app.py
```

### 2. Create requirements.txt with pinned versions

Already provided ✓

### 3. Deploy

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY="your-api-key"

# Deploy
git push heroku main
```

---

## 🐳 Deploy with Docker

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Create .dockerignore

```
__pycache__
*.pyc
.git
.env
.streamlit/secrets.toml
```

### 3. Build & Run

```bash
# Build
docker build -t xyz-ai .

# Run
docker run -p 8501:8501 -e GEMINI_API_KEY="your-key" xyz-ai
```

---

## 🔐 Security Notes

⚠️ **Never commit API keys!**

1. Keep `.streamlit/secrets.toml` in `.gitignore`
2. Use environment variables in production
3. Rotate API keys periodically
4. Use Streamlit Cloud's Secrets management

---

## 📱 Features

✅ Multi-role authentication (Student, Parent, Teacher, Principal)
✅ 11 language support (English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu)
✅ Real-time chat with Gemini AI
✅ Mock API integration (Attendance, Grades, Analytics)
✅ Role-based permissions
✅ Escalation to teacher/management
✅ Professional UI with animations
✅ Conversation history management
✅ Timestamp tracking

---

## 🛠️ Troubleshooting

### Issue: "AttributeError: module 'google.generativeai' has no attribute 'GenerativeModel'"
**Solution:** Update google-generativeai package
```bash
pip install --upgrade google-generativeai
```

### Issue: API Key not working
**Solution:** 
- Verify key at https://makersuite.google.com/app/apikey
- Check in secrets.toml or environment variables
- Ensure no extra spaces in key

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: CSS not loading properly
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)

---

## 📞 Support

For issues:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Gemini API docs: https://ai.google.dev/
3. Create GitHub issue with error details

---

## 📄 File Structure

```
xyz-ai-school-assistant/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── .env.example          # Environment variables template
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # API keys (not in git)
├── Dockerfile            # Docker configuration
├── Procfile             # Heroku configuration
└── README.md            # Project documentation
```

---

## 🎯 Next Steps

1. Set up your Gemini API key
2. Run the app locally
3. Test with demo credentials
4. Deploy to your preferred platform
5. Customize for your school data

Enjoy! 🤖
