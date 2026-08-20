"""
Utility functions for XYZ AI School Assistant
"""
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class RoleManager:
    """Manages role-based permissions and access control"""
    
    PERMISSIONS = {
        'Student': {
            'view_own_attendance': True,
            'view_own_grades': True,
            'view_class_info': True,
            'view_other_attendance': False,
            'mark_attendance': False,
            'manage_grades': False,
            'view_school_analytics': False,
            'manage_users': False,
        },
        'Parent': {
            'view_own_attendance': False,
            'view_own_grades': False,
            'view_class_info': True,
            'view_other_attendance': True,  # Own children
            'mark_attendance': False,
            'manage_grades': False,
            'view_school_analytics': False,
            'manage_users': False,
        },
        'Teacher': {
            'view_own_attendance': True,
            'view_own_grades': True,
            'view_class_info': True,
            'view_other_attendance': True,  # Own class
            'mark_attendance': True,
            'manage_grades': True,
            'view_school_analytics': False,
            'manage_users': False,
        },
        'Principal': {
            'view_own_attendance': True,
            'view_own_grades': True,
            'view_class_info': True,
            'view_other_attendance': True,  # All
            'mark_attendance': False,
            'manage_grades': False,
            'view_school_analytics': True,
            'manage_users': True,
        }
    }
    
    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        """Check if role has specific permission"""
        if role not in RoleManager.PERMISSIONS:
            return False
        return RoleManager.PERMISSIONS[role].get(permission, False)
    
    @staticmethod
    def get_role_permissions(role: str) -> Dict[str, bool]:
        """Get all permissions for a role"""
        return RoleManager.PERMISSIONS.get(role, {})


class IntentDetector:
    """Detects user intent from natural language"""
    
    INTENTS = {
        'attendance': ['attendance', 'present', 'absent', 'leave', 'absence', 'days'],
        'grades': ['grade', 'mark', 'score', 'marks', 'subject', 'result', 'performance'],
        'schedule': ['schedule', 'timetable', 'class', 'period', 'time', 'timing'],
        'fees': ['fee', 'payment', 'dues', 'fine', 'charges'],
        'activity': ['activity', 'event', 'sports', 'club', 'program', 'competition'],
        'escalate': ['talk to', 'call', 'teacher', 'management', 'principal', 'contact'],
        'help': ['help', 'issue', 'problem', 'error', 'support', 'assistance'],
    }
    
    @staticmethod
    def detect_intent(user_input: str) -> List[str]:
        """Detect intents from user input"""
        user_input_lower = user_input.lower()
        detected_intents = []
        
        for intent, keywords in IntentDetector.INTENTS.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    detected_intents.append(intent)
                    break
        
        return detected_intents if detected_intents else ['general']
    
    @staticmethod
    def extract_entity(user_input: str, entity_type: str) -> str:
        """Extract specific entity from user input"""
        patterns = {
            'student_name': r'\b([A-Z][a-z]+)\b',
            'date': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            'number': r'\d+',
        }
        
        pattern = patterns.get(entity_type)
        if pattern:
            matches = re.findall(pattern, user_input)
            return matches[0] if matches else None
        return None


class LanguageManager:
    """Manages language-specific operations"""
    
    LANGUAGE_CODES = {
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
        'Urdu': 'ur'
    }
    
    LANGUAGE_PROMPTS = {
        'hi': "कृपया हिंदी में जवाब दें।",
        'ta': "தமிழில் பதிலளிக்க வேண்டுகிறது।",
        'te': "తెలుగులో సమాధానం ఇవ్వండి।",
        'mr': "कृपया मराठीत उत्तर द्या।",
        'bn': "অনুগ্রহ করে বাংলায় উত্তর দিন।",
        'gu': "કૃપયા ગુજરાતીમાં જવાબ આપો।",
        'pa': "ਕਿਰਪਾ ਕਰਕੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।",
        'kn': "ದಯವಿಟ್ಟು ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರ ಕೊಡಿ।",
        'ml': "കൃപയാ മലയാളത്തിൽ ഉത്തരം നൽകുക.",
        'ur': "براہ کرم اردو میں جواب دیں۔"
    }
    
    @staticmethod
    def get_language_code(language: str) -> str:
        """Get ISO language code"""
        return LanguageManager.LANGUAGE_CODES.get(language, 'en')
    
    @staticmethod
    def get_language_instruction(language: str) -> str:
        """Get language-specific instruction for AI"""
        code = LanguageManager.get_language_code(language)
        return LanguageManager.LANGUAGE_PROMPTS.get(code, "")


class SecurityManager:
    """Manages security and validation"""
    
    DANGEROUS_PATTERNS = [
        r'system\s*prompt',
        r'api\s*key',
        r'password',
        r'secret',
        r'admin',
        r'bypass',
        r'inject',
        r'execute',
        r'eval',
    ]
    
    @staticmethod
    def is_safe_input(user_input: str) -> bool:
        """Check if user input is safe"""
        user_input_lower = user_input.lower()
        
        for pattern in SecurityManager.DANGEROUS_PATTERNS:
            if re.search(pattern, user_input_lower):
                return False
        
        if len(user_input) > 5000:
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Sanitize user input"""
        # Remove special characters but keep normal text
        user_input = re.sub(r'[<>"]', '', user_input)
        user_input = user_input.strip()
        return user_input
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class ConversationManager:
    """Manages conversation history"""
    
    @staticmethod
    def format_conversation(messages: List[Dict]) -> str:
        """Format conversation history for AI context"""
        formatted = []
        for msg in messages[-10:]:  # Last 10 messages
            role = msg.get('role', '').title()
            content = msg.get('content', '')
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def summarize_conversation(messages: List[Dict]) -> str:
        """Summarize key points from conversation"""
        if not messages:
            return "No conversation history"
        
        summary = {
            'total_messages': len(messages),
            'user_queries': sum(1 for m in messages if m['role'] == 'user'),
            'first_message': messages[0].get('timestamp', 'N/A'),
            'last_message': messages[-1].get('timestamp', 'N/A'),
        }
        
        return json.dumps(summary, indent=2)
    
    @staticmethod
    def get_conversation_context(messages: List[Dict]) -> str:
        """Extract context from conversation"""
        intents = []
        for msg in messages:
            if msg['role'] == 'user':
                detected = IntentDetector.detect_intent(msg['content'])
                intents.extend(detected)
        
        unique_intents = list(set(intents))
        return f"Conversation topics: {', '.join(unique_intents)}"


class MockAPIHandler:
    """Handles mock API calls and data operations"""
    
    def __init__(self):
        self.attendance_db = self._init_attendance_db()
        self.grades_db = self._init_grades_db()
    
    def _init_attendance_db(self) -> Dict:
        """Initialize mock attendance database"""
        return {
            'Rahul': {'present': 85, 'absent': 8, 'leave': 7, 'percentage': 91.2},
            'Arjun': {'present': 78, 'absent': 12, 'leave': 10, 'percentage': 84.3},
            'Priya': {'present': 92, 'absent': 5, 'leave': 3, 'percentage': 97.1},
        }
    
    def _init_grades_db(self) -> Dict:
        """Initialize mock grades database"""
        return {
            'Rahul': {'Math': 'A', 'English': 'B+', 'Science': 'A', 'History': 'B', 'PE': 'A'},
            'Arjun': {'Math': 'B', 'English': 'B', 'Science': 'B+', 'History': 'A', 'PE': 'A'},
        }
    
    def get_attendance(self, student_name: str) -> Dict:
        """Get student attendance"""
        return self.attendance_db.get(student_name)
    
    def get_grades(self, student_name: str) -> Dict:
        """Get student grades"""
        return self.grades_db.get(student_name)
    
    def mark_attendance(self, student_name: str, status: str) -> bool:
        """Mark attendance for student"""
        if student_name not in self.attendance_db:
            return False
        
        if status.lower() == 'present':
            self.attendance_db[student_name]['present'] += 1
        elif status.lower() == 'absent':
            self.attendance_db[student_name]['absent'] += 1
        elif status.lower() == 'leave':
            self.attendance_db[student_name]['leave'] += 1
        else:
            return False
        
        # Recalculate percentage
        total = sum([
            self.attendance_db[student_name]['present'],
            self.attendance_db[student_name]['absent'],
            self.attendance_db[student_name]['leave']
        ])
        
        self.attendance_db[student_name]['percentage'] = (
            self.attendance_db[student_name]['present'] / total * 100
        )
        
        return True
    
    def get_school_analytics(self) -> Dict:
        """Get school-wide analytics"""
        students = list(self.attendance_db.keys())
        avg_attendance = sum([
            data['percentage'] for data in self.attendance_db.values()
        ]) / len(self.attendance_db)
        
        return {
            'total_students': len(students),
            'average_attendance': avg_attendance,
            'students_above_90': sum(1 for data in self.attendance_db.values() if data['percentage'] >= 90),
            'students_below_75': sum(1 for data in self.attendance_db.values() if data['percentage'] < 75),
        }


# Logging utility
class Logger:
    """Simple logging utility"""
    
    @staticmethod
    def log(level: str, message: str, data: Dict = None) -> str:
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        
        if data:
            log_msg += f" | Data: {json.dumps(data)}"
        
        return log_msg
