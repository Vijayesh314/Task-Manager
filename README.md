# Taskality

Transform your mundane everyday tasks and habits into a fun and interactive experience! This app motivates users to complete daily routines by gamifying task completion with points, levels, achievements, and rewards.

## Features

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

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON file (can be easily migrated to database)

## Project Structure

```
mountainhacks/
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- User authentication and multiple user support
- Social features (share achievements, challenge friends)
- More game mechanics (quests, challenges, leaderboards)
- Mobile app version
- More customization options
- Daily/weekly challenges

## License

This project is created for Mountain Hacks hackathon
