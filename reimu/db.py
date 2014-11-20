import sqlite3
from faker import Factory

fake = Factory.create()


def init_db():
    pass


def _fake_post_text(paragraphs_num):
    paragraphs = [fake.paragraph(nb_sentences=5) for _ in range(paragraphs_num)]
    post_text = '\n\n'.join(paragraphs)
    return post_text


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
    posts_values = [
        (i, fake.sentence(), fake.date(), _fake_post_text(7))
        for i in range(30)]
    cursor.executemany(posts_query, posts_values)

    # Inser comments (10 comments per post - 210)
    comments_query = ('INSERT INTO Comments (cid, pid, author, email, created_at, content) '
                      'VALUES (?,?,?,?,?,?);')
    comments_values = [
        (i, i//10, fake.name(), fake.email(), fake.date(), fake.paragraph())
        for i in range(300)]
    cursor.executemany(comments_query, comments_values)

    # Execute statements and close connection
    connection.commit()
    connection.close()

