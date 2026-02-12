from mongoengine import Document, StringField, EmailField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(Document):
    meta = {
        'collection': 'users',
        'db_alias': 'auth_db'
    }
    username = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)    
    
    def check_password(self, password):
        return check_password_hash(self.password, password)