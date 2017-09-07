#!myenv/bin/python
from app import app
app.run(host='0.0.0.0', port=8080, debug=True)
#app.run(host='0.0.0.0', debug=True)