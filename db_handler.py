import sqlite3
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def get_connection():
    return sqlite3.connect('database.db')

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                person_id TEXT NOT NULL,
                name TEXT NOT NULL,
                note TEXT,
                file VARCHAR(36),
                FOREIGN KEY(person_id) REFERENCES persons(id),
                FOREIGN KEY(file) REFERENCES files(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags_to_entry (
                entry_id TEXT NOT NULL,
                tag_id TEXT NOT NULL,
                FOREIGN KEY(entry_id) REFERENCES entries(id),
                FOREIGN KEY(tag_id) REFERENCES tags(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id VARCHAR(36) PRIMARY KEY,
                file BLOB NOT NULL
            )
        ''')
        conn.commit()

def add_entry(date, person_name, entry_name, note, tags, fileId):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM persons WHERE name = ?", (person_name,))
        person = cursor.fetchone()
        person_id = person[0]
        
        entry_id = generate_uuid()
        cursor.execute('''
            INSERT INTO entries (id, date, person_id, name, note, file)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (entry_id, date, person_id, entry_name, note, fileId))
        
        for tag in tags:
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
            tag_data = cursor.fetchone()
            tag_id = tag_data[0]
            
            cursor.execute("INSERT INTO tags_to_entry (entry_id, tag_id) VALUES (?, ?)", (entry_id, tag_id))
        
        conn.commit()

def get_entries():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.date, p.name, e.name, 
                   (SELECT GROUP_CONCAT(t.name) FROM tags t 
                    JOIN tags_to_entry te ON t.id = te.tag_id 
                    WHERE te.entry_id = e.id) AS tags,
                   e.note, e.file
            FROM entries e
            JOIN persons p ON e.person_id = p.id
            ORDER BY e.date DESC
        ''')
        return cursor.fetchall()

def get_file(file_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file FROM files WHERE id = ?", (file_id,))
        return cursor.fetchone()

def get_tags():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name 
            FROM tags
            ORDER BY lower(name)
        ''')
        return [tag[0] for tag in cursor.fetchall()]

def get_persons():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name 
            FROM persons
            ORDER BY lower(name)
        ''')
        return [val[0] for val in cursor.fetchall()]

def get_first_date():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MIN(date) as FirstDate from entries')
        return cursor.fetchone()

def add_file(file_path): 
    uuid = generate_uuid()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO files (id, file) VALUES (?, ?)", (uuid, convert_to_binary_data(file_path)))

    return uuid

def add_person(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO persons (id, name) VALUES (?,?)", (generate_uuid(), name))

def add_tag(tag):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags (id, name) VALUES (?,?)", (generate_uuid(), tag))

def convert_to_binary_data(file_path):
    with open(file_path, 'rb') as file:
        blobData = file.read()
    return blobData

