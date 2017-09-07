from flask import render_template, flash, redirect, url_for, session, g, request, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from ..forms import QuestionForm
from datetime import datetime
from sqlalchemy import and_
from .models import Question
from app.mod_user.models import User
from app.mod_answer.models import Answer
from app.mod_tag.models import Tag
from app.mod_vote.models import Upvote, Downvote
from app.mod_comment.models import Comment
mod_question = Blueprint('mod_question', __name__)

@mod_question.route('/question/<question_id>', methods = ['GET', 'POST'])
def showQuestion(question_id):
	"""This function shows a particular question by given question id"""
	question = Question.query.filter_by(question_id = question_id).all()
	if not question:
		return redirect(url_for('index'))
	answers = Answer.query.filter_by(question_id = question_id).all()
	answers = question[0].answers
	comments = Comment.query.filter_by(question_id = question_id).all()
	enabled = True
	if g.user.is_authenticated and len(Answer.query.filter_by(question_id = question_id, user_id = g.user.user_id).all()):
		enabled = False
	return render_template('mod_question/showQuestion.html', title = question[0].title, questions = question, answers = answers, enabled = enabled, comments = comments)

@mod_question.route('/addQuestion', methods = ['GET', 'POST'])
@login_required
def addQuestion():
	"""This function adds question which the user has written through form"""
	form = QuestionForm()
	print(form.validate_on_submit())
	if form.validate_on_submit():
		print(form.tag.data)
		code = "\n" + form.code.data
		question = Question(title = form.title.data, body = form.body.data, code = code, author = g.user, timestamp = datetime.utcnow(), answered = 0)
		db.session.add(question)
		db.session.commit()
		tags = form.tag.data.split(",")
		print(tags)
		for i in tags:
			tag = Tag(body = i, question = question)
			db.session.add(tag)
			db.session.commit()
		return redirect(url_for('mod_home.index'))
	return render_template('mod_question/addQuestion.html', title = 'Add Question', form = form)

@mod_question.route('/unansweredQuestions')
@mod_question.route('/unansweredQuestions/<int:page>', methods=['GET', 'POST'])
def unansweredQuestions(page=1):
	"""Returns number of unanswered questions"""
	questions = Question.query.filter(Question.answered == 0).order_by(Question.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	#questions = Question.query.filter(Question.answered == 0).order_by(Question.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('mod_question/unansweredQuestions.html', title = 'Unanswered Questions', questions = questions)

@mod_question.route('/answeredQuestions')
@mod_question.route('/answeredQuestions/<int:page>', methods=['GET', 'POST'])
def answeredQuestions(page=1):
	"""Returns number of answered questions"""
	questions = Question.query.filter(Question.answered != 0).order_by(Question.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	#questions = Question.query.filter(Question.answered != 0).order_by(Question.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('mod_question/answeredQuestions.html', title = 'Answered Questions', questions = questions)

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