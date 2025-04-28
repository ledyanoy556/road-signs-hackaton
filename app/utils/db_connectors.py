import pandas as pd
from sqlalchemy import create_engine
from app.config import Config

class DBConnector:
    @staticmethod
    def get_gibdd_data():
        engine = create_engine(Config.GIBDD_DB_URI)
        query = "SELECT unical_id, name, latitude, longitude, description FROM public.sampledatabase"
        return pd.read_sql(query, engine)
    
    @staticmethod
    def get_commercial_data():
        engine = create_engine(Config.COMMERCIAL_DB_URI)
        query = "SELECT id, name, geo, description, internal_id FROM sample_table"
        return pd.read_sql(query, engine)
    
    @staticmethod
    def save_unified_data(df):
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        df.to_sql('road_signs', engine, if_exists='replace', index=False)