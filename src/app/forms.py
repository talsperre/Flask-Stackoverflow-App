from flask_wtf import Form, RecaptchaField
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from app.mod_user.models import User

class RegistrationForm(Form):
	email = StringField('Email', validators = [DataRequired(), Email()])
	username = StringField('Username', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')
	recaptcha = RecaptchaField()
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email is already in use.')

	def validate_username(self, field):
		if User.query.filter_by(username = field.data).first():
			raise ValidationError('Username is already in use.')

class LoginForm(Form):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	submit = SubmitField('Login')

class QuestionForm(Form):
	title = StringField('Title', validators = [DataRequired()])
	body = TextAreaField('Body', validators = [DataRequired()])
	code = TextAreaField('Code')
	tag = StringField('Tags')
	submit = SubmitField('Add Question')

class AnswerForm(Form):
	body = TextAreaField('Body', validators = [DataRequired()])
	code = TextAreaField('Code')
	submit = SubmitField('Submit Answer')

class TagForm(Form):
	tag = StringField('Tags')
	submit = SubmitField('Search Tag')

class ProfileForm(Form):
	username = StringField('Username', validators = [DataRequired()])
	submit = SubmitField('Search User')