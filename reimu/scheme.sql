-- Таблица комментариев
CREATE TABLE Comments (
  cid INTEGER PRIMARY KEY AUTOINCREMENT,
  pid TEXT,
  created_at DATETIME,
  visible BOOLEAN,
  is_admin BOOLEAN,
  author TEXT,
  email TEXT,
  content TEXT,
  ip_address TEXT
);

-- CREATE INDEX comments__pid_index ON Comments(pid);
