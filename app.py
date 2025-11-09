from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import uuid
import csv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Data storage file
DATA_FILE = 'user_data.json'

# Define shop items (centralized)
SHOP_ITEMS = {
    'mountain_boots': {'name': 'Mountain Boots', 'cost': 100, 'description': 'Sturdy boots for mountain climbing'},
    'backpack': {'name': 'Adventure Backpack', 'cost': 150, 'description': 'A spacious backpack for your journey'},
    'compass': {'name': 'Golden Compass', 'cost': 200, 'description': 'Never lose your way'},
    'rope': {'name': 'Magic Rope', 'cost': 125, 'description': 'Strong and lightweight climbing rope'},
    'map': {'name': 'Ancient Map', 'cost': 175, 'description': 'Reveals hidden mountain paths'},
    'water_bottle': {'name': 'Enchanted Water Bottle', 'cost': 100, 'description': 'Never runs empty'},
    'first_aid': {'name': 'Healer\'s Kit', 'cost': 150, 'description': 'For magical healing'},
    'tent': {'name': 'Cloud Tent', 'cost': 250, 'description': 'A cozy shelter in the mountains'}
}

def load_data():
    """Load user data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'users': {},
        'tasks': {},
        'achievements': {}
    }

def save_data(data):
    """Save user data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_id():
    """Get or create user session ID"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def initialize_user(data, user_id):
    """Initialize user data if not exists"""
    if user_id not in data['users']:
        data['users'][user_id] = {
            'level': 1,
            'xp': 0,
            'coins': 0,
            'streak': 0,
            'last_completed_date': None,
            'total_tasks_completed': 0,
            'badges': [],
            'inventory': []
        }
    # Migrate old data structure if needed
    user = data['users'][user_id]
    if 'avatar_customizations' in user and 'inventory' not in user:
        user['inventory'] = [item for item in user['avatar_customizations'] if item != 'default']
        del user['avatar_customizations']
        save_data(data)
    if 'inventory' not in user:
        user['inventory'] = []
        save_data(data)
    return user

@app.route('/')
def index():
    """Main page"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            return render_template('login.html', error='Please fill in all fields')
        
        # Read CSV file
        try:
            with open('login_info.csv', 'r') as f:
                reader = csv.DictReader(f)
                for user in reader:
                    if user['username'] == username and check_password_hash(user['password'], password):
                        session['username'] = username
                        session['user_id'] = str(uuid.uuid4())
                        session['avatar'] = user['avatar']
                        session['coins'] = int(user['coins'])
                        return redirect(url_for('index'))
            
            return render_template('login.html', error='Invalid username or password')
        except FileNotFoundError:
            return render_template('login.html', error='System error. Please try again later.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not password:
            return render_template('register.html', error='Please fill in all fields')
            
        if len(username) < 3:
            return render_template('register.html', error='Username must be at least 3 characters long')
            
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters long')
            
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        try:
            # Check if username already exists
            with open('login_info.csv', 'r') as f:
                reader = csv.DictReader(f)
                if any(user['username'] == username for user in reader):
                    return render_template('register.html', error='Username already exists')
            
            # Hash password and add new user
            hashed_password = generate_password_hash(password)
            with open('login_info.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, hashed_password, 'default', 100, ''])  # Starting with 100 coins
            
            # Start session
            session['username'] = username
            session['user_id'] = str(uuid.uuid4())
            session['avatar'] = 'default'
            session['coins'] = 100
            
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks for current user"""
    data = load_data()
    user_id = get_user_id()
    initialize_user(data, user_id)
    
    user_tasks = [task for task in data['tasks'].values() if task.get('user_id') == user_id]
    return jsonify({'tasks': user_tasks})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = load_data()
    user_id = get_user_id()
    user = initialize_user(data, user_id)
    
    task_data = request.json
    task_id = str(uuid.uuid4())
    
    new_task = {
        'id': task_id,
        'user_id': user_id,
        'title': task_data.get('title'),
        'description': task_data.get('description', ''),
        'recurring': task_data.get('recurring', False),
        'frequency': task_data.get('frequency', 'daily'),  # daily, weekly, custom
        'scheduled_time': task_data.get('scheduled_time', ''),
        'xp_reward': task_data.get('xp_reward', 10),
        'coin_reward': task_data.get('coin_reward', 5),
        'completed': False,
        'completed_dates': [],
        'created_at': datetime.now().isoformat(),
        'streak': 0
    }
    
    data['tasks'][task_id] = new_task
    save_data(data)
    
    return jsonify({'task': new_task, 'message': 'Task created successfully!'})

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = load_data()
    user_id = get_user_id()
    
    if task_id not in data['tasks'] or data['tasks'][task_id].get('user_id') != user_id:
        return jsonify({'error': 'Task not found'}), 404
    
    task_data = request.json
    task = data['tasks'][task_id]
    
    # Update task fields
    for key in ['title', 'description', 'recurring', 'frequency', 'scheduled_time']:
        if key in task_data:
            task[key] = task_data[key]
    
    save_data(data)
    return jsonify({'task': task, 'message': 'Task updated successfully!'})

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    data = load_data()
    user_id = get_user_id()
    
    if task_id not in data['tasks'] or data['tasks'][task_id].get('user_id') != user_id:
        return jsonify({'error': 'Task not found'}), 404
    
    del data['tasks'][task_id]
    save_data(data)
    return jsonify({'message': 'Task deleted successfully!'})

@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark task as completed and award rewards"""
    data = load_data()
    user_id = get_user_id()
    user = initialize_user(data, user_id)
    
    if task_id not in data['tasks'] or data['tasks'][task_id].get('user_id') != user_id:
        return jsonify({'error': 'Task not found'}), 404
    
    task = data['tasks'][task_id]
    today = datetime.now().date().isoformat()
    
    # Check if already completed today
    if today in task.get('completed_dates', []):
        return jsonify({'error': 'Task already completed today'}), 400
    
    # Award rewards
    xp_reward = task.get('xp_reward', 10)
    coin_reward = task.get('coin_reward', 5)
    
    user['xp'] += xp_reward
    user['coins'] += coin_reward
    user['total_tasks_completed'] += 1
    
    # Update streak
    last_date = user.get('last_completed_date')
    if last_date:
        last_date_obj = datetime.fromisoformat(last_date).date()
        today_obj = datetime.now().date()
        
        if (today_obj - last_date_obj).days == 1:
            user['streak'] += 1
            task['streak'] = task.get('streak', 0) + 1
        elif (today_obj - last_date_obj).days > 1:
            user['streak'] = 1
            task['streak'] = 1
        else:
            # Same day, maintain streak
            pass
    else:
        user['streak'] = 1
        task['streak'] = 1
    
    user['last_completed_date'] = datetime.now().isoformat()
    
    # Update task
    if 'completed_dates' not in task:
        task['completed_dates'] = []
    task['completed_dates'].append(today)
    task['completed'] = True
    
    # Level up check
    xp_for_next_level = user['level'] * 100
    level_up = False
    while user['xp'] >= xp_for_next_level:
        user['level'] += 1
        user['xp'] -= xp_for_next_level
        xp_for_next_level = user['level'] * 100
        level_up = True
        user['coins'] += 50  # Bonus coins on level up
    
    # Check for achievements
    achievements_unlocked = []
    
    # Streak achievements
    if user['streak'] == 7 and 'streak_7' not in user['badges']:
        user['badges'].append('streak_7')
        achievements_unlocked.append('7 Day Streak!')
    if user['streak'] == 30 and 'streak_30' not in user['badges']:
        user['badges'].append('streak_30')
        achievements_unlocked.append('30 Day Streak!')
    
    # Task completion achievements
    if user['total_tasks_completed'] == 10 and 'tasks_10' not in user['badges']:
        user['badges'].append('tasks_10')
        achievements_unlocked.append('10 Tasks Completed!')
    if user['total_tasks_completed'] == 50 and 'tasks_50' not in user['badges']:
        user['badges'].append('tasks_50')
        achievements_unlocked.append('50 Tasks Completed!')
    
    save_data(data)
    
    return jsonify({
        'message': 'Task completed!',
        'xp_reward': xp_reward,
        'coin_reward': coin_reward,
        'user': user,
        'level_up': level_up,
        'achievements': achievements_unlocked
    })

@app.route('/api/user', methods=['GET'])
def get_user():
    """Get current user data"""
    data = load_data()
    user_id = get_user_id()
    user = initialize_user(data, user_id)
    
    # Calculate XP needed for next level
    xp_needed = user['level'] * 100
    xp_progress = user['xp'] % xp_needed if user['level'] > 1 else user['xp']
    xp_percentage = (xp_progress / xp_needed) * 100
    
    return jsonify({
        'user': user,
        'xp_needed': xp_needed,
        'xp_progress': xp_progress,
        'xp_percentage': xp_percentage
    })

@app.route('/api/user/unlock', methods=['POST'])
def unlock_customization():
    """Unlock avatar/item customization"""
    data = load_data()
    user_id = get_user_id()
    user = initialize_user(data, user_id)
    
    item_data = request.json
    item_id = item_data.get('item')
    item_cost = item_data.get('cost', 100)
    
    # Validate item exists
    if item_id not in SHOP_ITEMS:
        return jsonify({'error': 'Invalid item'}), 400
        
    item = SHOP_ITEMS[item_id]
    
    # Initialize inventory if doesn't exist
    if 'inventory' not in user:
        user['inventory'] = []
    
    # Check if already owned
    if item_id in user.get('inventory', []):
        return jsonify({'error': 'Item already unlocked'}), 400
    
    # Check if enough coins
    if user['coins'] < item['cost']:
        return jsonify({'error': 'Not enough coins'}), 400
    
    # Purchase the item
    user['coins'] -= item['cost']
    user['inventory'].append(item_id)
    
    save_data(data)
    return jsonify({
        'message': f'Successfully purchased {item["name"]}!',
        'user': user,
        'item': {
            'id': item_id,
            'name': item['name'],
            'cost': item['cost']
        }
    })

@app.route('/profile')
def profile():
    """User profile page"""
    if 'username' not in session:
        return redirect(url_for('login'))
        
    data = load_data()
    user_id = get_user_id()
    user = initialize_user(data, user_id)
    
    # Initialize inventory if doesn't exist
    if 'inventory' not in user:
        user['inventory'] = []
        save_data(data)
    
    # Get user's purchased items
    purchased_items = [
        {**SHOP_ITEMS[item], 'id': item}
        for item in user.get('inventory', [])
        if item in SHOP_ITEMS
    ]
    
    # Get total coins earned (current + spent)
    total_coins_earned = user['coins'] + sum(SHOP_ITEMS[item]['cost'] for item in user.get('inventory', []) if item in SHOP_ITEMS)
    
    return render_template('profile.html',
                         username=session['username'],
                         user=user,
                         purchased_items=purchased_items,
                         total_coins_earned=total_coins_earned)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
