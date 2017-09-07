from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

"""This is the model for User class"""
class User(UserMixin, db.Model):
	__tablename__ = "users"
	user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String, index = True, unique = True)
	email = db.Column(db.String, index = True, unique = True)
	password_hash = db.Column(db.String(128))
	last_seen = db.Column(db.DateTime)
	questions = db.relationship('Question', backref = 'author', lazy = 'dynamic')
	answers = db.relationship('Answer', backref = 'author', lazy = 'dynamic')
	comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')
	upvotes = db.relationship('Upvote', backref = 'author', lazy = 'dynamic')
	downvotes = db.relationship('Downvote', backref = 'author', lazy = 'dynamic')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	"""This generates password based on hashing """
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	"""This verifies password based on hashing"""
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_id(self):
		return str(self.user_id)

	"""Uses gravatar API"""
	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)
	def __repr__(self):
		return '<User %r>' % (self.username)

"""Refer to Flask/login documentation"""
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))