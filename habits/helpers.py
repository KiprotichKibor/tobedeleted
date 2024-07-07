from datetime import datetime, timedelta
from collections import Counter
from .models import Goal, Habit, HabitLog, Mood
import numpy as np

def get_week_start_end():
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start, end

def fetch_weekly_data():
    start, end = get_week_start_end()

    # Goals
    goals = Goal.query.all()
    goal_progress = {goal.title: goal.status for goal in goals}

    # Habits
    habits = Habit.query.all()
    habit_completion = {habit.name: 0 for habit in habits}
    habit_logs = HabitLog.query.filter(HabitLog.date >= start, HabitLog.date <= end).all()
    for log in habit_logs:
        if log.completed:
            habit_completion[log.habit.name] += 1

    # Moods
    moods = Mood.query.filter(Mood.date >= start, Mood.date <= end).all()
    mood_counter = Counter([mood.mood_type.value for mood in moods])

    return goal_progress, habit_completion, mood_counter, goals, habits, moods

def calculate_goals_completed(goals):
    completed = sum(1 for goal in goals if goal.status == 'completed')
    total = len(goals)
    return round((completed / total) * 100 if total > 0 else 0, 2)

def calculate_habit_completion_rate(habit_completion):
    total_completions = sum(habit_completion.values())
    total_possible = len(habit_completion) * 7  # 7 days in a week
    return round((total_completions / total_possible) * 100 if total_possible > 0 else 0, 2)

def calculate_most_common_mood(mood_counter):
    return mood_counter.most_common(1)[0][0] if mood_counter else 'No data'

def calculate_mood_trend(moods):
    if not moods:
        return 'No data'
    mood_values = [list(Mood.MoodType).index(mood.mood_type) for mood in moods]
    if len(mood_values) < 2:
        return 'Stable'
    trend = np.polyfit(range(len(mood_values)), mood_values, 1)[0]
    if trend > 0:
        return 'Improving'
    elif trend < 0:
        return 'Declining'
    else:
        return 'Stable'

def get_dates_of_week():
    start, end = get_week_start_end()
    return [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

def get_mood_values_of_week(moods):
    mood_dict = {mood.date.strftime('%Y-%m-%d'): list(Mood.MoodType).index(mood.mood_type) + 1 for mood in moods}
    return [mood_dict.get(date, None) for date in get_dates_of_week()]

def calculate_goal_habit_correlation(goals, habits):
    goal_progress = [list(Goal.StatusType).index(goal.status) for goal in goals]
    habit_completion = [sum(1 for log in habit.logs if log.completed) / 7 for habit in habits]
    if len(goal_progress) != len(habit_completion):
        return []
    return [{'x': gp, 'y': hc} for gp, hc in zip(goal_progress, habit_completion)]

def get_analytics_data():
    goal_progress, habit_completion, mood_counter, goals, habits, moods = fetch_weekly_data()
    
    data = {
        'goal_progress': goal_progress,
        'habit_completion': habit_completion,
        'mood_counter': dict(mood_counter),
        'goals_completed': calculate_goals_completed(goals),
        'habit_completion_rate': calculate_habit_completion_rate(habit_completion),
        'most_common_mood': calculate_most_common_mood(mood_counter),
        'mood_trend': calculate_mood_trend(moods),
        'mood_over_time': {
            'dates': get_dates_of_week(),
            'values': get_mood_values_of_week(moods)
        },
        'goal_habit_correlation': calculate_goal_habit_correlation(goals, habits)
    }
    
    return data
