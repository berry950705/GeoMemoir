from flask import Flask, request, g, redirect, url_for
from flask_babel import Babel, Domain
from config import Config

# set up application
app = Flask(__name__)
app.config.from_object(Config)

# import and register blueprints
from app.routes import locales
app.register_blueprint(locales)

# set up babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(
            app.config['LANGUAGES']) or app.config['LANGUAGES'][0]

        print(g.lang_code)
    return g.lang_code


@app.route('/')
def home():
    if not g.get('lang_code', None):
        get_locale()
    return redirect('https://geomemoir.fun/en/')
    #return redirect(url_for('locales.index'))
