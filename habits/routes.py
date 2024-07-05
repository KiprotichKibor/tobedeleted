@habit_bp.route('/habits', methods=['GET', 'POST'])
def habits():
    form = HabitForm()
    form.goal.choices = [(goal.id, goal.title) for goal in Goal.query.all()]
    if form.validate_on_submit():
        new_habit = Habit(name=form.name.data, goal_id=form.goal.data)
        db.session.add(new_habit)
        db.session.commit()
        flash('Habit added successfully!', 'success')
        return redirect(url_for('habit.habits'))
    habits = Habit.query.all()
    goals = Goal.query.all()
    return render_template('habits.html', form=form, habits=habits, goals=goals)

@habit_bp.route('/habit/log/<int:habit_id>', methods=['GET', 'POST'])
def log_habit(habit_id):
    form = HabitLogForm()
    habit = Habit.query.get_or_404(habit_id)
    if form.validate_on_submit():
        new_log = HabitLog(
            habit_id=habit_id,
            date=form.date.data,
            completed=form.completed.data,
            notes=form.notes.data
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Habit log updated successfully!', 'success')
        return redirect(url_for('habit.habits'))
    logs = HabitLog.query.filter_by(habit_id=habit_id).order_by(HabitLog.date.desc()).all()
    return render_template('log_habit.html', form=form, habit=habit, logs=logs)

@habit_bp.route('/habits/history/<int:habit_id>')
def habits_history(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    habit_history = HabitLog.query.filter_by(habit_id=habit_id).order_by(HabitLog.date.desc()).all()
    return render_template('habits_history.html', habit=habit, habit_history=habit_history)

@habit_bp.route('/habit/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    flash('Habit deleted successfully!', 'success')
    return redirect(url_for('habit.habits'))

@habit_bp.route('/habit/update/<int:habit_id>', methods=['POST'])
def update_status(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    form = HabitStatusForm()
    if form.validate_on_submit():
        new_log = HabitLog(
            habit_id=habit_id,
            date=datetime.utcnow().date(),
            completed=form.status.data == 'completed',
            notes=form.notes.data
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Habit status updated successfully!', 'success')
    return redirect(url_for('habit.habits'))

@habit_bp.route('/goals', methods=['GET', 'POST'])
def goals():
    form = GoalForm()
    if form.validate_on_submit():
        new_goal = Goal(
            title=form.title.data,
            description=form.description.data,
            type=GoalType[form.type.data],
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('habit.goals'))
    goals = Goal.query.all()
    return render_template('goals.html', form=form, goals=goals)
