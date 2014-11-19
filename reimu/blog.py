from flask import Blueprint, g, render_template, abort, redirect, url_for
import sqlite3

POSTS_PER_PAGE = 10

blog = Blueprint('blog', __name__)



@blog.before_request
def before_request():
    g.db = sqlite3.connect('reimu/blog.db')
    g.db.row_factory = sqlite3.Row


@blog.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@blog.route('/')
@blog.route('/<int:page>')
def blog_page(page=0):

    posts = g.db.cursor().execute('SELECT * FROM Posts;').fetchall()

    # TODO - обойтись без распаковки?
    (posts_count,) = g.db.cursor().execute('SELECT COUNT() FROM Posts;').fetchone()

    if posts_count % POSTS_PER_PAGE:
        pages_count = posts_count // POSTS_PER_PAGE + 1
    else:
        pages_count = posts_count // POSTS_PER_PAGE

    return render_template('page.html', posts=posts, posts_count=posts_count,
                           pages_count=pages_count, current_page=page)


@blog.route('/posts/<int:post_id>')
def read_post(post_id):
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