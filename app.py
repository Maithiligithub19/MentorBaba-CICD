from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pandas as pd
from functools import wraps
import openpyxl
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    import os
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'quizapp'),
            password=os.getenv('DB_PASSWORD', 'password123'),
            database=os.getenv('DB_NAME', 'quiz_app2'),
            autocommit=False,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if not session.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- Static Files ---
@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/<filename>')
def serve_html(filename):
    if filename.endswith('.html'):
        return send_from_directory('templates', filename)
    return send_from_directory('static', filename)

# --- Authentication APIs ---
@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        hashed_password = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users1 (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return jsonify({'error': 'Email already registered'}), 409
        return jsonify({'error': f'Database error: {str(err)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users1 WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['is_admin'] = bool(user.get('is_admin', False))
            return jsonify({
                'message': 'Login successful', 
                'user': {
                    'id': user['id'], 
                    'email': user['email'],
                    'is_admin': session['is_admin']
                }
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/user', methods=['GET'])
@login_required
def api_get_user():
    return jsonify({
        'user': {
            'id': session['user_id'], 
            'email': session['email'],
            'is_admin': session.get('is_admin', False)
        }
    }), 200

# --- Question Management APIs ---
@app.route('/api/upload', methods=['POST'])
@admin_required
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    try:
        df = pd.read_excel(file, engine='openpyxl')
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM answers1")
        cursor.execute("DELETE FROM questions1")
        
        for index, row in df.iterrows():
            cursor.execute(
                "INSERT INTO questions1 (question, option_a, option_b, option_c, option_d, correct_ans) VALUES (%s,%s,%s,%s,%s,%s)",
                (row['Question'], row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D'], row['Correct_Ans'])
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Questions uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/api/questions', methods=['GET'])
@login_required
def api_get_questions():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions1")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    questions_response = []
    for q in questions:
        questions_response.append({
            'id': q['id'],
            'question': q['question'],
            'option_a': q['option_a'],
            'option_b': q['option_b'],
            'option_c': q['option_c'],
            'option_d': q['option_d'],
            'correct_ans': q['correct_ans']
        })
    
    return jsonify({'questions': questions_response}), 200

@app.route('/api/questions/count', methods=['GET'])
@login_required
def api_question_count():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions1")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    return jsonify({'count': count}), 200

# --- Quiz APIs ---
@app.route('/api/quiz/submit', methods=['POST'])
@login_required
def api_submit_quiz():
    data = request.get_json()
    answers = data.get('answers', {})
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    score = 0
    results = []
    
    # Get all questions
    cursor.execute("SELECT * FROM questions1 ORDER BY id")
    all_questions = cursor.fetchall()
    
    for question in all_questions:
        q_id = question['id']
        selected_option = answers.get(str(q_id))
        is_correct = False
        
        if selected_option:
            is_correct = (question['correct_ans'] == selected_option)
            if is_correct:
                score += 1
                
            cursor.execute(
                "INSERT INTO answers1 (user_id, question_id, selected_option, is_correct) VALUES (%s, %s, %s, %s)",
                (user_id, q_id, selected_option, is_correct)
            )
        
        results.append({
            'question': question['question'],
            'options': {
                'A': question['option_a'],
                'B': question['option_b'], 
                'C': question['option_c'],
                'D': question['option_d']
            },
            'selected': selected_option or 'Not Attempted',
            'correct': question['correct_ans'],
            'is_correct': is_correct,
            'attempted': selected_option is not None
        })
    
    total_questions = len(all_questions)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        'score': score, 
        'total': total_questions,
        'percentage': round((score/total_questions)*100, 2) if total_questions > 0 else 0,
        'results': results
    }), 200

# --- Dashboard API ---
@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM questions1")
    question_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT answered_at) FROM answers1 WHERE user_id = %s", (session['user_id'],))
    quiz_attempts = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'user': {
            'id': session['user_id'], 
            'email': session['email'],
            'is_admin': session.get('is_admin', False)
        },
        'stats': {
            'question_count': question_count,
            'quiz_attempts': quiz_attempts
        }
    }), 200

# --- Excel Template Download ---
@app.route('/questions_template.xlsx')
def download_template():
    return send_from_directory('.', 'questions_template.xlsx', as_attachment=True)

# --- Admin Stats API ---
@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM questions1")
        question_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users1")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT user_id, DATE(answered_at)) FROM answers1")
        quiz_attempts = cursor.fetchone()[0]
        
        return jsonify({
            'question_count': question_count,
            'user_count': user_count,
            'quiz_attempts': quiz_attempts
        }), 200
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- Health Check ---
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
# --- Health Check ---
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500