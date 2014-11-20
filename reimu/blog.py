from flask import Blueprint, g, render_template, abort, redirect, url_for
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
def page(page_num=0):
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
def read_post(post_id):
    """Render a single post if present"""

    # Try to get post's data, 404 if not found
    post = g.db.cursor().execute('SELECT * FROM Posts WHERE pid=?;', (post_id,)).fetchone()
    if not post:
        abort(404)

    # Fetch all comments for that post
    comments = g.db.cursor().execute('SELECT * FROM Comments WHERE pid=?;', (post_id,)).fetchall()

    return render_template('post.html', post=post, comments=comments)


@blog.route('/comments', methods=['POST'])
def create_comment():
    pass



# TODO
def archive_page(): pass
def rss_page(): pass
def sitemap_page(): pass
def static_page(): pass