"""
Flask server for quiz administration and student interface
"""
from flask import Flask, render_template, request, jsonify, session
import os
import json
from datetime import datetime, timedelta
import hashlib
import random
import logging

# Setup logging first
try:
    from server.utils import setup_logging, validate_quiz_data
    logger = setup_logging()
except ImportError:
    # Fallback if utils not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    def validate_quiz_data(data):
        return True, ""

# Get the directory where this file is located (server/)
# and go up one level to get the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Export for testing/debugging (using cleaner names)
project_root = BASE_DIR
template_dir = TEMPLATE_DIR
static_dir = STATIC_DIR

# Verify directories exist and log
logger.info(f"Base directory: {BASE_DIR}")
logger.info(f"Template directory: {TEMPLATE_DIR}")
logger.info(f"Static directory: {STATIC_DIR}")

if not os.path.exists(TEMPLATE_DIR):
    # Fallback: try current working directory
    if os.path.exists('templates'):
        TEMPLATE_DIR = os.path.abspath('templates')
        logger.info(f"Using fallback template directory: {TEMPLATE_DIR}")
    else:
        error_msg = f"Templates directory not found. Expected: {TEMPLATE_DIR}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

if not os.path.exists(STATIC_DIR):
    # Fallback: try current working directory
    if os.path.exists('static'):
        STATIC_DIR = os.path.abspath('static')
        logger.info(f"Using fallback static directory: {STATIC_DIR}")
    else:
        logger.warning(f"Static directory not found. Expected: {STATIC_DIR}")

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)
app.secret_key = os.urandom(24)  # Generate random secret key
logger.info("Flask app initialized with template and static folders")

# Global quiz data (loaded when quiz is launched)
CURRENT_QUIZ = None
QUIZ_START_TIME = None
ACTIVE_SESSIONS = {}  # Track active sessions to prevent resubmission


def load_quiz(quiz_name: str):
    """Load quiz data from file"""
    global CURRENT_QUIZ, QUIZ_START_TIME, ACTIVE_SESSIONS
    
    # Clear previous quiz data and sessions
    CURRENT_QUIZ = None
    QUIZ_START_TIME = None
    ACTIVE_SESSIONS = {}
    
    quiz_path = os.path.join('data', f"{quiz_name}.json")
    
    if not os.path.exists(quiz_path):
        logger.error(f"Quiz file not found: {quiz_path}")
        return False
    
    try:
        with open(quiz_path, 'r', encoding='utf-8') as f:
            CURRENT_QUIZ = json.load(f)
        
        # Validate quiz data
        is_valid, error_msg = validate_quiz_data(CURRENT_QUIZ)
        if not is_valid:
            logger.error(f"Invalid quiz data: {error_msg}")
            return False
        
        # Shuffle questions if requested
        if CURRENT_QUIZ.get('shuffle_questions', False) and 'questions' in CURRENT_QUIZ:
            random.shuffle(CURRENT_QUIZ['questions'])
        
        QUIZ_START_TIME = datetime.now()
        logger.info(f"Quiz loaded successfully: {quiz_name}")
        logger.info(f"Quiz title: {CURRENT_QUIZ.get('title', 'N/A')}")
        logger.info(f"Number of questions: {len(CURRENT_QUIZ.get('questions', []))}")
        return True
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in quiz file: {e}")
        return False
    except Exception as e:
        logger.error(f"Error loading quiz: {e}", exc_info=True)
        return False


def generate_session_id():
    """Generate unique session ID"""
    return hashlib.md5(f"{datetime.now()}{os.urandom(16)}".encode()).hexdigest()


def calculate_score(answers: dict, quiz_data: dict) -> dict:
    """Calculate quiz score based on answers"""
    total_points = 0
    earned_points = 0
    question_results = []
    
    logger.info(f"Starting score calculation. Total questions: {len(quiz_data.get('questions', []))}")
    logger.info(f"Received answers: {answers}")
    
    for i, question in enumerate(quiz_data.get('questions', [])):
        question_id = str(i)
        weight = question.get('weight', 1)
        total_points += weight
        
        if question_id not in answers:
            question_results.append({
                'question_num': i + 1,
                'correct': False,
                'points_earned': 0,
                'points_possible': weight,
                'type': question.get('type', 'unknown')
            })
            continue
        
        user_answer = answers[question_id]
        correct_answer = question.get('correct_answer', '')
        q_type = question.get('type', '')
        is_correct = False
        points_earned = 0
        
        # Debug logging
        logger.debug(f"Q{i+1}: type={q_type}, user={user_answer}, correct={correct_answer}")
        
        if q_type == 'multiple_choice_single':
            # Exact match - strip whitespace only, preserve case for Arabic/special chars
            if str(user_answer).strip() == str(correct_answer).strip():
                is_correct = True
                points_earned = weight
                logger.debug(f"Q{i+1}: CORRECT match!")
            else:
                logger.debug(f"Q{i+1}: INCORRECT - '{str(user_answer).strip()}' != '{str(correct_answer).strip()}'")
        elif q_type == 'multiple_choice_multiple':
            if isinstance(correct_answer, list):
                # Exact match - strip whitespace only, preserve case
                user_ans_set = set([str(a).strip() for a in user_answer]) if isinstance(user_answer, list) else set()
                correct_ans_set = set([str(a).strip() for a in correct_answer])
                if user_ans_set == correct_ans_set:
                    is_correct = True
                    points_earned = weight
        elif q_type == 'true_false':
            # Exact match - strip whitespace only, preserve case
            if str(user_answer).strip() == str(correct_answer).strip():
                is_correct = True
                points_earned = weight
                logger.debug(f"Q{i+1}: CORRECT match!")
            else:
                logger.debug(f"Q{i+1}: INCORRECT - '{str(user_answer).strip()}' != '{str(correct_answer).strip()}'")
        elif q_type in ['short_answer', 'paragraph']:
            if correct_answer:  # Only auto-grade if correct answer is provided
                # Exact match - strip whitespace only, preserve case for Arabic
                if str(user_answer).strip() == str(correct_answer).strip():
                    is_correct = True
                    points_earned = weight
            else:
                # Manual grading needed
                is_correct = None
                points_earned = 0
        
        earned_points += points_earned
        question_results.append({
            'question_num': i + 1,
            'correct': is_correct,
            'points_earned': points_earned,
            'points_possible': weight,
            'type': q_type,
            'user_answer': user_answer
        })
    
    percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    
    return {
        'total_points': total_points,
        'earned_points': earned_points,
        'percentage': round(percentage, 2),
        'question_results': question_results
    }


@app.route('/')
def index():
    """Serve the quiz interface"""
    if not CURRENT_QUIZ:
        return render_template('error.html', message="No quiz is currently active. Please contact your instructor."), 404
    
    # Always generate a new session ID for each page load
    # This ensures each student gets their own independent session
    session_id = generate_session_id()
    session['session_id'] = session_id
    session.permanent = False  # Session expires when browser closes
    
    # Initialize new session
    ACTIVE_SESSIONS[session_id] = {
        'started': datetime.now(),
        'submitted': False,
        'student_name': None
    }
    
    quiz_display = {
        'title': CURRENT_QUIZ.get('title', 'Quiz'),
        'start_message': CURRENT_QUIZ.get('start_message', ''),
        'timer_minutes': CURRENT_QUIZ.get('timer_minutes', 30),
        'require_full_name': CURRENT_QUIZ.get('require_full_name', True),
        'questions': CURRENT_QUIZ.get('questions', []),
        'session_id': session_id,
        'start_time': datetime.now().isoformat()  # Each student gets their own start time
    }
    
    return render_template('index.html', quiz=quiz_display)


@app.route('/api/quiz_data')
def get_quiz_data():
    """API endpoint to get quiz data"""
    if not CURRENT_QUIZ:
        return jsonify({'error': 'No quiz active'}), 404
    
    session_id = session.get('session_id')
    if not session_id or session_id not in ACTIVE_SESSIONS:
        return jsonify({'error': 'Invalid session'}), 403
    
    if ACTIVE_SESSIONS.get(session_id, {}).get('submitted', False):
        return jsonify({'error': 'Already submitted'}), 403
    
    # Calculate time remaining based on THIS student's start time
    session_data = ACTIVE_SESSIONS.get(session_id, {})
    session_start = session_data.get('started', datetime.now())
    elapsed = (datetime.now() - session_start).total_seconds()
    timer_minutes = CURRENT_QUIZ.get('timer_minutes', 30)
    time_remaining = max(0, (timer_minutes * 60) - elapsed)
    
    return jsonify({
        'timer_minutes': timer_minutes,
        'time_remaining_seconds': int(time_remaining),
        'start_time': session_start.isoformat()
    })


@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    """Handle quiz submission"""
    if not CURRENT_QUIZ:
        logger.warning("Submit attempted with no active quiz")
        return jsonify({'error': 'No quiz active'}), 404
    
    session_id = session.get('session_id')
    if not session_id:
        logger.warning("Submit attempted without session ID")
        return jsonify({'error': 'No session ID'}), 403
    
    # Check if already submitted
    if ACTIVE_SESSIONS.get(session_id, {}).get('submitted', False):
        logger.warning(f"Resubmission attempted for session: {session_id}")
        return jsonify({'error': 'Already submitted'}), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        student_name = data.get('student_name', '').strip()
        
        # Validate name if required
        if CURRENT_QUIZ.get('require_full_name', True) and not student_name:
            logger.warning(f"Submission attempted without name for session: {session_id}")
            return jsonify({'error': 'Full name is required'}), 400
        
        answers = data.get('answers', {})
        
        # Calculate score
        score_result = calculate_score(answers, CURRENT_QUIZ)
        
        # Mark session as submitted
        ACTIVE_SESSIONS[session_id]['submitted'] = True
        ACTIVE_SESSIONS[session_id]['submitted_at'] = datetime.now()
        
        # Save results
        try:
            save_results(student_name, answers, score_result, session_id)
            logger.info(f"Quiz submitted successfully: {student_name} (Session: {session_id})")
        except Exception as e:
            logger.error(f"Error saving results: {e}", exc_info=True)
            # Continue even if save fails - user has submitted
        
        return jsonify({
            'success': True,
            'message': CURRENT_QUIZ.get('end_message', 'Thank you for completing the quiz!')
        })
    except Exception as e:
        logger.error(f"Error processing submission: {e}", exc_info=True)
        return jsonify({'error': 'Server error processing submission'}), 500


def save_results(student_name: str, answers: dict, score_result: dict, session_id: str):
    """Save quiz results to files"""
    quiz_name = CURRENT_QUIZ.get('name', 'unknown_quiz')
    results_dir = os.path.join('results', quiz_name)
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Sanitize filename
    safe_name = "".join(c for c in student_name if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
    if not safe_name:
        safe_name = 'Student'
    
    # Prepare result data
    result_data = {
        'quiz_name': quiz_name,
        'quiz_title': CURRENT_QUIZ.get('title', ''),
        'student_name': student_name,
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'score': score_result,
        'answers': answers,
        'questions': CURRENT_QUIZ.get('questions', [])
    }
    
    # Save JSON
    json_filename = f"{safe_name}_{timestamp}.json"
    json_path = os.path.join(results_dir, json_filename)
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to JSON: {json_path}")
    except Exception as e:
        logger.error(f"Error saving JSON results: {e}", exc_info=True)
        raise
    
    # Save CSV
    csv_path = os.path.join(results_dir, f"{quiz_name}_results.csv")
    import csv
    
    try:
        # Check if CSV exists and write header if new
        file_exists = os.path.exists(csv_path)
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                # Write header
                header = ['Timestamp', 'Student Name', 'Session ID', 'Total Points', 
                         'Earned Points', 'Percentage']
                # Add question columns
                for i in range(len(CURRENT_QUIZ.get('questions', []))):
                    header.extend([f'Q{i+1}_Answer', f'Q{i+1}_Correct', f'Q{i+1}_Points'])
                writer.writerow(header)
            
            # Write data row
            row = [
                result_data['timestamp'],
                student_name,
                session_id,
                score_result['total_points'],
                score_result['earned_points'],
                score_result['percentage']
            ]
            
            # Add question answers
            for q_result in score_result['question_results']:
                q_idx = str(q_result['question_num'] - 1)
                user_ans = answers.get(q_idx, '')
                if isinstance(user_ans, list):
                    user_ans = '; '.join(str(a) for a in user_ans)
                row.extend([
                    str(user_ans),
                    str(q_result['correct']) if q_result['correct'] is not None else 'Manual',
                    f"{q_result['points_earned']}/{q_result['points_possible']}"
                ])
            
            writer.writerow(row)
        logger.info(f"Results appended to CSV: {csv_path}")
    except Exception as e:
        logger.error(f"Error saving CSV results: {e}", exc_info=True)
        raise


def create_app(quiz_name: str):
    """Create Flask app with loaded quiz"""
    if not load_quiz(quiz_name):
        raise ValueError(f"Failed to load quiz: {quiz_name}")
    return app


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        quiz_name = sys.argv[1].replace('.json', '')
        create_app(quiz_name)
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    else:
        print("Usage: python app.py <quiz_name>")

