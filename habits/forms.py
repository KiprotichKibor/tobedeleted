class HabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[DataRequired()])
    goal = SelectField('Associated Goal', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class HabitLogForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    completed = BooleanField('Completed')
    notes = TextAreaField('Notes')
    submit = SubmitField('Log Habit')

class HabitStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('completed', 'Completed'), ('not_completed', 'Not Completed')])
    notes = TextAreaField('Notes')
    submit = SubmitField('Update Status')

class GoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    type = SelectField('Goal Type', choices=[(t.name, t.value) for t in GoalType], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Add Goal')
