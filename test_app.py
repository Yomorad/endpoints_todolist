import os
from dotenv import load_dotenv
import pytest
from app import app, db

load_dotenv()
db_name = os.getenv("TEST_MYSQL_DB")
db_user = os.getenv("TEST_MYSQL_USER")
db_password = os.getenv("TEST_MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Фикстура для настройки тестовой среды
@pytest.fixture
def client():
    # Настройка приложения на использование SQLite в памяти для тестов
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Создаем контекст приложения
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        yield app.test_client()  # Возвращаем тестовый клиент

        # После тестов удаляем все таблицы
        db.session.remove()
        db.drop_all()

# Тест для проверки GET запроса на получение списка задач
def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == []  # Так как задач еще нет

# Тест для создания новой задачи через POST запрос
def test_create_task(client):
    # Отправляем POST запрос с новой задачей
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    
    assert response.status_code == 201
    data = response.json
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'

# Тест для получения задачи по ID
def test_get_task_by_id(client):
    # Сначала создаем новую задачу
    client.post('/tasks', json={
        'title': 'Another Test Task',
        'description': 'Another test task'
    })
    
    # Теперь получаем задачу по ID (1)
    response = client.get('/tasks/1')
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'Another Test Task'
    assert data['description'] == 'Another test task'

# Тест для обновления задачи через PUT запрос
def test_update_task(client):
    # Сначала создаем задачу
    client.post('/tasks', json={
        'title': 'Task to be updated',
        'description': 'Task description'
    })
    
    # Теперь обновляем задачу
    response = client.put('/tasks/1', json={
        'title': 'Updated Task',
        'description': 'Updated description'
    })
    
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'Updated Task'
    assert data['description'] == 'Updated description'

# Тест для удаления задачи через DELETE запрос
def test_delete_task(client):
    # Сначала создаем задачу
    client.post('/tasks', json={
        'title': 'Task to be deleted',
        'description': 'Task description'
    })
    
    # Удаляем задачу
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'

    # Проверяем, что задачи больше нет
    response = client.get('/tasks/1')
    assert response.status_code == 404
