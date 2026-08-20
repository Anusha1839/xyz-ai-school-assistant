# 🤖 XYZ AI - Human-Like AI School Assistant

A comprehensive Streamlit-based AI school assistant that acts as a real human assistant for students, parents, teachers, and school management. Built with Google Gemini API and featuring multi-language support, role-based permissions, and a professional chat interface.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 🔐 Authentication & Authorization
- 4 Role-based access: Student, Parent, Teacher, Principal
- Secure login with mock database
- Demo mode for quick testing
- Session management

### 💬 Chat Interface
- Real-time conversation with Gemini AI
- Message history with timestamps
- Responsive design with animations
- Context-aware responses

### 🌍 Multi-Language Support
- 11 Indian languages supported:
  - English, Hindi, Tamil, Telugu, Marathi
  - Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu
- Real-time language switching
- AI responds in selected language

### 👥 Role-Specific Features

**Student:**
- View own attendance
- Check grades/marks
- Get study recommendations
- Ask general school questions

**Parent:**
- View child's attendance
- Check child's grades
- Understand child's performance
- Get school update notifications

**Teacher:**
- Mark student attendance
- Record grades
- View class analytics
- Manage student information

**Principal:**
- View school-wide attendance analytics
- Overall performance metrics
- Staff management queries
- Decision support data

### 📊 Mock API Integration
- Attendance tracking
- Grade management
- Performance analytics
- School operations data

### 📞 Escalation System
- "Talk to Teacher" button
- "Contact Management" option
- Request tracking
- Status confirmation

### 🎨 Professional UI
- Gradient color scheme (Purple/Blue)
- Responsive layout
- Smooth animations
- Mobile-friendly design
- Dark mode ready

---

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.8 or higher
- pip package manager
- Gemini API key (free tier available)
```

### Installation

1. **Clone/Download Repository**
```bash
git clone https://github.com/yourusername/xyz-ai-school-assistant.git
cd xyz-ai-school-assistant
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Gemini API Key**

Get your free API key:
- Visit: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

Add to `.streamlit/secrets.toml`:
```toml
gemini_api_key = "your-api-key-here"
```

5. **Run Application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📱 Demo Credentials

| Role | Email | Password | Use Case |
|------|-------|----------|----------|
| **Student** | student@school.com | student123 | View own attendance/grades |
| **Parent** | parent@school.com | parent123 | Check child's performance |
| **Teacher** | teacher@school.com | teacher123 | Mark attendance, record grades |
| **Principal** | principal@school.com | principal123 | View school analytics |

Or click **"Demo Mode"** for instant access without entering credentials!

---

## 🎯 Usage Examples

### Student
```
Student: "What is my attendance?"
XYZ AI: "Your current attendance is 91.2% (85 days present, 8 days absent, 7 days leave)"

Student: "What are my grades?"
XYZ AI: "Your grades: Math A, English B+, Science A, History B, PE A"
```

### Parent
```
Parent: "How much attendance does my child have?"
XYZ AI: "Rahul currently has 91.2% attendance. Would you like to see his recent grades?"

Parent: "I want to talk to his teacher"
XYZ AI: "I can connect you with Ms. Priya. Would you like me to request a call now?"
```

### Principal
```
Principal: "What is the overall attendance?"
XYZ AI: "School Overall Attendance: 90.8%. Total Students: 3 (Analytics continues...)"

Principal: "Show me performance metrics"
XYZ AI: "(Provides detailed school-wide performance data)"
```

---

## 📂 Project Structure

```
xyz-ai-school-assistant/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
│
├── .streamlit/
│   ├── config.toml          # Streamlit theme & settings
│   └── secrets.toml         # API keys (not in git) ⚠️
│
├── Docker/
│   └── Dockerfile           # Docker containerization
│
├── Procfile                 # Heroku deployment config
│
├── SETUP_GUIDE.md           # Detailed setup instructions
└── README.md                # This file
```

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended)
**Easiest & Free option**

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" → Select your repo
4. In app settings, add secrets:
   ```
   gemini_api_key = "your-key"
   ```
5. Deploy!

### Option 2: Heroku
**Paid but powerful**

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
heroku config:set GEMINI_API_KEY="your-key"
git push heroku main
```

### Option 3: Docker
**For self-hosted servers**

```bash
# Build image
docker build -t xyz-ai .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your-key" \
  xyz-ai
```

### Option 4: Railway, Render, or PythonAnywhere
See SETUP_GUIDE.md for detailed instructions

---

## 🔒 Security Features

✅ Role-based access control
✅ Mock API authentication
✅ Prompt injection prevention
✅ Secure credential storage
✅ No sensitive data in logs
✅ API key protection via secrets management
✅ CORS configuration
✅ Session management

---

## 🛠️ Advanced Configuration

### Customize Mock Data
Edit the `MOCK_*_DATA` dictionaries in `app.py`:

```python
MOCK_ATTENDANCE_DATA = {
    'Rahul': {'present': 85, 'absent': 8, 'leave': 7, 'percentage': 91.2},
    'Arjun': {'present': 78, 'absent': 12, 'leave': 10, 'percentage': 84.3},
    # Add more students...
}
```

### Customize System Prompts
Edit `SYSTEM_PROMPTS` dictionary to change AI behavior:

```python
SYSTEM_PROMPTS = {
    'Student': "Your custom prompt here...",
    'Parent': "Parent-specific prompt...",
    # etc.
}
```

### Customize UI Theme
Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
textColor = "#262730"
```

---

## 📊 Gemini API Models

The app uses `gemini-pro` model:
- **Free Tier**: 60 requests/minute
- **Paid Tier**: Unlimited (pay-as-you-go)
- **Context Window**: 30K tokens
- **Response Time**: ~1-3 seconds

See pricing at: https://ai.google.dev/pricing

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### API Key not working
1. Verify key at https://makersuite.google.com/app/apikey
2. Check `.streamlit/secrets.toml` has no extra spaces
3. Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

### Slow Response Times
1. Check internet connection
2. Verify Gemini API is responsive
3. Reduce chat history size

### Port 8501 Already in Use
```bash
streamlit run app.py --server.port 8502
```

### CSS Not Loading
- Hard refresh browser: `Ctrl+Shift+R`
- Clear cache: Browser Settings → Clear Browsing Data

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Page Load Time | < 2s |
| API Response Time | 1-3s |
| Concurrent Users | 10+ |
| Chat History Size | Up to 100 messages |
| Languages Supported | 11 |
| Mobile Compatible | ✅ Yes |

---

## 🎓 Learning Outcomes

By studying this project, you'll learn:
- ✅ Streamlit framework & advanced features
- ✅ Google Gemini API integration
- ✅ Role-based access control
- ✅ Session management in web apps
- ✅ Professional UI/UX design
- ✅ Cloud deployment strategies
- ✅ Security best practices
- ✅ API integration patterns

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Email**: support@xyzai.school
- **Documentation**: See SETUP_GUIDE.md
- **API Docs**: https://ai.google.dev/docs

---

## 🙏 Acknowledgments

- Google Gemini API for powerful AI capabilities
- Streamlit for amazing web framework
- All contributors and testers

---

## 📌 Version History

**v1.0.0** (Current)
- ✅ Complete chat interface
- ✅ Multi-language support
- ✅ Role-based access
- ✅ Mock API integration
- ✅ Professional UI
- ✅ Multiple deployment options

**Planned Features:**
- 🔄 Real database integration
- 🎤 Voice input/output
- 👤 AI Avatar with animations
- 📧 Email notifications
- 📱 Mobile app
- 🔐 2FA authentication

