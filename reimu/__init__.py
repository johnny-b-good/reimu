from flask import Flask

from reimu.blog import blog
from reimu.admin import admin


# Initialize application
app = Flask(__name__)

# Load configuration
app.config.from_object('reimu.config')

# Register blueprints
app.register_blueprint(blog)
app.register_blueprint(admin)


