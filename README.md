# Daily Routine Gamifier 🎮

Transform your mundane everyday tasks and habits into engaging mini-games! This app motivates users to complete daily routines by gamifying task completion with points, levels, achievements, and rewards.

## Features

- **User Authentication**: Secure login and registration system with password validation
- **Multiple User Support**: Each user has their own profile, tasks, and progress
- **Task Input & Scheduling**: Create daily routines and chores with scheduling options
- **Gamified Task Completion**: Earn XP, coins, and rewards for completing tasks
- **Visual Progress Tracking**: See progress bars, streak counters, and level progression
- **Rewards & Levels**: Unlock badges, level up, and customize your avatar with items
- **Simple UI with Feedback**: Clean interface with encouraging sounds and visual cues
- **Notifications & Reminders**: Get timely alerts to complete tasks and maintain streaks
- **Achievement System**: Unlock badges for milestones like 7-day streaks and task completion goals

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. You will be redirected to the login page if not authenticated

## Authentication

### User Registration

1. Click "Register here" on the login page
2. Choose a username (3-20 characters, alphanumeric, underscores, and hyphens only)
3. Enter a password (minimum 6 characters)
   - Real-time password strength indicator shows feedback
   - Indicators: Weak, Fair, Good, Strong
4. Confirm your password
   - Match indicator shows if passwords match
5. Click "Create Account"

### User Login

1. Enter your username and password
2. Click "Login"
3. You'll be directed to your personal dashboard

### Password Security

- Passwords are hashed using Werkzeug's `generate_password_hash`
- Original passwords are never stored in the database
- Session tokens are used to maintain login state
- Each user can only see their own tasks and progress

## Usage

1. **Create Tasks**: Click on the "Create New Task" panel and fill in your task details
   - Set task title and description
   - Choose if it's recurring (daily, weekly, etc.)
   - Set scheduled time for reminders
   - Set XP and coin rewards

2. **Complete Tasks**: Click the "Complete" button on any task to earn rewards
   - Earn XP and coins
   - Build your streak
   - Level up when you gain enough XP

3. **Track Progress**: View your level, XP, coins, and streak in the header
   - Watch your XP progress bar fill up
   - Maintain daily streaks for bonus rewards

4. **Unlock Rewards**: Use coins to unlock avatar customizations in the shop
   - Unlock hats, pets, and other items
   - Show off your achievements

5. **Earn Badges**: Complete milestones to unlock achievement badges
   - 7-day streak badge
   - 30-day streak badge
   - 10 tasks completed badge
   - 50 tasks completed badge

6. **User Profile**: Click "Profile" to view your stats and purchased items

7. **Logout**: Click "Logout" to safely exit your account

## Data Storage

### User Credentials (users.json)
- Stores usernames and hashed passwords
- User metadata (registration date, email)

### User Data (user_data.json)
- Tasks associated with each user
- User stats (level, XP, coins, streak, badges)
- Achievements and inventory
- Completed task dates

Each user's data is completely isolated and can only be accessed when logged in as that user.

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON files (can be easily migrated to database)
- **Security**: Werkzeug password hashing

## Project Structure

```
mountainhacks/
├── app.py                      # Main Flask application with auth and API
├── users.json                  # User credentials (auto-created)
├── user_data.json              # User tasks and stats (auto-created)
├── templates/
│   ├── login.html              # Login page
│   ├── register.html           # Registration page with password validation
│   ├── index.html              # Main dashboard
│   └── profile.html            # User profile page
├── static/
│   ├── css/
│   │   └── style.css           # Styling including form validation feedback
│   └── js/
│       └── main.js             # Frontend logic and API calls
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Security Notes

⚠️ **Important for Production**:
- Change the `app.secret_key` in `app.py` to a secure random string
- Consider using environment variables for sensitive configuration
- For production, use a proper database (PostgreSQL, MySQL) instead of JSON files
- Implement HTTPS/SSL encryption
- Add rate limiting to prevent brute force attacks
- Add email verification for new accounts
- Consider implementing password reset functionality
- Use proper CORS headers for API security

## API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /login` - Authenticate user
- `GET /logout` - End user session

### Tasks
- `GET /api/tasks` - Get current user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<task_id>` - Update task
- `DELETE /api/tasks/<task_id>` - Delete task
- `POST /api/tasks/<task_id>/complete` - Mark task as completed

### User Data
- `GET /api/user` - Get current user stats
- `POST /api/user/unlock` - Purchase item from shop

### Pages
- `GET /` - Main dashboard (requires login)
- `GET /profile` - User profile page (requires login)

## Future Enhancements

- Email verification for new accounts
- Password reset functionality
- Social features (share achievements, challenge friends)
- More game mechanics (quests, challenges, leaderboards)
- Mobile app version
- Database integration (SQLite/PostgreSQL)
- More customization options
- Daily/weekly challenges
- User activity logs and statistics

## License

This project is created for Mountain Hacks hackathon.
