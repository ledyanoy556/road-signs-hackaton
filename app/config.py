import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Для ГИБДД (PostgreSQL)
    GIBDD_DB_URI = 'postgresql://postgres:password@localhost:5432/gibdd_db'
    
    # Для коммерческой (PostgreSQL)
    COMMERCIAL_DB_URI = 'postgresql://postgres:password@localhost:5432/commercial_db'
    
    # Общая база
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/road_signs_db'