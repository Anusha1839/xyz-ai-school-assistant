# 🎨 XYZ AI - Customization Guide

Learn how to customize XYZ AI for your specific school needs.

---

## 📝 1. Customize User Data

### Edit Mock Users
File: `app.py` (lines ~150-160)

```python
MOCK_USERS = {
    'student@yourschool.com': {
        'password': 'student123',
        'role': 'Student',
        'name': 'Rahul Kumar',
        'child': 'Rahul',
        'class': '10-A',
        'rollno': '101'
    },
    'parent@yourschool.com': {
        'password': 'parent123',
        'role': 'Parent',
        'name': 'Rajesh Kumar',
        'child': 'Rahul',
    },
    # Add more users...
}
```

### Add Database Integration (Future)
```python
def authenticate_user(email: str, password: str):
    # Connect to real database
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return True, user_data
    return False, None
```

---

## 📊 2. Customize Mock Data

### Edit Attendance Data
File: `app.py` or `utils.py`

```python
MOCK_ATTENDANCE_DATA = {
    'Student1': {
        'present': 85,
        'absent': 8,
        'leave': 7,
        'percentage': 91.2
    },
    'Student2': {
        'present': 78,
        'absent': 12,
        'leave': 10,
        'percentage': 84.3
    },
    # Add all students...
}
```

### Edit Grades Data
```python
MOCK_GRADES_DATA = {
    'Student1': {
        'Math': 'A',
        'English': 'B+',
        'Science': 'A',
        'History': 'B',
        'PE': 'A',
        'Art': 'A-',
        # Add more subjects...
    },
    # Add more students...
}
```

### Add Custom Metrics
```python
def get_school_analytics():
    return {
        'total_students': 150,
        'average_attendance': 90.8,
        'students_above_90': 120,
        'students_below_75': 5,
        'average_gpa': 3.7,
        'placement_rate': 95.5,  # Add custom metrics
        'sports_participants': 45,
    }
```

---

## 🌈 3. Customize UI Theme

### Edit Color Scheme
File: `.streamlit/config.toml`

```toml
[theme]
# Your school colors
primaryColor = "#1f77b4"        # Your primary color
backgroundColor = "#ffffff"     # Background
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Edit CSS Styling
File: `app.py` (CSS section)

```python
st.markdown("""
    <style>
        .auth-header h1 {
            color: #your-color;
            font-family: 'Your Font';
        }
        .chat-header {
            background: linear-gradient(135deg, #color1 0%, #color2 100%);
        }
        /* Add more custom CSS */
    </style>
""", unsafe_allow_html=True)
```

### Add School Logo
```python
st.markdown("""
    <div style="text-align: center;">
        <img src="https://your-school-logo-url.png" width="200">
        <h1>Your School Name</h1>
    </div>
""", unsafe_allow_html=True)
```

---

## 🎯 4. Customize AI Behavior

### Edit System Prompts
File: `app.py` (lines ~165-190)

```python
SYSTEM_PROMPTS = {
    'Student': """You are a friendly academic assistant for [School Name].
    - Be encouraging and supportive
    - Help with: attendance, grades, academic queries
    - Mention [School Name] when relevant
    - Use our school's terminology
    - Keep responses under 3 sentences initially""",
    
    'Parent': """You are a caring support assistant for [School Name].
    - Address parents professionally
    - Ask about specific child
    - Provide detailed performance insights
    - Mention school contact info when needed""",
    
    'Teacher': """You are a professional assistant for [School Name] teachers.
    - Support classroom management
    - Help with attendance marking
    - Provide student analytics
    - Confirm before marking attendance""",
    
    'Principal': """You are a management assistant for [School Name].
    - Provide strategic insights
    - Focus on key metrics
    - Support decision-making
    - Reference school policies"""
}
```

### Customize Gemini Model
```python
# Use different models
model = genai.GenerativeModel('gemini-2.5-flash')      # Current
model = genai.GenerativeModel('gemini-3.6-flash')  # With vision

# Adjust parameters
response = model.generate_content(
    prompt,
    generation_config={
        'temperature': 0.7,      # Creativity (0-1)
        'top_p': 0.95,          # Diversity
        'top_k': 40,            # Token selection
        'max_output_tokens': 1000,  # Response length
    }
)
```

---

## 🔌 5. Add Custom Features

### Add Homework Tracking
```python
MOCK_HOMEWORK = {
    'Subject': 'Math',
    'Topic': 'Algebra',
    'DueDate': '2024-09-20',
    'Status': 'Pending',
    'Submission': None
}

def get_homework(student_name):
    # Return homework for student
    pass

def submit_homework(student_name, file):
    # Process submission
    pass
```

### Add Exam Schedule
```python
EXAM_SCHEDULE = {
    '2024-10-15': {'subject': 'Math', 'time': '09:00 AM'},
    '2024-10-16': {'subject': 'English', 'time': '02:00 PM'},
    # More exams...
}

def get_exam_schedule(student_id):
    # Return upcoming exams
    pass
```

### Add Announcements
```python
ANNOUNCEMENTS = [
    {
        'date': '2024-09-15',
        'title': 'Annual Sports Day',
        'content': 'All students participate in sports day...',
        'audience': ['Student', 'Parent']
    },
    # More announcements...
]

def get_announcements(role):
    # Return relevant announcements
    pass
```

### Add Fee Management
```python
FEES = {
    'Rahul': {
        'monthly': 5000,
        'paid': 10000,
        'pending': 5000,
        'duedate': '2024-09-30'
    }
}

def get_fee_status(student_id):
    # Return fee information
    pass
```

---

## 📱 6. Multi-Language Customization

### Add New Languages
File: `utils.py`

```python
LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Bengali': 'bn',
    'Gujarati': 'gu',
    'Punjabi': 'pa',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Urdu': 'ur',
    'Spanish': 'es',      # Add new
    'French': 'fr',       # Add new
}

LANGUAGE_PROMPTS = {
    'es': "Por favor, responda en español.",
    'fr': "Veuillez répondre en français.",
    # Add more...
}
```

### Localize Messages
```python
MESSAGES = {
    'en': {
        'welcome': 'Welcome to XYZ AI',
        'attendance': 'Attendance',
        'grades': 'Grades',
    },
    'hi': {
        'welcome': 'XYZ AI में आपका स्वागत है',
        'attendance': 'उपस्थिति',
        'grades': 'अंक',
    },
    # Add more languages...
}
```

---

## 🔐 7. Security Customization

### Add 2FA Authentication
```python
def send_otp(email: str) -> str:
    otp = generate_random_otp()
    # Send via email
    return otp

def verify_otp(email: str, otp: str) -> bool:
    # Verify OTP from cache/database
    pass

if authenticate_user(email, password):
    if requires_2fa(role):
        otp = send_otp(email)
        entered_otp = st.text_input("Enter OTP:")
        if verify_otp(email, entered_otp):
            # Complete authentication
            pass
```

### Add Role-Based Access Control
```python
def check_permission(user_role: str, action: str) -> bool:
    permissions = {
        'Student': ['view_own_data', 'submit_homework'],
        'Parent': ['view_child_data', 'communicate_teacher'],
        'Teacher': ['mark_attendance', 'upload_grades'],
        'Principal': ['view_all_data', 'manage_users'],
    }
    return action in permissions.get(user_role, [])

# Use in functions
if check_permission(user_role, 'mark_attendance'):
    mark_attendance_ui()
else:
    st.error("You don't have permission for this action")
```

### Add Activity Logging
```python
def log_activity(user_email: str, action: str, details: dict):
    activity = {
        'timestamp': datetime.now(),
        'user': user_email,
        'action': action,
        'details': details,
        'ip': request.remote_addr,
    }
    # Save to database
    db.add(activity)
```

---

## 📧 8. Email & Notification Customization

### Add Email Notifications
```python
import smtplib
from email.mime.text import MIMEText

def send_email(recipient: str, subject: str, body: str):
    sender = "noreply@yourschool.com"
    password = os.getenv('EMAIL_PASSWORD')
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# Send notifications
send_email(
    parent_email,
    'Attendance Alert',
    f'Your child has low attendance. Current: 70%'
)
```

### Add SMS Notifications
```python
from twilio.rest import Client

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_sms(phone: str, message: str):
    client.messages.create(
        body=message,
        from_='+1234567890',
        to=phone
    )

# Send SMS alert
send_sms(
    parent_phone,
    'Attendance Alert: Your child was absent today'
)
```

---

## 🗄️ 9. Database Integration

### Switch to Real Database
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create database connection
DATABASE_URL = "postgresql://user:password@localhost/xyz_ai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    role = Column(String)
    name = Column(String)

# Use in authentication
def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        return True, user
    return False, None
```

### Environment Variables
Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/xyz_ai
EMAIL_PASSWORD=your-email-password
GEMINI_API_KEY=your-api-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

---

## 🎓 10. Add Learning Management Features

### Add Course Management
```python
COURSES = {
    'MATH101': {
        'name': 'Algebra I',
        'teacher': 'Ms. Priya',
        'students': 30,
        'credits': 3,
        'syllabus': 'url-to-syllabus'
    },
}

def get_student_courses(student_id):
    # Return enrolled courses
    pass
```

### Add Assignment Tracking
```python
ASSIGNMENTS = {
    'MATH101': [
        {
            'id': 'ASN001',
            'title': 'Chapter 5 Exercises',
            'deadline': '2024-09-20',
            'submitted': True,
            'grade': 'A',
        },
    ],
}

def submit_assignment(course_id, assignment_id, file):
    # Process submission
    pass
```

---

## 📊 11. Add Analytics Dashboard

```python
import plotly.express as px
import pandas as pd

def show_analytics_dashboard():
    # Attendance chart
    attendance_data = get_attendance_statistics()
    fig = px.bar(attendance_data, x='name', y='percentage')
    st.plotly_chart(fig)
    
    # Performance metrics
    metrics_df = get_class_metrics()
    st.dataframe(metrics_df)
    
    # Trend analysis
    trend_data = get_attendance_trend()
    fig2 = px.line(trend_data, x='date', y='attendance')
    st.plotly_chart(fig2)
```

---

## 🚀 12. Deployment Customization

### Environment-Specific Configuration
```python
import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    GEMINI_MODEL = 'gemini-pro'
    DEBUG = False
    CACHE_TIMEOUT = 3600
elif ENVIRONMENT == 'staging':
    GEMINI_MODEL = 'gemini-pro'
    DEBUG = True
    CACHE_TIMEOUT = 600
else:  # development
    GEMINI_MODEL = 'gemini-pro'
    DEBUG = True
    CACHE_TIMEOUT = 0
```

---

## ✅ Quick Customization Checklist

- [ ] Update school name in UI
- [ ] Customize colors to school theme
- [ ] Add school logo
- [ ] Update mock data with actual students
- [ ] Customize AI prompts for your context
- [ ] Add school-specific features
- [ ] Set up email/SMS notifications
- [ ] Configure database if needed
- [ ] Update language support as needed
- [ ] Test all features thoroughly
- [ ] Deploy to your platform
- [ ] Monitor performance
- [ ] Gather user feedback
- [ ] Iterate and improve

---

## 📞 Support

For help with customization:
- Check the main README.md
- See code comments
- Review Google Gemini documentation: https://ai.google.dev/
- Check Streamlit documentation: https://docs.streamlit.io

---

**Happy Customizing! 🎨**

*Last Updated: August 2024*
