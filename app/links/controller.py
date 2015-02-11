from app import app
from .model import Link
from flask import jsonify, request
from ..users.controller import auth
from ..users.model import User
from datetime import datetime

@app.route('/links')
def links():
  links = [l.serialize() for l in Link.query.order_by(Link.score.desc()).all()]
  return jsonify({'links': links})

# POST: title, url
@app.route('/links/create', methods=['POST'])
@auth.login_required
def create():
  title = request.form['title']
  url = request.form['url']
  user_id = User.query.filter_by(username=auth.username()).first().id
  link = Link(title, url, user_id)
  link.save()
  return jsonify(link.serialize())

# POST: link_id
@app.route('/links/vote', methods=['POST'])
@auth.login_required
def vote():
  link_id = request.form['link_id']
  link = Link.query.get(link_id)
  user = User.query.filter_by(username=auth.username()).first()
  ids = [u.id for u in link.voters]
  if not user.id in ids:
    link.points += 1
    link.voters.append(user)
    now = datetime.now()
    created = link.created_at
    delta = now - created
    hours = delta.seconds / 60 / 60
    link.score = (link.points - 1) / (hours + 2) ** 1.8
    link.save()
  return jsonify(link.serialize())