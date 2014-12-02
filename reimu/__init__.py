from flask import Flask, Markup
from markdown import markdown

from reimu.blog import blog
from reimu.admin import admin
from reimu.auth import auth


# Initialize application
app = Flask(__name__)


# Load configuration
app.config.from_object('reimu.config')


# Register blueprints
app.register_blueprint(blog)
app.register_blueprint(admin)
app.register_blueprint(auth)


# Register filters
@app.template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))