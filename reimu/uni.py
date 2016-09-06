# ------------------------------ Standard modules ------------------------------
from datetime import datetime
import os
import re

# ------------------------------ Extra modules ------------------------------
from flask import Flask, Markup, Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session
from markdown import markdown

# ------------------------------ App modules ------------------------------
import db


# ------------------------------ App init ------------------------------
app = Flask(__name__)
app.config.from_object('config')

EXTRACT_RE_STR = r'(?P<date>\d{4}-\d{2}-\d{2})(?:__(?P<num>\d{0,2}))?__(?P<url>\w*)\.md'

EXTRACT_RE = re.compile(EXTRACT_RE_STR, flags=re.I)

post_dict = {}
post_list = []

for root, dirs, files in os.walk('content'):
    for name in files:
        match = EXTRACT_RE.match(name)
        if match:
            post_data = match.groupdict()
            post_data.update({
                'path': os.path.join(root, name)
            })
            index_key = '{date}__{url}'.format(**post_data)
            post_dict[index_key] = post_data
            post_list.append(index_key)

post_list.sort(reverse=True)

print(post_index)
print(posts)


# ------------------------------ Request handlers ------------------------------
@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def teardown_request(exception):
    db.disconnect()


# ------------------------------ Template filters ------------------------------
@app.template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@app.template_filter('ru_date')
def ru_date_filter(data):
    return datetime.strptime(data, '%Y-%m-%d').strftime('%d.%m.%Y')


# ------------------------------ Auth routes ------------------------------
@app.route('/login', methods=['GET'])
def login_page():
    """Render the login page."""
    if session.get('is_admin', False):
        return redirect(url_for('index_page'))
    else:    
        return render_template('auth.html')


@app.route('/login', methods=['POST'])
def login():
    """Login as blog admin."""

    # Successeful login conditions
    user_is_valid = (request.form['user'] == current_app.config['USER'])
    password_is_valid = (request.form['password'] == current_app.config['PASSWORD'])
    trap_is_empty = (not request.form['trap'])

    # Login user if credentials are correct
    if user_is_valid and password_is_valid and trap_is_empty:
        session['is_admin'] = True
        return redirect(url_for('index_page'))
    else:
        return render_template('auth.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout."""
    session.pop('is_admin', None)
    return redirect(url_for('index_page'))


# ------------------------------ Page routes ------------------------------
@app.route('/')
@app.route('/<int:page_num>')
def index_page(page_num=0):
    """Render a blog page with posts"""

    # # Get all posts for a given page, return 404 if there are none
    # posts_limits = (page_num*config.POSTS_PER_PAGE, config.POSTS_PER_PAGE)
    # posts = reimu.db.select('SELECT * FROM Posts '
    #                         'ORDER BY created_at DESC '
    #                         'LIMIT ?,?', posts_limits)
    # if not posts:
    #     abort(404)

    # # Get total posts count for pagination
    # posts_count = reimu.db.count('Posts')

    # # Calculate the number of pages
    # if posts_count % POSTS_PER_PAGE:
    #     pages_count = posts_count // POSTS_PER_PAGE + 1
    # else:
    #     pages_count = posts_count // POSTS_PER_PAGE



    return render_template('_page.html', posts=posts, posts_count=posts_count,
                           pages_count=pages_count, current_page=page_num)


@app.route('/posts/<date>/<url>')
def post_page(date, url):
    """Render a single post if present"""

    # Try to get post's data, 404 if not found
    index_key = '{date}__{url}'.format(date, url)
    post = post_dict.get(index_key, none)
    if not post:
        abort(404)

    # Fetch all comments for that post
    comments = reimu.db.select('SELECT * FROM Comments '
                               'WHERE pid=? '
                               'ORDER BY created_at DESC;',
                               (index_key,))

    return render_template('post.html', post=post, comments=comments)


# ------------------------------ Comment routes ------------------------------
@app.route('/comments', methods=['POST'])
def create_comment():
    """Add new commentary."""
    pass


# ------------------------------ TODO routes ------------------------------
def archive_page(): pass
def rss_page(): pass
def sitemap_page(): pass
def static_page(): pass    