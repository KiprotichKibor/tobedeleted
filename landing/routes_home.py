<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">

@app.route("/home")
@login_required
def home():
    current_date = datetime.utcnow()
    
    # Fetch data for summaries
    goals_count = Goal.query.filter_by(user_id=current_user.id, status='in_progress').count()
    completed_goals_count = Goal.query.filter_by(user_id=current_user.id, status='completed').count()
    habits_count = Habit.query.filter_by(user_id=current_user.id).count()
    habits_completed_today = HabitLog.query.filter(
        HabitLog.habit.has(user_id=current_user.id),
        HabitLog.date == current_date.date(),
        HabitLog.completed == True
    ).count()
    
    # Fetch mood data for the last 7 days
    seven_days_ago = current_date - timedelta(days=7)
    moods = Mood.query.filter(
        Mood.user_id == current_user.id,
        Mood.date >= seven_days_ago
    ).order_by(Mood.date).all()
    
    mood_dates = [mood.date.strftime('%Y-%m-%d') for mood in moods]
    mood_values = [mood.mood_type.value for mood in moods]
    mood_average = sum(mood_values) / len(mood_values) if mood_values else 0
    
    # Calculate goal completion rate and habit streak
    total_goals = Goal.query.filter_by(user_id=current_user.id).count()
    goal_completion_rate = (completed_goals_count / total_goals * 100) if total_goals > 0 else 0
    
    habit_streak = calculate_habit_streak(current_user.id)  # You'll need to implement this function
    
    return render_template('home.html',
                           current_date=current_date,
                           goals_count=goals_count,
                           completed_goals_count=completed_goals_count,
                           habits_count=habits_count,
                           habits_completed_today=habits_completed_today,
                           mood_dates=mood_dates,
                           mood_values=mood_values,
                           mood_average=round(mood_average, 1),
                           goal_completion_rate=round(goal_completion_rate, 1),
                           habit_streak=habit_streak)
