from re import template
from flask import Flask, render_template
from flask import (render_template, Blueprint, g, redirect,
                   request, current_app, abort, url_for)
from flask_babel import _, refresh
from app import app


locales = Blueprint('locales', __name__,
                         template_folder='templates', static_folder='static', url_prefix='/<lang_code>')

@locales.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@locales.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

@locales.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        adapter = app.url_map.bind('')
        try:
            endpoint, args = adapter.match(
                '/en' + request.full_path.rstrip('/ ?'))
            return redirect(url_for(endpoint, **args), 301)
        except:
            abort(404)

    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            abort(404)


@locales.route('/signup')
def signup():
        return render_template('signup.html')

@locales.route('/login')
def login():
        return render_template('login.html')

@locales.route('/forgot_password')
def forgot_pwd():
        return render_template('/forgot_password.html')

@locales.route('/reset_password')
def forgot_pwd_reset():
        return render_template('/forgot_password_reset.html')

@locales.route('/index')
@locales.route('/')
def index():
        return render_template('index.html')


@locales.route('/about')
def about():
        return render_template('about.html')

@locales.route('/contact')
def contact():
        return render_template('contact.html')

@locales.route('/gallery')
def gallery():
        return render_template('gallery.html')


@locales.route('/destinations')
def explore():
        return render_template('destinations.html')

@locales.route('/destinations/americas')
def americas():
        return render_template('americas.html')

@locales.route('/destinations/asia_pacific')
def asia_pacific():
        return render_template('asia_pacific.html')

@locales.route('/destinations/europe')
def europe():
        return render_template('europe.html')

@locales.route('/destinations/middle_east_africa')
def middle_east_africa():
        return render_template('middle_east_africa.html')


@locales.route('/<username>/story/<story_id>')
def show_story(username, story_id):
        return render_template('story_detail.html')

@locales.route('/<username>/my_travel_profile')
def show_travel_profile(username):
        return render_template('my_travel_profile.html')

@locales.route('/<username>/write_stories')
def write_stories(username):
        return render_template('new_stories.html')

@locales.route('/<username>/story_list')
def show_story_list(username):
        return render_template('story_list.html')

@locales.route('/<username>/edit_stories/<story_id>')
def edit_story_page(username, story_id):
        return render_template('edit_stories.html')

@locales.route('/<username>/edit_profile')
def edit_profile(username):
        return render_template('edit_profile.html')


@locales.route('/<username>/change_email')
def change_email(username):
        return render_template('change_email.html')

@locales.route('/<username>/change_password')
def change_password(username):
        return render_template('change_password.html')

@locales.route('/privacy_policy')
def privacy_policy():
        return render_template('privacy_policy.html')

@locales.route('/terms_and_conditions')
def terms_and_conditions():
        return render_template('terms_and_conditions.html')


