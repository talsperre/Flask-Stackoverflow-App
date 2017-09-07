from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir
from flask import render_template
#from . import context_processors

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page"
login_manager.login_view = "login"
Bootstrap(app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

from app.mod_answer.views import mod_answer
app.register_blueprint(mod_answer)

from app.mod_auth.views import mod_auth
app.register_blueprint(mod_auth)

from app.mod_comment.views import mod_comment
app.register_blueprint(mod_comment)

from app.mod_home.views import mod_home
app.register_blueprint(mod_home)

from app.mod_question.views import mod_question
app.register_blueprint(mod_question)

from app.mod_tag.views import mod_tag
app.register_blueprint(mod_tag)

from app.mod_user.views import mod_user
app.register_blueprint(mod_user)

from app.mod_vote.views import mod_vote
app.register_blueprint(mod_vote)
