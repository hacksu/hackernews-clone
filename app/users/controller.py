from app import app
from flask import jsonify, request
from .model import User, hash

@app.route('/users')
def users():
  users = [u.serialize() for u in User.query.all()]
  return jsonify({'users': users})

@app.route('/users/register', methods=['POST'])
def register():
  user = User(request.form['username'], hash(request.form['password']))
  user.save()
  return jsonify(user.serialize())