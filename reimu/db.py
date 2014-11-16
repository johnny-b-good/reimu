import sqlite3
from faker import Factory

fake = Factory.create()


def populate_db():
    """(Re)Populate blog's database with fake posts and comments."""

    connection = sqlite3.connect('reimu/blog.db')
    cursor = connection.cursor()

    # Clear tables
    cursor.execute('DELETE FROM Comments;')
    cursor.execute('DELETE FROM Posts;')

    # Insert posts (30)
    posts_query = ('INSERT INTO Posts (pid, title, created_at, content) '
                   'VALUES (?, ?, ?, ?);')
    posts_values = [(i, fake.sentence(), fake.date(), fake.text()) for i in range(30)]
    cursor.executemany(posts_query, posts_values)

    # Inser comments (7 comments per post - 210)
    comments_query = ('INSERT INTO Comments (cid, pid, author, email, created_at, content) '
                      'VALUES (?,?,?,?,?,?);')
    comments_values = [(i, i//7, fake.name(), fake.email(), fake.date(), fake.paragraph()) for i in range(210)]
    cursor.executemany(comments_query, comments_values)

    # Execute statements and close connection
    connection.commit()
    connection.close()
