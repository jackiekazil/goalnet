from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

#from flask import Blueprint, render_template, abort
#from jinja2 import TemplateNotFound

#simple_page = Blueprint('simple_page', __name__,
#                        template_folder='templates')

#@simple_page.route('/', defaults={'page': 'index'})
#@simple_page.route('/<page>')
#def show(page):
#    try:
#        return render_template('pages/%s.html' % page)
#    except TemplateNotFound:
#        abort(404)
