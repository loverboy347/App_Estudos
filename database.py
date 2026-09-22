import sqlite3, json
from pathlib import Path
from datetime import datetime

DB=Path(__file__).resolve().parent.parent/"questions.db"

def connect():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    c=connect()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS questions(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      external_id TEXT UNIQUE,
      discipline TEXT NOT NULL,
      topic TEXT,
      subtopic TEXT,
      institution TEXT,
      qtype TEXT NOT NULL,
      original_number TEXT,
      source_url TEXT NOT NULL,
      source_title TEXT,
      answer TEXT NOT NULL,
      statement TEXT NOT NULL,
      affirmations_json TEXT NOT NULL,
      alternatives_json TEXT NOT NULL,
      image TEXT,
      notes TEXT,
      status TEXT NOT NULL DEFAULT 'candidate',
      created_at TEXT NOT NULL,
      reviewed_at TEXT
    );
    CREATE TABLE IF NOT EXISTS decisions(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      question_id INTEGER NOT NULL,
      decision TEXT NOT NULL,
      reason TEXT,
      created_at TEXT NOT NULL
    );
    """)
    c.commit(); c.close()

def insert(q):
    c=connect()
    cur=c.execute("""INSERT OR IGNORE INTO questions
    (external_id,discipline,topic,subtopic,institution,qtype,original_number,
     source_url,source_title,answer,statement,affirmations_json,alternatives_json,
     image,notes,status,created_at)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
      q.get("id"),q["disciplina"],q.get("tema"),q.get("subtema"),q["instituicao"],
      q["tipo"],q.get("numero_original"),q["fonte"],q.get("source_title"),
      q["gabarito"],q["enunciado"],json.dumps(q.get("afirmativas",[]),ensure_ascii=False),
      json.dumps(q.get("alternativas",[]),ensure_ascii=False),q.get("imagem"),
      q.get("observacoes",""),q.get("status","candidate"),datetime.now().isoformat()))
    c.commit(); i=cur.lastrowid; c.close(); return i

def rows(where=""):
    c=connect(); r=c.execute("SELECT * FROM questions "+where).fetchall(); c.close(); return [dict(row) for row in r]

def set_status(i,status):
    c=connect(); c.execute("UPDATE questions SET status=?,reviewed_at=? WHERE id=?",
        (status,datetime.now().isoformat(),i)); c.commit(); c.close()

def decision(i,d,reason=""):
    c=connect(); c.execute(
        "INSERT INTO decisions(question_id,decision,reason,created_at) VALUES(?,?,?,?)",
        (i,d,reason,datetime.now().isoformat())); c.commit(); c.close()
