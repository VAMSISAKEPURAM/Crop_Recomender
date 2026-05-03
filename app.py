import os
import sqlite3
import pickle
import numpy as np
import bcrypt
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-super-secret-key')
DATABASE = 'users.db'

# Load Model and Scaler
MODEL_PATH = os.path.join(app.root_path, 'model', 'crop_model.pkl')
SCALER_PATH = os.path.join(app.root_path, 'model', 'scaler.pkl')

model = None
scaler = None

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
    else:
        print("Warning: Model or scaler files not found. Prediction endpoint will return an error until they are available.")
except Exception as e:
    print(f"Error loading models: {e}")

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/')
@login_required
def dashboard():
    return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Please provide both username and password.')
            
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password.')
        except sqlite3.Error:
            return render_template('login.html', error='Database connection error.')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error='Please provide both username and password.')
            
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            conn.close()
            
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Username already exists. Please choose a different one.')
        except sqlite3.Error:
            return render_template('register.html', error='Database error occurred during registration.')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if model is None or scaler is None:
        return jsonify({'error': 'Model not found. Please check model directory.'}), 503
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided.'}), 400
            
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall']
        input_data = []
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({'error': f'Missing value for {field}.'}), 400
            
            try:
                # Ensure it's a number
                val = float(data[field])
                input_data.append(val)
            except ValueError:
                return jsonify({'error': f'Invalid value for {field}. Must be numeric.'}), 400
                
        # Transform and predict
        input_array = np.array(input_data).reshape(1, -1)
        scaled_input = scaler.transform(input_array)
        prediction = model.predict(scaled_input)[0]
        
        return jsonify({
            'success': True,
            'prediction': str(prediction),
            'message': 'Prediction successful.'
        })
        
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'error': 'An unexpected error occurred during prediction.'}), 500

# Error handlers
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='Internal Server Error'), 500

@app.errorhandler(404)
def not_found_error(e):
    return render_template('error.html', error='Page Not Found'), 404

if __name__ == '__main__':
    # Debug mode should be disabled for production
    app.run(debug=False, host='0.0.0.0', port=5000)
