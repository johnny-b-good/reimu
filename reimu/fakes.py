import sqlite3
import random

from faker import Factory


fake = Factory.create()


def value_or_none(value, chance):
    """Randomly return specified value or None."""
    dice = random.randint(0, 100)
    if dice <= chance:
        return value
    else:
        return None



def _generate_fake_text(paragraphs_num):
    """Generate fake post text."""
    paragraphs = [fake.paragraph(nb_sentences=5) for _ in range(paragraphs_num)]
    post_text = '\n\n'.join(paragraphs)
    return post_text


def populate_db():
    """(Re)Populate blog's database with fake posts and comments.

    This function should be called from interactive shell.
    """

    # Connect to the database
    db = sqlite3.connect(reimu.config.DATABASE)
    cursor = db.cursor()

    # Clear tables
    cursor.execute('DELETE FROM Comments;')
    cursor.execute('DELETE FROM Posts;')

    # Create and insert posts (30)
    posts_query = ("""
        INSERT INTO Posts (pid, title, content, created_at, updated_at, is_published)
        VALUES (?, ?, ?, ?, ?, ?);
    """)
    posts_values = [
        (
            i,  # pid
            fake.sentence(),  # title
            _generate_fake_text(7),  # content
            fake.date(), # created_at
            None,  # updated_at
            True  # is_published
        )
        for i in range(30)]
    cursor.executemany(posts_query, posts_values)

    # Create and insert comments (10 comments per post - 300)
    comments_query = ("""
        INSERT INTO Comments (cid, pid, author, email, created_at, content, user_agent, ip_address, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """)
    comments_values = [
        (
            i,  # cid
            i//10,  # pid
            fake.name(),  # author
            value_or_none(fake.free_email(), 30),  # email
            fake.date(),  # created_at
            fake.paragraph(),  # content
            fake.user_agent(),  # user_agent
            fake.ipv4(),  # ip_address
            random.choice([True, False]) #is_admin
        )
        for i in range(300)]
    cursor.executemany(comments_query, comments_values)

    # Execute statements and close connection
    db.commit()
    db.close()
