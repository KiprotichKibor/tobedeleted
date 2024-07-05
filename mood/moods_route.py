from flask import jsonify

@mood_bp.route('/moods', methods=['GET', 'POST'])
def moods():
    form = MoodForm()
    if form.validate_on_submit():
        new_mood = Mood(
            date=form.date.data,
            mood_type=MoodType[form.mood_type.data],
            notes=form.notes.data
        )
        try:
            db.session.add(new_mood)
            db.session.commit()
            flash('Mood logged successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error: Mood for this date already exists.', 'error')
        return redirect(url_for('mood.moods'))
    
    moods = Mood.query.order_by(Mood.date.desc()).all()
    
    # Prepare data for the mood chart
    dates = [mood.date.strftime('%Y-%m-%d') for mood in moods]
    mood_values = [list(MoodType).index(mood.mood_type) + 1 for mood in moods]
    
    return render_template('moods.html', form=form, moods=moods, dates=dates, mood_values=mood_values)

@mood_bp.route('/moods/<int:mood_id>/edit', methods=['GET', 'POST'])
def edit_mood(mood_id):
    mood = Mood.query.get_or_404(mood_id)
    form = MoodForm(obj=mood)
    if form.validate_on_submit():
        mood.date = form.date.data
        mood.mood_type = MoodType[form.mood_type.data]
        mood.notes = form.notes.data
        db.session.commit()
        flash('Mood updated successfully!', 'success')
        return redirect(url_for('mood.moods'))
    return render_template('edit_mood.html', form=form, mood=mood)

@mood_bp.route('/moods/<int:mood_id>/delete', methods=['POST'])
def delete_mood(mood_id):
    mood = Mood.query.get_or_404(mood_id)
    db.session.delete(mood)
    db.session.commit()
    flash('Mood deleted successfully!', 'success')
    return redirect(url_for('mood.moods'))
