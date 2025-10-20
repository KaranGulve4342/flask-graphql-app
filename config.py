import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    MONGO_URI = os.getenv('MONGO_URI')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database configuration
    DB_NAME = os.getenv('DB_NAME', 'graphql')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'users')
