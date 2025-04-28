import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # # Настройки единой PostgreSQL базы
    # SQLALCHEMY_DATABASE_URI = os.getenv('UNIFIED_DB_URI', 'postgresql://postgres:m0pK1UQl971@localhost/road_signs')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # # Настройки источников данных
    # GIBDD_DB_URI = os.getenv('GIBDD_DB_URI', 'mssql+pyodbc://postgres:m0pK1UQl971@localhost/gibdd?driver=ODBC+Driver+17+for+SQL+Server')
    # COMMERCIAL_DB_URI = os.getenv('COMMERCIAL_DB_URI', 'postgresql://postgres:m0pK1UQl971@localhost/commercial_signs')
    
    # # Параметры синхронизации
    # SYNC_RADIUS_METERS = 50  # Радиус для сопоставления знаков
    # COMMERCIAL_DATA_PRIORITY = True  # Приоритет коммерческих данных
    # Для ГИБДД (PostgreSQL)
    GIBDD_DB_URI = 'postgresql://postgres:m0pK1UQl971@localhost:5432/gibdd_db'
    
    # Для коммерческой (PostgreSQL)
    COMMERCIAL_DB_URI = 'postgresql://postgres:m0pK1UQl971@localhost:5432/commercial_db'
    
    # Общая база
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:m0pK1UQl971@localhost:5432/road_signs_db'