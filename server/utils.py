"""
Utility functions for server operations
"""
import logging
import os
from datetime import datetime
from typing import Tuple


def setup_logging():
    """Configure logging for the application"""
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = os.path.join(logs_dir, f"quiz_server_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def validate_quiz_data(quiz_data: dict) -> Tuple[bool, str]:
    """
    Validate quiz data structure
    
    Returns:
        (is_valid, error_message)
    """
    required_fields = ['name', 'title', 'questions']
    
    for field in required_fields:
        if field not in quiz_data:
            return False, f"Missing required field: {field}"
    
    if not isinstance(quiz_data['questions'], list):
        return False, "Questions must be a list"
    
    if len(quiz_data['questions']) == 0:
        return False, "Quiz must have at least one question"
    
    # Validate each question
    for i, question in enumerate(quiz_data['questions']):
        if 'type' not in question:
            return False, f"Question {i+1} missing type"
        
        if 'text' not in question or not question['text'].strip():
            return False, f"Question {i+1} missing text"
        
        q_type = question['type']
        
        if q_type in ['multiple_choice_single', 'multiple_choice_multiple']:
            if 'options' not in question or len(question.get('options', [])) < 2:
                return False, f"Question {i+1}: Multiple choice needs at least 2 options"
        
        if 'weight' in question:
            try:
                float(question['weight'])
            except (ValueError, TypeError):
                return False, f"Question {i+1}: Weight must be a number"
    
    return True, ""


def graceful_shutdown(server_thread=None, ngrok_url=None):
    """Gracefully shutdown server and cleanup resources"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("Initiating graceful shutdown...")
    
    # Stop ngrok
    if ngrok_url:
        try:
            from pyngrok import ngrok
            ngrok.kill()
            logger.info("Ngrok tunnel closed")
        except Exception as e:
            logger.error(f"Error closing ngrok: {e}")
    
    logger.info("Shutdown complete")

