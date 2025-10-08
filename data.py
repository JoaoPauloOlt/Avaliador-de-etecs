import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'database': 'Avaliar',
    'port': 5432,
    'user': 'postgres',
    'password': 'Idopro01',
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding('UTF8')
    return conn


class Etec:
    def __init__(self, id, name, city, photo_path=""):
        self.id = id
        self.name = name
        self.city = city
        self.photo_path = photo_path

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "photo_path": self.photo_path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["city"], data.get("photo_path", ""))

class User:
    def __init__(self, username, password, name="", email="", photo_path="", user_type="student"):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.photo_path = photo_path
        self.user_type = user_type  # "student" or "teacher"

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "email": self.email,
            "photo_path": self.photo_path,
            "user_type": self.user_type
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["username"],
            data["password"],
            data.get("name", ""),
            data.get("email", ""),
            data.get("photo_path", ""),
            data.get("user_type", "student")
        )

class Rating:
    def __init__(self, id, etec_id, username, stars, comment="", date=None):
        self.id = id
        self.etec_id = etec_id
        self.username = username
        self.stars = stars  # 0-5
        self.comment = comment
        self.date = date or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "etec_id": self.etec_id,
            "username": self.username,
            "stars": self.stars,
            "comment": self.comment,
            "date": self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        date = datetime.fromisoformat(data["date"]) if "date" in data else None
        return cls(
            data.get("id"),
            data["etec_id"],
            data["username"],
            data["stars"],
            data.get("comment", ""),
            date
        )

# Data management functions
def load_etecs():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM etecs ORDER BY id")
        rows = cur.fetchall()
    conn.close()
    return [Etec(row['id'], row['name'], row['city'], row['photo_path']) for row in rows]

def save_etecs(etecs):
    # Not needed for load, but for completeness to insert
    conn = get_db_connection()
    with conn.cursor() as cur:
        for etec in etecs:
            cur.execute("INSERT INTO etecs (id, name, city, photo_path) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, city = EXCLUDED.city, photo_path = EXCLUDED.photo_path", (etec.id, etec.name, etec.city, etec.photo_path))
    conn.commit()
    conn.close()

def load_users():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
    conn.close()
    return [User(row['username'], row['password'], row['name'], row['email'], row['photo_path'], row['user_type']) for row in rows]

def save_users(users):
    conn = get_db_connection()
    with conn.cursor() as cur:
        for user in users:
            cur.execute("INSERT INTO users (username, password, name, email, photo_path, user_type) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (username) DO UPDATE SET password = EXCLUDED.password, name = EXCLUDED.name, email = EXCLUDED.email, photo_path = EXCLUDED.photo_path, user_type = EXCLUDED.user_type", (user.username, user.password, user.name, user.email, user.photo_path, user.user_type))
    conn.commit()
    conn.close()

def load_ratings():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM ratings ORDER BY date DESC")
        rows = cur.fetchall()
    conn.close()
    return [Rating(row['id'], row['etec_id'], row['username'], row['stars'], row['comment'], row['date']) for row in rows]

def save_ratings(ratings):
    conn = get_db_connection()
    with conn.cursor() as cur:
        for rating in ratings:
            cur.execute("INSERT INTO ratings (etec_id, username, stars, comment, date) VALUES (%s, %s, %s, %s, %s)", (rating.etec_id, rating.username, rating.stars, rating.comment, rating.date))
    conn.commit()
    conn.close()

def get_etec_ratings(etec_id):
    ratings = load_ratings()
    return [r for r in ratings if r.etec_id == etec_id]

def get_average_rating(etec_id):
    ratings = get_etec_ratings(etec_id)
    if not ratings:
        return 0
    return sum(r.stars for r in ratings) / len(ratings)
