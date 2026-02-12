import os
from mongoengine import connect

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

try:
    connect(
        db="auth_db", 
        alias="auth_db", 
        host=CONNECTION_STRING,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        retryWrites=True,
        w='majority'
    )
    connect(
        db="project_db", 
        alias="project_db", 
        host=CONNECTION_STRING,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        retryWrites=True,
        w='majority'
    )
    print("✓ Connected to MongoDB Atlas successfully")
except Exception as e:
    print(f"✗ MongoDB Connection Error: {str(e)}")
    print("Please check:")
    print("1. Your internet connection")
    print("2. MongoDB Atlas cluster is running")
    print("3. Your IP address is whitelisted in MongoDB Atlas")
    print("4. Firewall is not blocking MongoDB connections")

