import sqlite3
import json

from flask import g, current_app

import reimu.config


def init_db():
    pass


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
    columns = [col[0] for col in cursor.description]
    if row_type == 'object':
        rows = [RowObject(row, columns) for row in rows]
    elif row_type == 'dict':
        rows = [dict(zip(columns, row)) for row in rows]

    # Unpack list if needed
    if single:
        return rows[0] if len(rows) else None
    else:
        return rows if len(rows) else []


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
