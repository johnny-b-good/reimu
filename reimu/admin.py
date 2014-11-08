from flask import Blueprint
import reimu.db as db

admin = Blueprint('admin', __name__)


@admin.before_request
def before_request():
    pass


@admin.teardown_request
def teardown_request(exception):
    pass


@admin.route('/admin')
def admin_page():
    pass


@admin.route('/login', methods=['GET', 'POST'])
def login():
    pass


@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


@admin.route('/admin/posts')
def posts():
    pass


@admin.route('/admin/posts', methods=['POST'])
def create_post():
    pass


@admin.route('/admin/posts/<int:post_id>', methods=['GET'])
def read_post(post_id):
    pass


@admin.route('/admin/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    pass


@admin.route('/admin/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    pass


@admin.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    pass