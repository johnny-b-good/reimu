import json
import re
from datetime import datetime

from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session, Response

import reimu.db

admin = Blueprint('admin', __name__)


class JSONResponse(Response):
    """ JSONified response object.

        A simple convinience wrapper for standard flask.Response class.
        flask.jsonify is not used because of it's paranoic security feature
        which breaks BackboneJS collections.
        See http://flask.pocoo.org/docs/0.10/security/#json-security
    """
    def __init__(self, response_data):
        json_string = json.dumps(response_data)
        super(JSONResponse, self).__init__(json_string, mimetype='application/json')


def convert_date(date, direction):
    """ Convert dates between Russian (%d.%m.%Y) and US (%Y-%m-%d) formats. """
    try:
        if direction == 'us_to_ru':
            return datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
        elif direction == 'ru_to_us':
            return datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
        else:
            return None
    except ValueError:
        return None


@admin.before_request
def before_request():
    if not session.get('is_admin'):
        return redirect(url_for('blog.index_page'))
    reimu.db.connect()


@admin.teardown_request
def teardown_request(exception):
    reimu.db.disconnect()


@admin.route('/admin')
def posts_page(post_id=None):
    return render_template('admin.html')


@admin.route('/admin/api/posts', methods=['GET'])
def posts_list():
    posts = reimu.db.select(
        'SELECT pid, title, created_at, updated_at, is_published FROM Posts '
        'ORDER BY created_at DESC;',
        row_type='dict')

    for p in posts:
        p['created_at'] = convert_date(p['created_at'], 'us_to_ru')

    return JSONResponse(posts)


@admin.route('/admin/api/posts', methods=['POST'])
def create_post():
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    created_at = request.json.get('created_at', None)
    is_published = request.json.get('is_published', None)

    # Check for empty fields
    for param in [title, content, created_at]:
        if not param:
            return JSONResponse({'error': 'Ошибка: пустое поле'}), 422

    # Check for correct date
    print(created_at, re.match(created_at, '\d{2}\.\d{2}\.\d{4}'))
    if not re.match(r'\d{2}\.\d{2}\.\d{4}', created_at):
        return JSONResponse({'error': 'Ошибка: некорректная дата'}), 422

    # Convert date
    created_at = convert_date(created_at, 'ru_to_us')

    # Save changes
    query_arguments = (title, content, created_at, is_published)
    new_pid = reimu.db.insert(
        'INSERT INTO Posts (title, content, created_at, is_published) '
        'VALUES (?, ?, ?, ?) ', query_arguments)

    return JSONResponse({'pid': new_pid})


@admin.route('/admin/api/posts/<int:post_id>', methods=['GET'])
def read_post(post_id=None):
    post = reimu.db.select(
        'SELECT * FROM Posts '
        'WHERE pid=? '
        'ORDER BY created_at DESC;',
        (post_id,),
        row_type='dict', single=True
    )

    if not post:
        abort(404)

    post['created_at'] = convert_date(post['created_at'], 'us_to_ru')

    return JSONResponse(post)


@admin.route('/admin/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    created_at = request.json.get('created_at', None)
    is_published = request.json.get('is_published', None)
    title = request.json.get('title', None)
    pid = request.json.get('pid', None)

    # Check for empty fields
    for param in [title, content, created_at, pid]:
        if not param:
            return JSONResponse({'error': 'Ошибка: пустое поле'}), 422

    # Check for correct date
    if not re.match('\d{2}\.\d{2}\.\d{4}', created_at):
        return JSONResponse({'error': 'Ошибка: некорректная дата'}), 422

    # Convert date
    created_at = convert_date(created_at, 'ru_to_us')

    # Save changes
    query_arguments = (title, content, created_at, is_published, pid)
    reimu.db.update(
        'UPDATE Posts '
        'SET title=?, content=?, created_at=?, is_published=? '
        'WHERE pid=?;', query_arguments)

    return JSONResponse({})


@admin.route('/admin/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    pass


@admin.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    pass
