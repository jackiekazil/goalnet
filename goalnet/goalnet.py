import os
from flask import Flask, render_template

# configuration
DEBUG = True

# create app
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('GOALNET_SETTINGS', silent=True)

@app.route('/', methods=['GET'])
def index():
    runs = os.listdir('static/data/runs/')

    return render_template('index.html',
        runs=runs
        )

@app.route('/runs/<run_id>', methods = ['GET'])
def run_detail(run_id=None):
    return render_template('run_detail.html', run_id=run_id)

if __name__ == '__main__':
    #init_db()
    app.run()