from flask import g, current_app
from faker import Factory
import sqlite3

import reimu.config

fake = Factory.create()


def init_db():
    pass


def _generate_fake_text(paragraphs_num):
    """Generate fake post text."""
    paragraphs = [fake.paragraph(nb_sentences=5) for _ in range(paragraphs_num)]
    post_text = '\n\n'.join(paragraphs)
    return post_text


def populate_db():
    """(Re)Populate blog's database with fake posts and comments.

    This function shold be called from interactive shell.
    """

    # Connect to the database
    db = sqlite3.connect(reimu.config.DATABASE)
    cursor = db.cursor()

    # Clear tables
    cursor.execute('DELETE FROM Comments;')
    cursor.execute('DELETE FROM Posts;')

    # Create and insert posts (30)
    posts_query = (
        'INSERT INTO Posts (pid, title, content, created_at, updated_at, is_published) '
        'VALUES (?, ?, ?, ?, ?, ?);')
    posts_values = [
        (i, fake.sentence(), _generate_fake_text(7), fake.date(), None, True)
        for i in range(30)]
    cursor.executemany(posts_query, posts_values)

    # Create and insert comments (10 comments per post - 300)
    comments_query = ('INSERT INTO Comments (cid, pid, author, email, created_at, content) '
                      'VALUES (?, ?, ?, ?, ?, ?);')
    comments_values = [
        (i, i//10, fake.name(), fake.email(), fake.date(), fake.paragraph())
        for i in range(300)]
    cursor.executemany(comments_query, comments_values)

    # Execute statements and close connection
    db.commit()
    db.close()


class RowObject(object):
    """Table row object."""
    def __init__(self, row, columns):
        for i, column in enumerate(columns):
            setattr(self, column, row[i])


def connect():
    """Connect to database from application."""
    g.db = sqlite3.connect(current_app.config['DATABASE'])


def disconnect():
    """Close application's database connection."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def select(query, arguments=(), single=False, row_type='object'):
    """Select one or more rows from database."""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    rows = cursor.fetchall()

    # Convert rows to desired type
    column_names = [col[0] for col in cursor.description]
    if row_type == 'object':
        rows = [RowObject(row, column_names) for row in rows]
    elif row_type == 'dict':
        rows = [dict(zip(column_names, row)) for row in rows]

    if single:
        return rows[0] if len(rows) else None
    else:
        return rows


def count(table):
    """Count all rows in given table."""
    cursor = g.db.cursor()
    cursor.execute('SELECT COUNT() FROM {};'.format(table))
    result = cursor.fetchone()[0]
    return result


def update(query, arguments=()):
    """Update a row"""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    g.db.commit()


def insert(query, arguments=()):
    """Insert a row, return it's id"""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    g.db.commit()
    return cursor.lastrowid