class MoodForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    mood_type = SelectField('Mood', choices=[(mood.name, mood.value) for mood in MoodType], validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Log Mood')
