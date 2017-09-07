from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime

"""This is the model for Tag class"""
class Tag(db.Model):
	__tablename__ = "tags"
	tag_id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String)
	question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))

	def __repr__(self):
		return '<Tag %r>' % (self.body)