document.addEventListener('DOMContentLoaded', function() {
    // Инициализация карты
    const map = L.map('map').setView([55.751244, 37.618423], 12);
    
    // Добавление слоя OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Загрузка данных с сервера
    fetch('http://127.0.0.1:5000/api/unified_signs')
        .then(response => response.json())
        .then(data => {
            // Заполнение таблицы
            const tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';
            
            // Добавление маркеров на карту и строк в таблицу
            data.forEach(sign => {
                // Добавление маркера на карту
                const marker = L.marker([sign.latitude, sign.longitude]).addTo(map);
                marker.bindPopup(`
                    <b>${sign.name}</b><br>
                    ${sign.description || 'Нет описания'}<br>
                    Статус: ${getStatusText(sign.commercial_grade)}
                `);
                
                // Определение цвета маркера
                const markerColor = getMarkerColor(sign.commercial_grade);
                marker.setIcon(getCustomMarkerIcon(markerColor));
                
                // Добавление строки в таблицу
                const row = document.createElement('tr');
                row.className = `status-${sign.commercial_grade}`;
                row.innerHTML = `
                    <td>${sign.id}</td>
                    <td>${sign.name}</td>
                    <td>${sign.latitude.toFixed(6)}</td>
                    <td>${sign.longitude.toFixed(6)}</td>
                    <td>${sign.description || '-'}</td>
                    <td>${getStatusText(sign.commercial_grade)}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных:', error);
            alert('Не удалось загрузить данные. Проверьте подключение к серверу.');
        });
    
    // Функции для работы со статусами
    function getStatusText(grade) {
        const statuses = ['Используется', 'Подходит', 'Нужно согласование', 'Не подходит'];
        return statuses[grade] || 'Неизвестно';
    }
    
    function getMarkerColor(grade) {
        const colors = ['green', 'blue', 'orange', 'red'];
        return colors[grade] || 'gray';
    }
    
    function getCustomMarkerIcon(color) {
        return L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white"></div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
    }
});

// Добавьте этот код в конец файла script.js

// Функция фильтрации таблицы
function filterTable() {
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    const activeStatus = document.querySelector('[data-status].active')?.dataset.status || 'all';
    
    document.querySelectorAll('#tableBody tr').forEach(row => {
        const name = row.cells[1].textContent.toLowerCase();
        const status = row.className.includes('status-') 
            ? row.className.match(/status-(\d)/)[1] 
            : '';
        
        const matchesSearch = name.includes(searchText);
        const matchesStatus = activeStatus === 'all' || status === activeStatus;
        
        row.style.display = matchesSearch && matchesStatus ? '' : 'none';
    });
}

// Обработчики событий
document.getElementById('searchInput').addEventListener('input', filterTable);

document.querySelectorAll('[data-status]').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('[data-status]').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        filterTable();
    });
});

// Активируем кнопку "Все" по умолчанию
document.querySelector('[data-status="all"]').classList.add('active');

document.getElementById('syncButton').addEventListener('click', async () => {
    const button = document.getElementById('syncButton');
    const spinner = document.getElementById('syncSpinner');
    const status = document.getElementById('syncStatus');
    
    button.disabled = true;
    spinner.classList.remove('d-none');
    status.textContent = 'Синхронизация...';
    status.className = 'mt-2 text-info';
    
    try {
        const response = await fetch('http://localhost:5000/api/sync_unified', {
            method: 'POST'
        });
        const result = await response.json();
        
        if (result.status === 'success') {
            status.textContent = `Успешно! Обновлено ${result.count} записей`;
            status.className = 'mt-2 text-success';
            
            // Обновляем таблицу и карту после синхронизации
            loadData();
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        status.textContent = `Ошибка: ${error.message}`;
        status.className = 'mt-2 text-danger';
        console.error('Ошибка синхронизации:', error);
    } finally {
        button.disabled = false;
        spinner.classList.add('d-none');
    }
});

// Вызываем loadData() при загрузке страницы
function loadData() {
    fetch('http://127.0.0.1:5000/api/unified_signs')
        .then(response => response.json())
        .then(data => {
            updateTable(data);
            updateMap(data);
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
        });
}

// Загрузка данных при открытии страницы
document.addEventListener('DOMContentLoaded', loadData);