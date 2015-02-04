from app import db
import hashlib

def hash(password):
  return hashlib.sha224(password).hexdigest()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), nullable=False, unique=True)
  password = db.Column(db.String(64), nullable=False)
  links = db.relationship('Link', backref='user', lazy='dynamic')

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'id': self.id,
      'username': self.username
    }
