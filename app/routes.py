from flask import Blueprint, jsonify, request
from app.services.data_sync import DataSynchronizer
from app.models import UnifiedSign
from app import db
from geopy.distance import geodesic  # Добавлен импорт geodesic

bp = Blueprint('main', __name__)

# @bp.route('/api/sync', methods=['POST'])
# def sync_data():
#     try:
#         count = DataSynchronizer.sync_all_data()
#         return jsonify({'status': 'success', 'count': count})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @bp.route('/api/signs', methods=['GET'])
# def get_signs():
#     signs = UnifiedSign.query.filter_by(is_active=True).all()
#     return jsonify([sign.to_dict() for sign in signs])

# @bp.route('/api/signs/<int:sign_id>', methods=['GET'])
# def get_sign(sign_id):
#     sign = UnifiedSign.query.get_or_404(sign_id)
#     return jsonify(sign.to_dict())

# @bp.route('/api/signs/nearby', methods=['GET'])
# def get_nearby_signs():
#     lat = request.args.get('lat', type=float)
#     lon = request.args.get('lon', type=float)
#     radius = request.args.get('radius', default=500, type=float)  # в метрах
    
#     if not lat or not lon:
#         return jsonify({'error': 'Missing lat/lon parameters'}), 400
    
#     # Простая реализация поиска в радиусе (для продакшена нужно использовать PostGIS)
#     signs = UnifiedSign.query.filter_by(is_active=True).all()
#     nearby = []
    
#     for sign in signs:
#         dist = geodesic((lat, lon), (sign.latitude, sign.longitude)).meters
#         if dist <= radius:
#             nearby.append({**sign.to_dict(), 'distance': dist})
    
#     return jsonify(nearby)

from app.models import UnifiedSign

@bp.route('/api/sync_unified', methods=['POST'])
def sync_unified():
    try:
        count = DataSynchronizer.sync_all_data()
        return jsonify({'status': 'success', 'count': count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/api/unified_signs', methods=['GET'])
def get_unified_signs():
    signs = UnifiedSign.query.all()
    return jsonify([{
        'id': sign.id,
        'uid_gibdd': sign.uid_gibdd,
        'internal_id_comm': sign.internal_id_comm,
        'name': sign.name,
        'latitude': sign.latitude,
        'longitude': sign.longitude,
        'description': sign.description,
        'commercial_grade': sign.commercial_grade
    } for sign in signs])