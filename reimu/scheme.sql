-- Таблица комментариев
CREATE TABLE Comments (
  cid INTEGER PRIMARY KEY AUTOINCREMENT,
  pid TEXT,
  author TEXT,
  email TEXT,
  created_at DATETIME,
  content TEXT,
  is_admin BOOLEAN,
  user_agent TEXT,
  ip_address TEXT
);

CREATE INDEX comments__pid_index ON Comments(pid);
