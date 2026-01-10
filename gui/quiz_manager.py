"""
Quiz Manager - Handles quiz CRUD operations and data persistence
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class QuizManager:
    """Manages quiz storage and retrieval"""
    
    DATA_DIR = "data"
    
    def __init__(self):
        """Initialize quiz manager with data directory"""
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
    
    def list_quizzes(self) -> List[str]:
        """Get list of all quiz filenames"""
        if not os.path.exists(self.DATA_DIR):
            return []
        return [f.replace('.json', '') for f in os.listdir(self.DATA_DIR) 
                if f.endswith('.json')]
    
    def load_quiz(self, quiz_name: str) -> Optional[Dict]:
        """Load a quiz by name"""
        filepath = os.path.join(self.DATA_DIR, f"{quiz_name}.json")
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading quiz {quiz_name}: {e}")
            return None
    
    def save_quiz(self, quiz_data: Dict) -> bool:
        """Save a quiz to disk"""
        quiz_name = quiz_data.get('name', 'unnamed_quiz')
        filepath = os.path.join(self.DATA_DIR, f"{quiz_name}.json")
        try:
            # Add metadata
            quiz_data['last_modified'] = datetime.now().isoformat()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return False
    
    def delete_quiz(self, quiz_name: str) -> bool:
        """Delete a quiz file"""
        filepath = os.path.join(self.DATA_DIR, f"{quiz_name}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                print(f"Error deleting quiz: {e}")
                return False
        return False
    
    def get_default_quiz(self) -> Dict:
        """Return a default empty quiz structure"""
        return {
            'name': 'New Quiz',
            'title': 'Untitled Quiz',
            'require_full_name': True,
            'timer_minutes': 30,
            'start_message': 'Welcome! Please read all questions carefully. Good luck!',
            'end_message': 'Thank you for completing the quiz!',
            'shuffle_questions': False,
            'questions': []
        }

