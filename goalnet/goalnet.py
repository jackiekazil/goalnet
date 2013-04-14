from flask import Flask, render_template

# configuration
DEBUG = True

# create app
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('GOALNET_SETTINGS', silent=True)

@app.route('/', methods=['GET'])
def index():
    error = None
    return render_template('index.html', error=error)

if __name__ == '__main__':
    #init_db()
    app.run()