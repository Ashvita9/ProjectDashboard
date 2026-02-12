import os
from mongoengine import connect

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

connect(db="auth_db", alias="auth_db", host=CONNECTION_STRING)
connect(db="project_db", alias="project_db", host=CONNECTION_STRING)

