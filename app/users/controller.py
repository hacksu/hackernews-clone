from app import app
from flask import jsonify, request
from .model import User, hash
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
  user = User.query.filter_by(username=username).first()
  if user:
    return user.password
  return None

@auth.hash_password
def hash_pw(password):
  return hash(password)

@app.route('/users')
def users():
  users = [u.serialize() for u in User.query.all()]
  return jsonify({'users': users})

@app.route('/users/register', methods=['POST'])
def register():
  user = User(request.form['username'], hash(request.form['password']))
  user.save()
  return jsonify(user.serialize())