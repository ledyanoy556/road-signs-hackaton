import pandas as pd
from geopy.distance import geodesic
from app.models import UnifiedSign
from app import db
from flask import current_app
from ..utils.db_connectors import DBConnector

class DataSynchronizer:
    
    @staticmethod
    def normalize_coordinates(coord):
        """Нормализация координат с валидацией диапазонов"""
        try:
            if isinstance(coord, str):
                # Для коммерческих данных: "lat,lon"
                lat, lon = map(float, coord.split(','))
            elif isinstance(coord, (tuple, list)):
                # Для данных ГИБДД: [lat, lon] в микро градусах
                lat, lon = coord[0]/1e6, coord[1]/1e6
            else:
                return None, None
            
            # Проверка валидности координат
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            return None, None
        except:
            return None, None
    
    @staticmethod
    def calculate_commercial_grade(sign, commercial_coords):
        """Определение степени пригодности для коммерции"""
        if sign['source'] == 'commercial':
            return 0  # Уже коммерческий
        return 2
        
        try:
            from geopy.distance import geodesic
            sign_coords = (sign['latitude'], sign['longitude'])
            
            min_distance = min(
                geodesic(sign_coords, (lat, lon)).meters
                for lat, lon in commercial_coords
            ) if commercial_coords else float('inf')
            
            if min_distance < 50:
                return 2
            elif min_distance < 200:
                return 1
            return 3
        except Exception as e:
            print(f"Ошибка расчета расстояния: {e}")
            return 3  # В случае ошибки считаем знак неподходящим
    
    @staticmethod
    def sync_all_data():
        try:
            # Получаем данные
            gibdd_data = DBConnector.get_gibdd_data()
            commercial_data = DBConnector.get_commercial_data()
            
            print(f"Получено {len(gibdd_data)} записей из ГИБДД и {len(commercial_data)} коммерческих")

            # Создаем словарь коммерческих данных для быстрого поиска по координатам
            commercial_dict = {}
            for _, row in commercial_data.iterrows():
                lat, lon = DataSynchronizer.normalize_coordinates(row['geo'])
                if lat and lon:
                    key = f"{lat:.6f},{lon:.6f}"  # Ключ для сравнения координат
                    commercial_dict[key] = {
                        'internal_id': row['internal_id'],
                        'description': row['description']
                    }

            # Очистка объединенной таблицы
            UnifiedSign.query.delete()

            # Обрабатываем ВСЕ знаки из ГИБДД
            for _, row in gibdd_data.iterrows():
                lat, lon = DataSynchronizer.normalize_coordinates((row['latitude'], row['longitude']))
                if lat is None or lon is None:
                    continue

                # Проверяем есть ли коммерческие данные для этих координат
                coord_key = f"{lat:.6f},{lon:.6f}"
                commercial_info = commercial_dict.get(coord_key)

                if commercial_info:
                    # Если есть коммерческие данные - статус 0 (уже используется)
                    db.session.add(UnifiedSign(
                        uid_gibdd=row['unical_id'],
                        internal_id_comm=commercial_info['internal_id'],
                        name=row['name'],
                        latitude=lat,
                        longitude=lon,
                        description=commercial_info['description'] or row['description'],
                        commercial_grade=0
                    ))
                else:
                    # Если нет коммерческих данных - статус 2 (на согласовании)
                    db.session.add(UnifiedSign(
                        uid_gibdd=row['unical_id'],
                        name=row['name'],
                        latitude=lat,
                        longitude=lon,
                        description=row['description'],
                        commercial_grade=2
                    ))

            # Добавляем коммерческие знаки, которых нет в ГИБДД (на всякий случай)
            for _, row in commercial_data.iterrows():
                lat, lon = DataSynchronizer.normalize_coordinates(row['geo'])
                if lat and lon:
                    coord_key = f"{lat:.6f},{lon:.6f}"
                    # Проверяем, не добавили ли мы уже этот знак
                    exists = UnifiedSign.query.filter_by(
                        latitude=lat, 
                        longitude=lon
                    ).first()
                    if not exists:
                        db.session.add(UnifiedSign(
                            internal_id_comm=row['internal_id'],
                            name=row['name'],
                            latitude=lat,
                            longitude=lon,
                            description=row['description'],
                            commercial_grade=0
                        ))

            db.session.commit()
            return UnifiedSign.query.count()

        except Exception as e:
            print(f"Ошибка синхронизации: {str(e)}")
            db.session.rollback()
            raise