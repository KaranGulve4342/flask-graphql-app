from pymongo import MongoClient
from config import Config

class Database:
    """MongoDB Database connection handler"""
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        if self._client is None:
            self._client = MongoClient(Config.MONGO_URI)
            self._db = self._client[Config.DB_NAME]
            print(f"✓ Connected to MongoDB database: {Config.DB_NAME}")
        return self._db
    
    def get_collection(self, collection_name=None):
        """Get a collection from the database"""
        if self._db is None:
            self.connect()
        
        collection_name = collection_name or Config.COLLECTION_NAME
        return self._db[collection_name]
    
    def close(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("✓ Database connection closed")

# Singleton instance
db = Database()
