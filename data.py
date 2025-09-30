import json
import os
from datetime import datetime

# Data file paths
DATA_DIR = "data"
ETECS_FILE = os.path.join(DATA_DIR, "etecs.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

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
    def __init__(self, etec_id, username, stars, comment="", date=None):
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
            data["etec_id"],
            data["username"],
            data["stars"],
            data.get("comment", ""),
            date
        )

# Data management functions
def load_etecs():
    if os.path.exists(ETECS_FILE):
        with open(ETECS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Etec.from_dict(item) for item in data]
    return []

def save_etecs(etecs):
    data = [etec.to_dict() for etec in etecs]
    with open(ETECS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [User.from_dict(item) for item in data]
    return []

def save_users(users):
    data = [user.to_dict() for user in users]
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Rating.from_dict(item) for item in data]
    return []

def save_ratings(ratings):
    data = [rating.to_dict() for rating in ratings]
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_etec_ratings(etec_id):
    ratings = load_ratings()
    return [r for r in ratings if r.etec_id == etec_id]

def get_average_rating(etec_id):
    ratings = get_etec_ratings(etec_id)
    if not ratings:
        return 0
    return sum(r.stars for r in ratings) / len(ratings)

def initialize_sample_data():
    # Initialize with some sample Etecs from São Paulo
    etecs = [
        Etec(1, "ETEC de São Paulo", "São Paulo", "photos/etec_sp.jpg"),
        Etec(2, "ETEC de Campinas", "Campinas", "photos/etec_campinas.jpg"),
        Etec(3, "ETEC de Santos", "Santos", "photos/etec_santos.jpg"),
        Etec(4, "ETEC de Ribeirão Preto", "Ribeirão Preto", "photos/etec_rp.jpg"),
        Etec(5, "ETEC de São José dos Campos", "São José dos Campos", "photos/etec_sjc.jpg")
    ]
    save_etecs(etecs)

    # Initialize with default admin user
    users = [User("admin", "123", "Administrador", "admin@etec.sp.gov.br", "", "teacher")]
    save_users(users)

    # Create photos directory
    os.makedirs("photos", exist_ok=True)

# Initialize data if files don't exist
if not os.path.exists(ETECS_FILE):
    initialize_sample_data()
