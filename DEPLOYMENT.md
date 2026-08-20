# 🌐 XYZ AI - Cloud Deployment Guide

Complete instructions for deploying to popular cloud platforms.

---

## ☁️ 1. Streamlit Cloud (Recommended - FREE)

**Pros:** Free, easiest setup, automatic updates, built-in CI/CD
**Time:** 5 minutes

### Step 1: Prepare GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Connect GitHub account
4. Select your repository and `app.py`
5. Click **"Deploy"**

### Step 3: Add API Key

1. Click **Settings** (⚙️)
2. Go to **Secrets**
3. Add:
```toml
gemini_api_key = "your-api-key-here"
```
4. Save

**✓ Done!** Your app is live at `https://your-username-repo-name.streamlit.app`

---

## 🚀 2. Heroku (Paid - $5-7/month)

**Pros:** More control, custom domain, 24/7 uptime
**Time:** 10 minutes

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed

### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows - Download from: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App
```bash
heroku login
heroku create your-xyz-ai-app
```

### Step 3: Add Buildpack
```bash
heroku buildpacks:add heroku/python
```

### Step 4: Set Environment Variables
```bash
heroku config:set GEMINI_API_KEY="your-api-key-here"
```

### Step 5: Deploy
```bash
git push heroku main
```

### View Logs
```bash
heroku logs --tail
```

**✓ Live at:** `https://your-xyz-ai-app.herokuapp.com`

---

## 🐳 3. Docker + Cloud Run (Google Cloud)

**Pros:** Serverless, pay-as-you-go, scalable
**Time:** 15 minutes

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed
- Docker installed

### Step 1: Create Project
```bash
gcloud projects create xyz-ai-school
gcloud config set project xyz-ai-school
```

### Step 2: Build Docker Image
```bash
docker build -t xyz-ai:latest .
```

### Step 3: Tag for Google Cloud
```bash
docker tag xyz-ai:latest gcr.io/xyz-ai-school/xyz-ai:latest
```

### Step 4: Push to Google Container Registry
```bash
docker push gcr.io/xyz-ai-school/xyz-ai:latest
```

### Step 5: Deploy to Cloud Run
```bash
gcloud run deploy xyz-ai \
  --image gcr.io/xyz-ai-school/xyz-ai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-key
```

**✓ Live at:** `https://xyz-ai-XXXXX.run.app`

---

## 💻 4. Railway.app (FREE - $5 credits)

**Pros:** Simple, free credits, GitHub integration
**Time:** 5 minutes

### Step 1: Go to Railway
https://railway.app

### Step 2: Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub"**
- Authorize & select your repo

### Step 3: Add Environment Variables
1. Go to **Variables**
2. Add: `GEMINI_API_KEY = your-key`
3. Click **Deploy**

**✓ Live!** URL shown in dashboard

---

## 🌍 5. Render.com (FREE - with limitations)

**Pros:** Free tier available, simple setup
**Time:** 5 minutes

### Step 1: Go to Render
https://render.com

### Step 2: Create Service
- Click **"New+"**
- Select **"Web Service"**
- Connect GitHub

### Step 3: Configure
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Step 4: Add Environment Variables
- `GEMINI_API_KEY = your-key`
- Click **"Create Web Service"**

**✓ Live!** URL in dashboard (free tier has limited uptime)

---

## 🐍 6. PythonAnywhere (Free - with limitations)

**Pros:** Python-specific, easy setup, free tier
**Time:** 10 minutes

### Step 1: Create Account
https://www.pythonanywhere.com

### Step 2: Upload Code
- Use **"Upload a file"** or Git

### Step 3: Setup Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.9 xyz-ai
pip install -r requirements.txt
```

### Step 4: Configure WSGI
Edit WSGI file to use Streamlit

### Step 5: Add Environment Variables
In **.env** file:
```
GEMINI_API_KEY=your-key
```

**Note:** Streamlit on PythonAnywhere requires special configuration

---

## 🚀 7. AWS EC2 (Paid - $5-20/month)

**Pros:** Full control, scalable, most features
**Time:** 20 minutes

### Step 1: Create EC2 Instance
- Launch Ubuntu 20.04 LTS instance
- Security group: Allow ports 80, 443, 8501

### Step 2: SSH into Instance
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### Step 3: Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

### Step 4: Clone Repository
```bash
git clone https://github.com/yourusername/xyz-ai.git
cd xyz-ai
```

### Step 5: Setup and Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add API key
echo 'gemini_api_key = "your-key"' > .streamlit/secrets.toml

# Run with systemd (optional)
streamlit run app.py --server.port 8501
```

### Step 6: Use Reverse Proxy (Nginx)
```bash
sudo apt install nginx
# Configure Nginx to proxy to localhost:8501
```

**✓ Live at:** `http://your-instance-ip`

---

## 🌐 8. DigitalOcean App Platform

**Pros:** Simple, affordable, good documentation
**Time:** 10 minutes

### Step 1: Go to DigitalOcean
https://www.digitalocean.com/products/app-platform

### Step 2: Create App
- Connect GitHub repository
- Auto-detect Python

### Step 3: Configure
```yaml
name: xyz-ai
services:
  - name: web
    github:
      repo: yourusername/xyz-ai
      branch: main
    build_command: pip install -r requirements.txt
    run_command: streamlit run app.py --server.port 8080
    envs:
      - key: GEMINI_API_KEY
        value: your-key
```

### Step 4: Deploy
Click **Deploy**

**✓ Live!** URL provided

---

## 📊 Comparison Table

| Platform | Cost | Setup Time | Uptime | Scaling | Free Tier |
|----------|------|-----------|--------|---------|-----------|
| Streamlit Cloud | FREE | 5 min | 99.9% | ✓ Excellent | ✓ Yes |
| Heroku | $7/mo | 10 min | 99% | ✓ Good | Limited |
| Google Cloud Run | Pay-as-you-go | 15 min | 99.95% | ✓ Excellent | ✓ Free credits |
| Railway | FREE | 5 min | 99% | ✓ Good | ✓ $5 credits |
| Render | FREE | 5 min | 99% | ✓ Fair | ✓ Limited |
| PythonAnywhere | FREE | 10 min | 99% | ✗ Limited | ✓ Limited |
| AWS EC2 | $5-20 | 20 min | 99.99% | ✓ Excellent | Limited |
| DigitalOcean | $5+ | 10 min | 99% | ✓ Good | Limited |

---

## 🔒 Security Checklist

- [ ] API keys in environment variables (not hardcoded)
- [ ] Enable HTTPS/SSL
- [ ] Set up authentication
- [ ] Enable CORS if needed
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Update dependencies regularly
- [ ] Use secrets management

---

## 📱 Custom Domain Setup

### Streamlit Cloud
```
1. Go to app settings
2. Custom domain section
3. Add domain
4. Update DNS CNAME record
```

### Heroku
```bash
heroku domains:add yourdomain.com
# Update DNS CNAME to your-app.herokuapp.com
```

### Other Platforms
Check platform documentation for domain configuration.

---

## 🐛 Troubleshooting

### "Port already in use"
```bash
streamlit run app.py --server.port 8080
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not working"
- Verify at https://makersuite.google.com/app/apikey
- Check environment variable syntax
- Restart application

### "Slow loading"
- Check internet connection
- Upgrade server specs
- Enable caching

---

## 📈 Performance Optimization

1. **Caching:**
```python
@st.cache_data
def expensive_function():
    return compute_result()
```

2. **Session State:**
Use `st.session_state` instead of widget defaults

3. **Lazy Loading:**
Load heavy imports only when needed

4. **CDN:**
Serve static files through CDN

---

## 📞 Support

- **Streamlit:** https://docs.streamlit.io
- **Heroku:** https://devcenter.heroku.com
- **Google Cloud:** https://cloud.google.com/docs
- **Railway:** https://docs.railway.app
- **Render:** https://render.com/docs

---

**🎉 Choose your platform and deploy in minutes!**

*Last Updated: August 2024*
