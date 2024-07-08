def calculate_habit_streak(user_id):
    current_date = datetime.utcnow().date()
    streak = 0
    
    # Query to get all user's habits
    habits = Habit.query.filter_by(user_id=user_id).all()
    
    if not habits:
        return 0
    
    while True:
        # Check if all habits were completed for the current date
        completed_habits = HabitLog.query.filter(
            HabitLog.habit_id.in_([h.id for h in habits]),
            func.date(HabitLog.date) == current_date,
            HabitLog.completed == True
        ).count()
        
        if completed_habits == len(habits):
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak
