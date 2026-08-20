import io
import os
import hashlib
from datetime import datetime

import streamlit as st
from google import genai
import speech_recognition as sr
from gtts import gTTS


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="XYZ AI - School Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# API CONFIG
# =========================================================

try:
    if "gemini_api_key" in st.secrets:
        GEMINI_API_KEY = st.secrets["gemini_api_key"]
    else:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
except Exception:
    GEMINI_API_KEY = ""

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None


# Current stable Flash model. Fallback is kept for availability.
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-3.6-flash",
]


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.block-container {
    max-width: 1200px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    top: 0.5rem !important;
}

.app-title {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 8px;
}

.badge {
    display: inline-block;
    color: white;
    background: rgba(255,255,255,0.20);
    padding: 5px 13px;
    border-radius: 18px;
    margin-right: 6px;
    font-size: 13px;
}

.login-card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
    text-align: center;
    margin: 25px auto 25px auto;
    max-width: 540px;
}

.login-icon {
    font-size: 52px;
}

.login-title {
    color: #667eea;
    font-size: 30px;
    font-weight: 700;
    margin-top: 5px;
}

.login-subtitle {
    color: #777;
    font-size: 14px;
}

div[data-testid="stTextInput"] input {
    background: #171b29 !important;
    color: white !important;
    border: 1px solid #34394b !important;
    border-radius: 12px !important;
    min-height: 48px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #9fa3b1 !important;
}

div[data-testid="stAudioInput"] {
    background: #171b29 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    padding: 2px !important;
}

div[data-testid="stAudioInput"] label {
    display: none !important;
}

.stButton > button {
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 600 !important;
}

audio {
    width: 100%;
}

hr {
    border-color: rgba(255,255,255,0.25) !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "authenticated": False,
    "user_role": None,
    "user_email": None,
    "language": "English",
    "messages": [],
    "user_data": {},
    "last_audio_hash": None,
    "show_teacher_form": False,
    "show_management_form": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur",
}


# =========================================================
# DEMO USERS
# =========================================================

MOCK_USERS = {
    "student@school.com": {
        "password": "student123",
        "role": "Student",
        "name": "Rahul Kumar",
    },
    "parent@school.com": {
        "password": "parent123",
        "role": "Parent",
        "name": "Rajesh Kumar",
    },
    "teacher@school.com": {
        "password": "teacher123",
        "role": "Teacher",
        "name": "Ms. Priya",
    },
    "principal@school.com": {
        "password": "principal123",
        "role": "Principal",
        "name": "Dr. Sharma",
    },
}


# =========================================================
# DEMO DATA
# =========================================================

ATTENDANCE_DATA = {
    "Rahul Kumar": {
        "present": 85,
        "absent": 8,
        "leave": 7,
        "percentage": 91.2,
    },
    "Arjun Kumar": {
        "present": 78,
        "absent": 12,
        "leave": 10,
        "percentage": 84.3,
    },
    "Priya Sharma": {
        "present": 92,
        "absent": 5,
        "leave": 3,
        "percentage": 97.1,
    },
}

GRADES_DATA = {
    "Rahul Kumar": {
        "Math": "A",
        "English": "B+",
        "Science": "A",
        "History": "B",
        "PE": "A",
    },
    "Arjun Kumar": {
        "Math": "B",
        "English": "B",
        "Science": "B+",
        "History": "A",
        "PE": "A",
    },
}


# =========================================================
# PRIVACY MESSAGES
# =========================================================

PRIVACY_ATTENDANCE = (
    "I'm sorry, but I can't provide another student's attendance "
    "or other private academic information. For privacy and security, "
    "students can only access their own academic records."
)

PRIVACY_GRADES = (
    "I'm sorry, but I can't provide another student's grades "
    "or other private academic information. For privacy and security, "
    "students can only access their own academic records."
)

PRIVACY_GENERAL = (
    "I'm sorry, but I can't provide another student's private "
    "academic information. Please ask about your own records."
)


# =========================================================
# HELPERS
# =========================================================

def current_student_name():
    return st.session_state.user_data.get("name", "Rahul Kumar")


def get_own_attendance():

    data = ATTENDANCE_DATA.get(
        current_student_name()
    )

    if not data:
        return "Your attendance information is currently unavailable."

    language = st.session_state.language

    if language == "Telugu":
        return (
            f"మీ హాజరు {data['percentage']:.1f}% ఉంది. "
            f"మీరు {data['present']} రోజులు హాజరయ్యారు, "
            f"{data['absent']} రోజులు గైర్హాజరయ్యారు, "
            f"{data['leave']} రోజులు సెలవులో ఉన్నారు."
        )

    elif language == "Hindi":
        return (
            f"आपकी उपस्थिति {data['percentage']:.1f}% है। "
            f"आप {data['present']} दिनों तक उपस्थित रहे, "
            f"{data['absent']} दिन अनुपस्थित रहे और "
            f"{data['leave']} दिन छुट्टी पर रहे।"
        )

    elif language == "Tamil":
        return (
            f"உங்கள் வருகைப் பதிவு {data['percentage']:.1f}% ஆகும். "
            f"நீங்கள் {data['present']} நாட்கள் வருகை தந்துள்ளீர்கள், "
            f"{data['absent']} நாட்கள் வரவில்லை, "
            f"{data['leave']} நாட்கள் விடுப்பில் இருந்தீர்கள்."
        )

    elif language == "Kannada":
        return (
            f"ನಿಮ್ಮ ಹಾಜರಾತಿ {data['percentage']:.1f}% ಇದೆ. "
            f"ನೀವು {data['present']} ದಿನಗಳು ಹಾಜರಾಗಿದ್ದೀರಿ, "
            f"{data['absent']} ದಿನಗಳು ಗೈರುಹಾಜರಾಗಿದ್ದೀರಿ ಮತ್ತು "
            f"{data['leave']} ದಿನಗಳು ರಜೆಯಲ್ಲಿದ್ದೀರಿ."
        )

    elif language == "Malayalam":
        return (
            f"നിങ്ങളുടെ ഹാജർ {data['percentage']:.1f}% ആണ്. "
            f"നിങ്ങൾ {data['present']} ദിവസം ഹാജരായി, "
            f"{data['absent']} ദിവസം ഹാജരായില്ല, "
            f"{data['leave']} ദിവസം അവധിയിലായിരുന്നു."
        )

    elif language == "Marathi":
        return (
            f"तुमची उपस्थिती {data['percentage']:.1f}% आहे. "
            f"तुम्ही {data['present']} दिवस उपस्थित होता, "
            f"{data['absent']} दिवस अनुपस्थित होता आणि "
            f"{data['leave']} दिवस रजेवर होता."
        )

    elif language == "Bengali":
        return (
            f"আপনার উপস্থিতি {data['percentage']:.1f}%। "
            f"আপনি {data['present']} দিন উপস্থিত ছিলেন, "
            f"{data['absent']} দিন অনুপস্থিত ছিলেন এবং "
            f"{data['leave']} দিন ছুটিতে ছিলেন।"
        )

    else:
        return (
            f"Your attendance is {data['percentage']:.1f}%. "
            f"You have been present for {data['present']} days, "
            f"absent for {data['absent']} days, and on leave for "
            f"{data['leave']} days."
        )

def get_own_grades():
    grades = GRADES_DATA.get(current_student_name())

    if not grades:
        return "Your grade information is currently unavailable."

    text = ", ".join(
        f"{subject}: {grade}"
        for subject, grade in grades.items()
    )
    return f"Your grades are: {text}."


def get_school_analytics():
    average = sum(
        x["percentage"] for x in ATTENDANCE_DATA.values()
    ) / len(ATTENDANCE_DATA)

    return (
        "School Attendance Overview:\n\n"
        f"- Students in demo records: {len(ATTENDANCE_DATA)}\n"
        f"- Average attendance: {average:.1f}%\n\n"
        "Individual student records are restricted to authorized staff."
    )


# =========================================================
# PRIVACY DETECTION
# =========================================================

def is_request_about_another_student(text):
    """
    Detect requests for another student's private academic data.
    Supports English, Hindi, Telugu, Tamil, Kannada, Malayalam,
    Marathi, Bengali, Gujarati, Punjabi, Urdu and common Hinglish/
    transliterated phrases.
    """

    text = text.lower().strip()

    current_name = current_student_name().lower()

    # =====================================================
    # 1. OTHER-PERSON / CLASSMATE WORDS
    # =====================================================

    other_person_patterns = [

        # ---------------- ENGLISH ----------------
        "classmate",
        "classmate's",
        "classmate’s",
        "another student",
        "other student",
        "another person",
        "other person",
        "someone else",
        "my friend",
        "my friend's",
        "my friend’s",
        "friend's attendance",
        "friend’s attendance",
        "his attendance",
        "her attendance",
        "their attendance",
        "his grades",
        "her grades",
        "their grades",

        # ---------------- HINGLISH ----------------
        "mere classmate",
        "meri classmate",
        "mere dost",
        "meri dost",
        "mere friend",
        "meri friend",
        "kisi aur ki",
        "kisi aur ka",
        "dusre student",
        "doosre student",
        "kisi aur student",
        "uski attendance",
        "uska attendance",
        "uske marks",
        "uske grades",

        # ---------------- TELUGU ----------------
        "క్లాస్‌మేట్",
        "క్లాస్మేట్",
        "క్లాస్ మేట్",
        "సహ విద్యార్థి",
        "సహవిద్యార్థి",
        "మరొక విద్యార్థి",
        "ఇతర విద్యార్థి",
        "ఇంకొక విద్యార్థి",
        "నా ఫ్రెండ్",
        "నా స్నేహితుడు",
        "నా స్నేహితురాలు",
        "వేరే విద్యార్థి",
        "అతని హాజరు",
        "ఆమె హాజరు",
        "వాళ్ళ హాజరు",
        "వారి హాజరు",

        # ---------------- TAMIL ----------------
        "வகுப்பு தோழர்",
        "வகுப்பு தோழி",
        "வகுப்புத் தோழர்",
        "வகுப்பு நண்பர்",
        "என் நண்பர்",
        "என் நண்பி",
        "மற்றொரு மாணவர்",
        "வேறு மாணவர்",
        "அவருடைய வருகை",
        "அவளுடைய வருகை",
        "அவர்களின் வருகை",

        # ---------------- KANNADA ----------------
        "ಕ್ಲಾಸ್‌ಮೇಟ್",
        "ಕ್ಲಾಸ್ಮೇಟ್",
        "ತರಗತಿ ಸಹಪಾಠಿ",
        "ಸಹಪಾಠಿ",
        "ನನ್ನ ಸ್ನೇಹಿತ",
        "ನನ್ನ ಸ್ನೇಹಿತೆ",
        "ಮತ್ತೊಬ್ಬ ವಿದ್ಯಾರ್ಥಿ",
        "ಬೇರೆ ವಿದ್ಯಾರ್ಥಿ",
        "ಅವನ ಹಾಜರಾತಿ",
        "ಅವಳ ಹಾಜರಾತಿ",
        "ಅವರ ಹಾಜರಾತಿ",

        # ---------------- MALAYALAM ----------------
        "ക്ലാസ്മേറ്റ്",
        "ക്ലാസ് മേറ്റ്",
        "സഹപാഠി",
        "മറ്റൊരു വിദ്യാർത്ഥി",
        "മറ്റേ വിദ്യാർത്ഥി",
        "എന്റെ സുഹൃത്ത്",
        "അവന്റെ ഹാജർ",
        "അവളുടെ ഹാജർ",
        "അവരുടെ ഹാജർ",

        # ---------------- MARATHI ----------------
        "वर्गमित्र",
        "वर्गमैत्रीण",
        "वर्गमित्राची",
        "माझा मित्र",
        "माझी मैत्रीण",
        "दुसरा विद्यार्थी",
        "दुसरी विद्यार्थिनी",
        "इतर विद्यार्थी",
        "त्याची उपस्थिती",
        "तिची उपस्थिती",
        "त्यांची उपस्थिती",

        # ---------------- BENGALI ----------------
        "সহপাঠী",
        "ক্লাসমেট",
        "আমার বন্ধু",
        "অন্য ছাত্র",
        "অন্য শিক্ষার্থী",
        "আরেকজন ছাত্র",
        "তার উপস্থিতি",
        "তাদের উপস্থিতি",

        # ---------------- GUJARATI ----------------
        "વર્ગમિત્ર",
        "ક્લાસમેટ",
        "મારો મિત્ર",
        "મારી મિત્ર",
        "બીજો વિદ્યાર્થી",
        "અન્ય વિદ્યાર્થી",
        "તેની હાજરી",
        "તેમની હાજરી",

        # ---------------- PUNJABI ----------------
        "ਕਲਾਸਮੇਟ",
        "ਸਹਿਪਾਠੀ",
        "ਮੇਰਾ ਦੋਸਤ",
        "ਮੇਰੀ ਦੋਸਤ",
        "ਦੂਜਾ ਵਿਦਿਆਰਥੀ",
        "ਹੋਰ ਵਿਦਿਆਰਥੀ",
        "ਉਸਦੀ ਹਾਜ਼ਰੀ",
        "ਉਨ੍ਹਾਂ ਦੀ ਹਾਜ਼ਰੀ",

        # ---------------- URDU ----------------
        "کلاس فیلو",
        "کلاس فیلو کی",
        "ہم جماعت",
        "میرا دوست",
        "میری دوست",
        "دوسرا طالب علم",
        "دوسری طالبہ",
        "کسی اور طالب علم",
        "اس کی حاضری",
        "ان کی حاضری",
    ]

    # =====================================================
    # 2. DIRECT MATCH
    # =====================================================

    for pattern in other_person_patterns:
        if pattern.lower() in text:
            return True

    # =====================================================
    # 3. CHECK OTHER STUDENT NAMES
    # =====================================================

    for student_name in ATTENDANCE_DATA.keys():

        lower_name = student_name.lower()

        # Don't treat logged-in student's own name as another student
        if lower_name == current_name:
            continue

        first_name = lower_name.split()[0]

        if lower_name in text:
            return True

        # Example:
        # "Arjun attendance"
        if len(first_name) >= 3 and first_name in text:
            return True

    # =====================================================
    # 4. THIRD-PERSON PRONOUNS + ACADEMIC DATA
    # =====================================================

    academic_words = [
        "attendance",
        "present",
        "absent",
        "leave",
        "grade",
        "grades",
        "mark",
        "marks",
        "score",
        "scores",
        "result",
        "results",
        "academic",
        "హాజరు",
        "అటెండెన్స్",
        "మార్కులు",
        "గ్రేడ్లు",
        "வருகை",
        "மதிப்பெண்",
        "ಹಾಜರಾತಿ",
        "ಅಂಕಗಳು",
        "ഹാജർ",
        "മാർക്ക്",
        "उपस्थिति",
        "अटेंडेंस",
        "गुण",
        "नंबर",
        "উপস্থিতি",
        "নম্বর",
        "હાજરી",
        "ગુણ",
        "ਹਾਜ਼ਰੀ",
        "نمبر",
        "حاضری",
    ]

    third_person_words = [

        # English
        "his",
        "her",
        "their",
        "him",
        "them",

        # Hinglish
        "uski",
        "uska",
        "uske",

        # Telugu
        "అతని",
        "ఆమె",
        "వారి",
        "వాళ్ళ",

        # Tamil
        "அவருடைய",
        "அவளுடைய",
        "அவர்களின்",

        # Kannada
        "ಅವನ",
        "ಅವಳ",
        "ಅವರ",

        # Malayalam
        "അവന്റെ",
        "അവളുടെ",
        "അവരുടെ",

        # Marathi
        "त्याचा",
        "तिचा",
        "त्यांची",

        # Bengali
        "তার",
        "তাদের",

        # Gujarati
        "તેની",
        "તેમની",

        # Punjabi
        "ਉਸਦੀ",
        "ਉਨ੍ਹਾਂ ਦੀ",

        # Urdu
        "اس کی",
        "ان کی",
    ]

    has_academic_word = any(
        word.lower() in text
        for word in academic_words
    )

    has_third_person = any(
        word.lower() in text
        for word in third_person_words
    )

    if has_academic_word and has_third_person:
        return True

    return False

def is_own_attendance_request(text):
    text = text.lower().strip()

    # English
    english_patterns = [
        "attendance",
        "my attendance",
        "what is my attendance",
        "how much attendance",
        "attendance percentage",
        "how is my attendance",
    ]

    # Hinglish
    hinglish_patterns = [
        "meri attendance",
        "mera attendance",
        "meri attendance kitni",
        "attendance kitni hai",
        "attendance kitna hai",
        "attendance kitni h",
        "meri attendance kya hai",
        "na attendance",
        "naa attendance",
        "na attendance entha",
        "na attendance entha undi",
    ]

    # Telugu script
    telugu_patterns = [
        "నా attendance",
        "నా అటెండెన్స్",
        "నా హాజరు",
        "అటెండెన్స్ ఎంత",
        "హాజరు ఎంత",
        "నా హాజరు ఎంత ఉంది",
        "నా అటెండెన్స్ ఎంత ఉంది",
    ]

    # If asking about another person, never treat it as own attendance
    if is_request_about_another_student(text):
        return False

    patterns = (
        english_patterns
        + hinglish_patterns
        + telugu_patterns
    )

    return any(
        pattern.lower() in text
        for pattern in patterns
    )

def is_own_grades_request(text):
    text = text.lower().strip()

    if not any(
        word in text
        for word in [
            "grade",
            "grades",
            "mark",
            "marks",
            "score",
            "scores",
            "result",
            "results",
        ]
    ):
        return False

    if is_request_about_another_student(text):
        return False

    own_words = ["my", "mine", "me", "myself", "i "]

    if any(word in text for word in own_words):
        return True

    return any(
        phrase in text
        for phrase in [
            "what are my grades",
            "show my grades",
            "my marks",
            "my score",
            "my result",
        ]
    )


# =========================================================
# GEMINI - NEW GOOGLE GENAI SDK
# =========================================================

def get_gemini_response(messages, language):
    if client is None:
        return (
            "Gemini is not configured. Please add GEMINI_API_KEY "
            "to your .env file or Streamlit secrets."
        )

    conversation = "\n".join(
        f"{m['role'].title()}: {m['content']}"
        for m in messages[-10:]
    )

    system_instruction = f"""
You are XYZ AI School Assistant.

The logged-in role is: {st.session_state.user_role}.
The user's preferred language is: {language}.

Privacy rules:
- Never reveal another student's private academic information
  to a student.
- Students can access only their own attendance and grades.
- If asked for a classmate's attendance, grades, marks, or other
  private records, politely refuse.
- Be professional, concise, clear, and helpful.
- Reply in {language}.
"""

    prompt = f"""
{system_instruction}

Conversation:
{conversation}

Answer the user's latest question.
"""

    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if response and getattr(response, "text", None):
                return response.text.strip()

        except Exception as e:
            last_error = e

    # Do not expose a long technical traceback to the user.
    return (
        "I'm sorry, but I'm unable to generate an AI response right now. "
        "Please try again in a moment."
    )


# =========================================================
# QUERY ROUTER
# =========================================================

def process_user_query(user_input):
    text = user_input.lower().strip()
    role = st.session_state.user_role

    # -----------------------------------------------------
    # STUDENT PRIVACY FIRST
    # -----------------------------------------------------

    if role == "Student":
        if is_request_about_another_student(text):
            if any(
                word in text
                for word in [
                    "attendance",
                    "present",
                    "absent",
                    "leave",
                ]
            ):
                return PRIVACY_ATTENDANCE

            if any(
                word in text
                for word in [
                    "grade",
                    "grades",
                    "mark",
                    "marks",
                    "score",
                    "result",
                ]
            ):
                return PRIVACY_GRADES

            return PRIVACY_GENERAL

        if is_own_attendance_request(text):
            return get_own_attendance()

        if is_own_grades_request(text):
            return get_own_grades()

    # -----------------------------------------------------
    # STAFF
    # -----------------------------------------------------

    if role in ["Teacher", "Principal"]:
        if (
            "school attendance" in text
            or "overall attendance" in text
            or "school analytics" in text
            or text == "analytics"
        ):
            return get_school_analytics()

    # -----------------------------------------------------
    # PARENT
    # -----------------------------------------------------

    if role == "Parent":
        if "attendance" in text and not is_request_about_another_student(text):
            return get_own_attendance()

        if any(
            word in text
            for word in ["grade", "grades", "mark", "marks", "score", "result"]
        ):
            return get_own_grades()

    return get_gemini_response(
        st.session_state.messages,
        st.session_state.language,
    )


# =========================================================
# TEXT TO SPEECH
# =========================================================

def text_to_speech(text, language):
    try:
        tts = gTTS(
            text=text,
            lang=LANGUAGES.get(language, "en"),
            slow=False,
        )

        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)

        return buffer.read()

    except Exception:
        return None


# =========================================================
# SPEECH TO TEXT
# =========================================================

def speech_to_text(audio_bytes, language):
    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        return recognizer.recognize_google(
            audio_data,
            language=LANGUAGES.get(language, "en"),
        )

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

    except Exception:
        return ""


# =========================================================
# PROCESS MESSAGE
# =========================================================

def process_message(user_input):
    timestamp = datetime.now().strftime("%H:%M")

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "timestamp": timestamp,
        }
    )

    with st.spinner("🤔 Thinking..."):
        answer = process_user_query(user_input)

    audio = text_to_speech(
        answer,
        st.session_state.language,
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "timestamp": datetime.now().strftime("%H:%M"),
            "audio": audio,
        }
    )


# =========================================================
# LOGIN
# =========================================================

def show_auth_page():

    st.markdown(
        """
<div class="login-card">
    <div class="login-icon">🤖</div>
    <div class="login-title">Welcome to XYZ AI</div>
    <div class="login-subtitle">Sign in to your school assistant</div>
</div>
""",
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.selectbox(
            "Select Your Role",
            ["Student", "Parent", "Teacher", "Principal"],
            key="login_role",
        )

        email = st.text_input(
            "User ID or Email",
            placeholder="Enter your school email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "🔓 Sign In",
                use_container_width=True,
                key="signin_button",
            ):
                user = MOCK_USERS.get(email)

                if user and user["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_role = user["role"]
                    st.session_state.user_email = email
                    st.session_state.user_data = user
                    st.session_state.messages = []
                    st.session_state.last_audio_hash = None
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")

        with c2:
            if st.button(
                "📄 Demo Mode",
                use_container_width=True,
                key="demo_button",
            ):
                user = MOCK_USERS["student@school.com"]

                st.session_state.authenticated = True
                st.session_state.user_role = user["role"]
                st.session_state.user_email = "student@school.com"
                st.session_state.user_data = user
                st.session_state.messages = []
                st.session_state.last_audio_hash = None

                st.rerun()


# =========================================================
# HEADER
# =========================================================

def show_header():

    left, right = st.columns([4, 1.5])

    with left:
        name = st.session_state.user_data.get("name", "User")
        role = st.session_state.user_role or "Student"

        st.markdown(
            f"""
<div class="app-title">🤖 XYZ AI School Assistant</div>
<span class="badge">{name}</span>
<span class="badge">{role}</span>
""",
            unsafe_allow_html=True,
        )

    with right:
        language = st.selectbox(
            "Select Language",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(
                st.session_state.language
            ),
            key="language_selector",
        )

        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()


# =========================================================
# DISPLAY CHAT
# =========================================================

def display_messages():

    for message in st.session_state.messages:

        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
                st.caption(message.get("timestamp", ""))

        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])
                st.caption(message.get("timestamp", ""))

                if message.get("audio"):
                    st.audio(
                        message["audio"],
                        format="audio/mp3",
                    )


# =========================================================
# TEXT INPUT
# =========================================================

def submit_text_from_form():

    value = st.session_state.get(
        "chat_form_text",
        "",
    ).strip()

    if not value:
        return

    process_message(value)


def show_text_input():

    # Form submission supports Enter.
    # clear_on_submit removes the typed text immediately
    # after the answer is submitted.
    with st.form(
        "chat_text_form",
        clear_on_submit=True,
        border=False,
    ):

        col_text, col_send = st.columns([8, 1])

        with col_text:
            st.text_input(
                "Message",
                placeholder=(
                    "Ask me anything about attendance, "
                    "grades, or school..."
                ),
                label_visibility="collapsed",
                key="chat_form_text",
            )

        with col_send:
            submitted = st.form_submit_button(
                "➤",
                use_container_width=True,
            )

    if submitted:
        value = st.session_state.get(
            "chat_form_text",
            "",
        ).strip()

        if value:
            process_message(value)
            st.rerun()


# =========================================================
# VOICE INPUT
# =========================================================

def show_voice_input():

    audio_value = st.audio_input(
        "🎙️",
        key="voice_input",
    )

    if audio_value is None:
        return

    audio_bytes = audio_value.getvalue()

    if not audio_bytes:
        return

    audio_hash = hashlib.md5(
        audio_bytes
    ).hexdigest()

    if audio_hash == st.session_state.last_audio_hash:
        return

    st.session_state.last_audio_hash = audio_hash

    with st.spinner("🎙️ Converting your voice to text..."):
        spoken_text = speech_to_text(
            audio_bytes,
            st.session_state.language,
        )

    if spoken_text:
        process_message(spoken_text)
        st.rerun()
    else:
        st.warning(
            "I couldn't understand the recording. "
            "Please try again."
        )


# =========================================================
# INPUT AREA
# =========================================================

def show_input_area():

    col_text, col_voice = st.columns([8, 2])

    with col_text:
        show_text_input()

    with col_voice:
        show_voice_input()


# =========================================================
# ESCALATION
# =========================================================

def show_escalation():

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button(
            "📞 Talk to Teacher",
            use_container_width=True,
            key="teacher_button",
        ):
            st.session_state.show_teacher_form = True

    with c2:
        if st.button(
            "📋 Contact Management",
            use_container_width=True,
            key="management_button",
        ):
            st.session_state.show_management_form = True

    if st.session_state.show_teacher_form:
        with st.form("teacher_form"):
            message = st.text_area(
                "What would you like to discuss with your teacher?",
                height=80,
            )

            submitted = st.form_submit_button(
                "Send Request"
            )

            if submitted and message.strip():
                st.success(
                    "✓ Your request has been submitted to the teacher."
                )
                st.session_state.show_teacher_form = False

    if st.session_state.show_management_form:
        with st.form("management_form"):
            concern = st.text_area(
                "Describe your concern",
                height=80,
            )

            submitted = st.form_submit_button(
                "Submit to Management"
            )

            if submitted and concern.strip():
                st.success(
                    "✓ Your concern has been submitted to School Management."
                )
                st.session_state.show_management_form = False


# =========================================================
# MAIN CHAT
# =========================================================

def show_chat_interface():

    show_header()

    st.divider()

    display_messages()

    show_input_area()

    show_escalation()

    st.markdown("<br>", unsafe_allow_html=True)

    # Logout remains at bottom-left.
    logout_col, _ = st.columns([1.2, 4])

    with logout_col:
        if st.button(
            "🚪 Sign Out",
            use_container_width=True,
            key="bottom_logout",
        ):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_email = None
            st.session_state.user_data = {}
            st.session_state.messages = []
            st.session_state.last_audio_hash = None
            st.rerun()


# =========================================================
# MAIN
# =========================================================

def main():

    if st.session_state.authenticated:
        show_chat_interface()
    else:
        show_auth_page()


if __name__ == "__main__":
    main()