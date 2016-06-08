import re
import os


EXTRACT_RE_STR = \
    r'(?P<date>\d{4}-\d{2}-\d{2})' \
    r'(?:__(?P<num>\d{,2}))?' \
    r'__' \
    r'(?P<url>\w*)\.md'

EXTRACT_RE = re.compile(EXTRACT_RE_STR, flags=re.I)
posts = {}


for root, dirs, files in os.walk('content'):
    for name in files:
        match = EXTRACT_RE.match(name)
        if match:
            full_name = os.path.join(root, name)
            posts[full_name] = match.groupdict()

print(posts)
print()
print(list(posts.keys()))