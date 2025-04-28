from app import db
from datetime import datetime

# class RoadSign(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     original_id = db.Column(db.String(50))  # ID из исходной системы
#     name = db.Column(db.String(255))
#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     description = db.Column(db.Text)
#     source = db.Column(db.String(20))  # 'gibdd' или 'commercial'
#     is_active = db.Column(db.Boolean, default=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'original_id': self.original_id,
#             'name': self.name,
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'description': self.description,
#             'source': self.source,
#             'is_active': self.is_active
#         }
####    
class UnifiedSign(db.Model):
    __tablename__ = 'unified_signs'
    
    id = db.Column(db.Integer, primary_key=True)
    uid_gibdd = db.Column(db.Integer, nullable=True)  # ID из ГИБДД
    internal_id_comm = db.Column(db.String(50), nullable=True)  # ID из коммерческой базы
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    commercial_grade = db.Column(db.SmallInteger, default=3)  # 0-3 как в требованиях
    
    def __repr__(self):
        return f'<UnifiedSign {self.name}>'