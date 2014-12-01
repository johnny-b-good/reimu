from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session
import sqlite3

POSTS_PER_PAGE = 10

blog = Blueprint('blog', __name__)


@blog.before_request
def before_request():
    """Connect to the database before any request"""
    g.db = sqlite3.connect('reimu/blog.db')
    g.db.row_factory = sqlite3.Row


@blog.teardown_request
def teardown_request(exception):
    """Close database connection before completing request"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@blog.route('/')
@blog.route('/<int:page_num>')
def index_page(page_num=0):
    """Render a blog page with posts"""

    # Get all posts for a given page, return 404 if there are none
    posts_limits = (page_num*POSTS_PER_PAGE, POSTS_PER_PAGE)
    posts = g.db.cursor().execute('SELECT * FROM Posts LIMIT ?,?;', posts_limits).fetchall()
    if not posts:
        abort(404)

    # Get total posts count for pagination
    # TODO - обойтись без распаковки?
    (posts_count,) = g.db.cursor().execute('SELECT COUNT() FROM Posts;').fetchone()

    # Calculate the number of pages
    if posts_count % POSTS_PER_PAGE:
        pages_count = posts_count // POSTS_PER_PAGE + 1
    else:
        pages_count = posts_count // POSTS_PER_PAGE

    return render_template('page.html', posts=posts, posts_count=posts_count,
                           pages_count=pages_count, current_page=page_num)


@blog.route('/posts/<int:post_id>')
def post_page(post_id):
    """Render a single post if present"""

    # Try to get post's data, 404 if not found
    post = g.db.cursor().execute('SELECT * FROM Posts WHERE pid=?;', (post_id,)).fetchone()
    if not post:
        abort(404)

    # Fetch all comments for that post
    comments = g.db.cursor().execute('SELECT * FROM Comments WHERE pid=?;', (post_id,)).fetchall()

    return render_template('post.html', post=post, comments=comments)


@blog.route('/login', methods=['GET'])
def login_page():
    """Render the login page"""
    return render_template('login.html')


@blog.route('/login', methods=['POST'])
def login():
    """Login as site admin."""

    # Successeful login conditions
    user_is_valid = request.form['user'] == current_app.config['USER']
    password_is_valid = request.form['password'] == current_app.config['PASSWORD']
    trap_is_empty = not request.form['trap']

    # Login user if credentials are correct
    if user_is_valid and password_is_valid and trap_is_empty:
        session['is_admin'] = True
        return redirect(url_for('blog.index_page'))
    else:
        return render_template('login.html')


@blog.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout"""
    session.pop('is_admin', None)
    return redirect(url_for('blog.index_page'))


@blog.route('/comments', methods=['POST'])
def create_comment():
    pass


# TODO
def archive_page(): pass
def rss_page(): pass
def sitemap_page(): pass
def static_page(): pass