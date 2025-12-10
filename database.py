import sqlite3
import os

DB_FILE = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER,
            insights TEXT,
            plot_files TEXT,
            analysis_time TEXT,
            FOREIGN KEY(dataset_id) REFERENCES datasets(id)
        )
    ''')
    conn.commit()
    conn.close()

def save_dataset(filename):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO datasets (filename, upload_time) VALUES (?, datetime("now"))', (filename,))
    dataset_id = c.lastrowid
    conn.commit()
    conn.close()
    return dataset_id

def save_analysis(dataset_id, insights, plot_files):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    plot_str = ','.join(plot_files)
    c.execute('''
        INSERT INTO analyses (dataset_id, insights, plot_files, analysis_time)
        VALUES (?, ?, ?, datetime("now"))
    ''', (dataset_id, insights, plot_str))
    conn.commit()
    conn.close()
