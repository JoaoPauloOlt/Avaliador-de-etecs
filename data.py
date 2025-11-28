import json
import os
from datetime import datetime

DATA_DIR = 'data'
ETECS_FILE = os.path.join(DATA_DIR, 'etecs.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
RATINGS_FILE = os.path.join(DATA_DIR, 'ratings.json')


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
        self.user_type = user_type 

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
            None,
            data["etec_id"],
            data["username"],
            data["stars"],
            data.get("comment", ""),
            date
        )

def load_etecs():
    if not os.path.exists(ETECS_FILE):
        return []
    with open(ETECS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Etec.from_dict(item) for item in data]

def save_etecs(etecs):
    data = [etec.to_dict() for etec in etecs]
    with open(ETECS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [User.from_dict(item) for item in data]

def save_users(users):
    data = [user.to_dict() for user in users]
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_ratings():
    if not os.path.exists(RATINGS_FILE):
        return []
    with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Rating.from_dict(item) for item in data]

def save_ratings(ratings):
    data = [rating.to_dict() for rating in ratings]
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_etec_ratings(etec_id):
    ratings = load_ratings()
    return [r for r in ratings if r.etec_id == etec_id]

def get_average_rating(etec_id):
    ratings = get_etec_ratings(etec_id)
    if not ratings:
        return 0
    return sum(r.stars for r in ratings) / len(ratings)
