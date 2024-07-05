class GoalType(Enum):
    SHORT_TERM = 'Short Term'
    LONG_TERM = 'Long Term'

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.Enum(GoalType), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='not started')

    def __repr__(self):
        return f'<Goal {self.title}>'

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    goal = db.relationship('Goal', backref=db.backref('habits', lazy=True))

    def __repr__(self):
        return f'<Habit {self.name}>'

    @property
    def is_completed(self):
        today = datetime.utcnow().date()
        log = HabitLog.query.filter_by(habit_id=self.id, date=today).first()
        return log.completed if log else False

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    habit = db.relationship('Habit', backref=db.backref('logs', lazy=True))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<HabitLog {self.habit.name} - {self.date} - {self.completed}>'
