from flask import Blueprint
import reimu.db as db

blog = Blueprint('blog', __name__)


@blog.before_request
def before_request():
    pass


@blog.teardown_request
def teardown_request(exception):
    pass


@blog.route('/')
@blog.route('/<int:page>')
def blog_page(page=0):
    pass


@blog.route('/posts')
@blog.route('/posts/<int:post_id>')
def read_post(post_id):
    pass


@blog.route('/comments', methods=['POST'])
def create_comment():
    pass



# TODO
def archive_page(): pass
def rss_page(): pass
def sitemap_page(): pass
def static_page(): pass