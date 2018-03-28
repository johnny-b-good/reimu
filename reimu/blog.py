from flask import Flask, Blueprint, g, render_template, abort, redirect, url_for, request, session
from flask import current_app as app

import reimu.db


blog = Blueprint('blog', __name__)


@blog.before_request
def before_request():
    reimu.db.connect()


@blog.teardown_request
def teardown_request(exception):
    reimu.db.disconnect()


@blog.route('/')
@blog.route('/<int:page_num>')
def index_page(page_num=0):
    """Render a blog page with posts"""

    # Get all posts for a given page, return 404 if there are none
    posts_limits = (page_num * app.config['POSTS_PER_PAGE'], app.config['POSTS_PER_PAGE'])
    posts = reimu.db.select('SELECT * FROM Posts '
                            'ORDER BY created_at DESC '
                            'LIMIT ?,?', posts_limits)
    if not posts:
        abort(404)

    # Get total posts count for pagination
    posts_count = reimu.db.count('Posts')

    # Calculate the number of pages
    if posts_count % app.config['POSTS_PER_PAGE']:
        pages_count = posts_count // app.config['POSTS_PER_PAGE'] + 1
    else:
        pages_count = posts_count // app.config['POSTS_PER_PAGE']

    return render_template('_page.html', posts=posts, posts_count=posts_count,
                           pages_count=pages_count, current_page=page_num)


@blog.route('/posts/<int:post_id>')
def post_page(post_id):
    """Render a single post if present"""

    # Try to get post's data, 404 if not found
    post = reimu.db.select('SELECT * FROM Posts WHERE pid=?;', (post_id,), single=True)
    if not post:
        abort(404)

    # Fetch all comments for that post
    comments = reimu.db.select('SELECT * FROM Comments '
                               'WHERE pid=? '
                               'ORDER BY created_at DESC;',
                               (post_id,))

    return render_template('_post.html', post=post, comments=comments)


@blog.route('/comments', methods=['POST'])
def create_comment():
    """Add new commentary.

    Available for everyone.
    """
    pass


# TODO
def archive_page(): pass
def rss_page(): pass
def sitemap_page(): pass
def static_page(): pass