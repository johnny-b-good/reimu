-- Таблица постов
CREATE TABLE Posts (
  pid INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  content TEXT,
  created_at DATETIME,
  updated_at DATETIME,
  is_published BOOLEAN
);

CREATE UNIQUE INDEX posts__pid_index ON Posts (pid);


-- Таблица комментариев
CREATE TABLE Comments (
  cid INTEGER PRIMARY KEY AUTOINCREMENT,
  pid INTEGER NOT NULL,
  author TEXT,
  email TEXT,
  created_at DATETIME,
  content TEXT,
  user_agent TEXT,
  ip_address TEXT,
  is_admin BOOLEAN

  FOREIGN KEY(pid) REFERENCES Posts(pid)
);

CREATE UNIQUE INDEX comments__cid_index ON Comments(cid);
CREATE INDEX comments__pid_index ON Comments(pid);
