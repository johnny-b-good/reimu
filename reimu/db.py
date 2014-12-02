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

    # Insert posts (30)
    posts_query = ('INSERT INTO Posts (pid, title, created_at, content) '
                   'VALUES (?, ?, ?, ?);')
    posts_values = [
        (i, fake.sentence(), fake.date(), _generate_fake_text(7))
        for i in range(30)]
    cursor.executemany(posts_query, posts_values)

    # Inser comments (10 comments per post - 210)
    comments_query = ('INSERT INTO Comments (cid, pid, author, email, created_at, content) '
                      'VALUES (?, ?, ?, ?, ?, ?);')
    comments_values = [
        (i, i//10, fake.name(), fake.email(), fake.date(), fake.paragraph())
        for i in range(300)]
    cursor.executemany(comments_query, comments_values)

    # Execute statements and close connection
    db.commit()
    db.close()


def connect():
    """Connect to database from application."""
    g.db = sqlite3.connect(current_app.config['DATABASE'])
    g.db.row_factory = sqlite3.Row


def disconnect():
    """Disconnect from database."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def select(query, arguments, single=False):
    """Select one or more rows from database."""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)

    if single:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()

    return result


def count(table):
    """Count all rows in given table."""
    cursor = g.db.cursor()
    cursor.execute('SELECT COUNT() FROM {};'.format(table))
    result = cursor.fetchone()[0]
    return result