from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session
import reimu.db
import json


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
@admin.route('/admin/posts')
def posts_page():
    # Complete post list
    post_list = reimu.db.select('SELECT pid, title, created_at FROM Posts;')
    return render_template('admin.html', post_list=post_list)


@admin.route('/api/admin/posts', methods=['POST'])
def create_post():
    pass


@admin.route('/api/admin/posts/<int:post_id>', methods=['GET'])
def read_post(post_id=None):
    pass
    # if post_id:
    #     current_post = reimu.db.select('SELECT * FROM Posts WHERE pid=?;', (post_id,), single=True)
    # else:
    #     current_post = None

    # return render_template('admin.html', current_post=current_post)


@admin.route('/api/admin/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    pass


@admin.route('/api/admin/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    pass


@admin.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    pass