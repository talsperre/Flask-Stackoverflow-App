import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Database initialization
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# CSRF Protection
WTF_CSRF_ENABLED = True
SECRET_KEY = "who's your daddy"

# pagination
POSTS_PER_PAGE = 3

# Recaptcha Secret and Public Keys
RECAPTCHA_PUBLIC_KEY = '6LdYKh0UAAAAALk40fZ7hHPZNtgHYuC9VsMT9S1e'
RECAPTCHA_PRIVATE_KEY = '6LdYKh0UAAAAAPL5WAuelU2C99KuRzdIdFeOHvUR'

# Recaptcha parameters
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
