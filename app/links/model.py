from app import db
from datetime import datetime

voters = db.Table('voters',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('link_id', db.Integer, db.ForeignKey('link.id'))
)

class Link(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64), nullable=False)
  url = db.Column(db.String(128), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  score = db.Column(db.Float)
  points = db.Column(db.Integer)
  voters = db.relationship('User', secondary=voters, backref=db.backref('users', lazy='dynamic'))
  created_at = db.Column(db.DateTime)

  def __init__(self, title, url, user_id):
    self.title = title
    self.url = url
    self.user_id = user_id
    self.score = 0
    self.points = 0
    self.created_at = datetime.now()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'id': self.id,
      'title': self.title,
      'url': self.url,
      'user_id': self.user_id,
      'score': self.score,
      'points': self.points,
      'created_at': self.created_at
    }