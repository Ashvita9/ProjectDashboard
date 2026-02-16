from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField
from datetime import datetime

class Project(Document):
    meta = {
        'collection': 'projects',
        'db_alias': 'project_db'
    }
    name = StringField(required=True)
    description = StringField()
    owner = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    # Optional project dates
    start_date = DateTimeField()
    deployment_date = DateTimeField()

class Task(Document):
    meta = {
        'collection': 'tasks',
        'db_alias': 'project_db'
    }
    title = StringField(required=True)
    description = StringField()
    project = ReferenceField(Project, required=True)
    status = StringField(choices=['todo', 'in_progress', 'done'], default='todo')
    created_at = DateTimeField(default=datetime.utcnow)

