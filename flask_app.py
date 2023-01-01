from flask import *

app = Flask(__name__)

@app.route('/')
def page():
    return render_template('/index.html')

app.run()