import sqlite3

from flask import g, current_app

import reimu.config


def init_db():
    pass


# class RowObject(object):
#     """Table row object."""
#     def __init__(self, row, columns):
#         for i, column in enumerate(columns):
#             setattr(self, column, row[i])


def connect():
    """Connect to database from application."""
    g.db = sqlite3.connect(current_app.config['COMMENT_DATABASE'])
    g.db.row_factory = sqlite3.Row


def disconnect():
    """Close application's database connection."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def select(query, arguments=(), single=False):
    """Select one or more rows from the database."""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    if single:
        return cursor.fetchone()
    else:
        return cursor.fetchall()


def select_one(query, arguments=()):
    """Select single row from the database."""
    return select(query, arguments, single=True)


def count(table):
    """Count all rows in given table."""
    cursor = g.db.cursor()
    cursor.execute('SELECT COUNT() FROM {};'.format(table))
    result = cursor.fetchone()[0]
    return result


def update(query, arguments=()):
    """Update a row."""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    g.db.commit()


def insert(query, arguments=()):
    """Insert a row, return it's id."""
    cursor = g.db.cursor()
    cursor.execute(query, arguments)
    g.db.commit()
    return cursor.lastrowid


def delete():
    pass