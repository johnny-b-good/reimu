-- Таблица постов
CREATE TABLE Posts (
  pid INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME,
  content TEXT
);

CREATE UNIQUE INDEX posts__pid_index ON Posts (pid);


-- Таблица комментариев
CREATE TABLE Comments (
  cid INTEGER PRIMARY KEY AUTOINCREMENT,
  pid INTEGER NOT NULL,
  author TEXT,
  email TEXT,
  created_at DATETIME NOT NULL,
  content TEXT,

  FOREIGN KEY(pid) REFERENCES Posts(pid)
);

CREATE UNIQUE INDEX comments__cid_index ON Comments(cid);
CREATE INDEX comments__pid_index ON Comments(pid);
