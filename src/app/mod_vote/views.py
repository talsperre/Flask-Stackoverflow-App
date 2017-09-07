from flask import render_template, flash, redirect, url_for, session, g, request, Blueprint, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from ..forms import LoginForm, RegistrationForm, QuestionForm, AnswerForm, TagForm
from app.mod_user.models import User
from app.mod_answer.models import Answer
from app.mod_question.models import Question
from app.mod_tag.models import Tag
from .models import Upvote, Downvote
from app.mod_comment.models import Comment
from datetime import datetime
from sqlalchemy import and_
#from . import mod_vote
#from ..mod_question import views
mod_vote = Blueprint('mod_vote', __name__)

@mod_vote.route('/answerUpvote/<answer_id>')
@login_required
def answerUpvote(answer_id):
	"""This function does upvote on a particular answer in database"""
	answer = Answer.query.filter_by(answer_id = answer_id).first()
	if len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.answer_id == answer_id)).all()) == 0:
		try:
			upvote = Upvote(author = g.user, answer = answer)
			db.session.add(upvote)
			db.session.commit()
		except:
			print ("Could not add Upvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = answer.question_id))
	return jsonify({'upvotes': len(answer.upvotes.all())})

@mod_vote.route('/questionUpvote/<question_id>')
@login_required
def questionUpvote(question_id):
	"""This function does upvote on a particular question in database"""
	print (question_id)
	question = Question.query.filter_by(question_id = question_id).first()
	if len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.question_id == question_id)).all()) == 0:
		try:
			upvote = Upvote(author = g.user, question = question)
			db.session.add(upvote)
			db.session.commit()
		except:
			print ("Could not add Upvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = question_id))
	return jsonify({'upvotes': len(question.upvotes.all())})

@mod_vote.route('/answerDownvote/<answer_id>')
@login_required
def answerDownvote(answer_id):
	"""This function does Downvote on a particular answer in database"""
	answer = Answer.query.filter_by(answer_id = answer_id).first()
	if len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.answer_id == answer_id)).all()) == 0:
		try:
			downvote = Downvote(author = g.user, answer = answer)
			db.session.add(downvote)
			db.session.commit()
		except:
			print ("Could not add Downvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = answer.question_id))
	return jsonify({'downvotes': len(answer.downvotes.all())})

@mod_vote.route('/questionDownvote/<question_id>')
@login_required
def questionDownvote(question_id):
	"""This function does Upvote on a particular question in database"""
	question = Question.query.filter_by(question_id = question_id).first()
	if len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.question_id == question_id)).all()) == 0:
		try:
			downvote = Downvote(author = g.user, question = question)
			db.session.add(downvote)
			db.session.commit()
		except:
			print ("Could not add Downvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = question_id))
	return jsonify({'downvotes': len(question.downvotes.all())})

@mod_vote.route('/commentUpvote/<comment_id>')
@login_required
def commentUpvote(comment_id):
	"""THis function does Upvote on a particular comment in database"""
	comment = Comment.query.filter_by(comment_id = comment_id).first()
	if (comment.question_id):
		question_id = comment.question_id
	else :
		answer = Answer.query.filter_by(answer_id = comment.answer_id).first()
		question_id = answer.question_id
	if len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.comment_id == comment_id)).all()) == 0:
		try:
			upvote = Upvote(author = g.user, comment = comment)
			db.session.add(upvote)
			db.session.commit()
		except:
			print ("Could not add Upvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = question_id))
	return jsonify({'upvotes': len(comment.upvotes.all())})

@mod_vote.route('/commentDownvote/<comment_id>')
@login_required
def commentDownvote(comment_id):
	"""This function does Downvote on a particular comment in database"""
	comment = Comment.query.filter_by(comment_id = comment_id).first()
	if (comment.question_id):
		question_id = comment.question_id
	else :
		answer = Answer.query.filter_by(answer_id = comment.answer_id).first()
		question_id = answer.question_id
	if len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.comment_id == comment_id)).all()) == 0:
		try:
			downvote = Downvote(author = g.user, comment = comment)
			db.session.add(downvote)
			db.session.commit()
		except:
			print ("Could not add Downvote")
	#return redirect(url_for('mod_question.showQuestion', question_id = question_id))
	return jsonify({'downvotes': len(comment.downvotes.all())})

"""Registers a function to run before each request.The function will be called without any arguments. 
If the function returns a non-None value, it’s handled as if it was the return value from the view and further request handling is stopped"""

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

"""app.context-> Binds the application only. For as long as the application is bound to the current context the flask.current_app points to that application. 
                 An application context is automatically created when a request context is pushed if necessary.
                 """
"""context_processor:Registers a template context processor function."""
@app.context_processor
def utility_processor():
	def user(user_id):
		"""filters users by user_id and returns an object of users"""
		return User.query.filter_by(user_id = user_id).first()
	return dict(user = user)

@app.context_processor
def answer_comments():
	def get_answer_comments(answer_id):
		"""filters answers by anser_id and returns an object of comments filtered"""
		return Comment.query.filter_by(answer_id = answer_id).all()
	return dict(get_answer_comments = get_answer_comments)

@app.context_processor
def answer_id():
	def create_answer_id(answer_id):
		return "add-answer-comment-" + str(answer_id)
	return dict(create_answer_id = create_answer_id)

@app.context_processor
def body_id():
	def create_comment_body_id(answer_id):
		return "comment-body-" + str(answer_id)
	return dict(create_comment_body_id = create_comment_body_id)

@app.context_processor
def vote_check():
	"""tells number of votes based on whether it is upvote,downvote on question or answer"""
	"""pid => comment_id/question_id/answer_id, votetype => upvote/downvote, contenttype => question/comment/answer"""
	def vote_allowed_check(pid, votetype, contenttype):
		ans = 1
		if g.user.is_authenticated:
			if votetype == 1:
				"""Votetype 1-> Upvote"""
				if contenttype == 1:
					"""Upvote on a question"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.question_id == pid)).all())
				elif contenttype == 2:
					"""Upvote on an answer"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.answer_id == pid)).all())
				else :
					"""Upvote on a comment"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.comment_id == pid)).all())
			else : 
				"""Votetype 2->Downvote"""
				if contenttype == 1:
					"""Downvote on a question"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.question_id == pid)).all())
				elif contenttype == 2:
					"""Downvote on an answer"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.answer_id == pid)).all())
				else :
					"""Downvote on a comment"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.comment_id == pid)).all())
			print (ans)
		if ans >= 1:
			return 0
		else :
			return 1
	return dict(vote_allowed_check = vote_allowed_check)