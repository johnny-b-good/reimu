from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session

import reimu.db


admin = Blueprint('admin', __name__)


@admin.before_request
def before_request():
    if not session.get('is_admin'):
        return redirect(url_for('blog.index_page'))

    reimu.db.connect()



@admin.teardown_request
def teardown_request(exception):
    reimu.db.disconnect()


@admin.route('/admin')
def admin_page():
    return ''


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