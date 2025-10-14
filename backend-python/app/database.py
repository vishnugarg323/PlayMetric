"""
Database configuration and MongoDB connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

# MongoDB Configuration - Railway Hosted
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:gSFyjoeBNGrWpElewAfFLzloUYmSyqRm@gondola.proxy.rlwy.net:21458")
DATABASE_NAME = os.getenv("DATABASE_NAME", "playmetric")

# Async MongoDB client for FastAPI
async_client = None
async_db = None

# Sync MongoDB client for ML operations
sync_client = None
sync_db = None


def get_async_database():
    """Get async database connection for FastAPI endpoints"""
    global async_client, async_db
    if async_db is None:
        async_client = AsyncIOMotorClient(MONGODB_URI)
        async_db = async_client[DATABASE_NAME]
    return async_db


def get_sync_database():
    """Get sync database connection for ML/batch operations"""
    global sync_client, sync_db
    if sync_db is None:
        sync_client = MongoClient(MONGODB_URI)
        sync_db = sync_client[DATABASE_NAME]
    return sync_db


def close_connections():
    """Close all database connections"""
    global async_client, sync_client
    if async_client:
        async_client.close()
    if sync_client:
        sync_client.close()
