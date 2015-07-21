from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session, jsonify, Response
import json

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
# @admin.route('/admin/posts')
# @admin.route('/admin/posts/new')
# @admin.route('/admin/posts/<int:post_id>')
def posts_page(post_id=None):
    return render_template('admin.html')


@admin.route('/admin/api/posts', methods=['GET'])
def posts_list():
    posts = reimu.db.select(
        'SELECT pid, title, created_at, updated_at, is_published FROM Posts '
        'ORDER BY created_at DESC;',
        row_type='dict')

    return Response(json.dumps(posts), mimetype='application/json')


@admin.route('/admin/api/posts', methods=['POST'])
def create_post():
    query_arguments = (
        request.json.get('title', None),
        request.json.get('content', None),
        request.json.get('created_at', None),
        request.json.get('is_published', None)
    )

    new_pid = reimu.db.insert(
        'INSERT INTO Posts (title, content, created_at, is_published) '
        'VALUES (?, ?, ?, ?) ', query_arguments)

    return Response(json.dumps({'pid': new_pid}), mimetype='application/json')


@admin.route('/admin/api/posts/<int:post_id>', methods=['GET'])
def read_post(post_id=None):
    post = reimu.db.select(
        'SELECT * FROM Posts WHERE pid=? ORDER BY created_at DESC;', (post_id,),
        row_type='dict', single=True)

    if not post:
        abort(404)

    return jsonify(post)


@admin.route('/admin/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    query_arguments = (
        request.json.get('title', None),
        request.json.get('content', None),
        request.json.get('created_at', None),
        request.json.get('is_published', None),
        request.json.get('pid', None)
    )

    reimu.db.update(
        'UPDATE Posts '
        'SET title=?, content=?, created_at=?, is_published=? '
        'WHERE pid=?;', query_arguments)

    return Response('{}', mimetype='application/json')


@admin.route('/admin/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    pass


@admin.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    pass
