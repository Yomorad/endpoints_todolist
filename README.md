# RESTfull API для управления списком задач

## Stack:
- Flask
- MySQL
- SQLAlchemy

## Эндпоинты:

1. Создание задачи:
- Метод: POST
- URL: /tasks
- Параметры запроса: JSON-объект с полями title (строка) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

2. Получение списка задач:
- Метод: GET
- URL: /tasks
- Ответ: JSON-список задач, где каждая задача представляет собой JSON-объект с полями id, title, description, created_at, updated_at.

3. Получение информации о задаче:
- Метод: GET
- URL: /tasks/<id>
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

4. Обновление задачи:
- Метод: PUT
- URL: /tasks/<id>
- Параметры запроса: JSON-объект с полями title (строка, опционально) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

5. Удаление задачи:
- Метод: DELETE
- URL: /tasks/<id>
- Ответ: Сообщение об успешном удалении.


Требования:
1. Используйте Flask для создания веб-приложения.
2. Для хранения данных используйте MySQL.
3. Валидация данных должна быть реализована.
4. Код должен быть хорошо структурирован и сопровождаться комментариями.

Критерии оценки:
- Чистота и читаемость кода.
- Логика и структура проекта.
- Наличие и качество тестов.
- Корректная обработка ошибок.
- Документация к API (например, с использованием Swagger или другого инструмента) необязательна, но будет плюсом
    /apidocs

Дедлайн:
5 рабочих дней со дня получения задания

## Как развернуть проект:
### 1 Клонируем проект

```bash
git clone <<https://github.com/Yomorad/flask_sqlalchemy_endpoints>>
```

### 2 Настраиваем виртуальную среду
```bash
# Ставьте как удобно и грузите requirements.txt
# можно сделать через встроенный модуль venv из библиотеки python
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 3 Прописываем свои конфиги в .env
```bash
# конфиги основной бд
MYSQL_DB = 'your_database_name'
MYSQL_USER = 'your_database_user'
MYSQL_PASSWORD = 'your_database_password'
# конфиги тестовой бд, либо ставьте sqlite
TEST_MYSQL_DB = 'your_database_name'
TEST_MYSQL_USER = 'your_database_user'
TEST_MYSQL_PASSWORD = 'your_database_password'
```

### 4 Миграции
```bash
flask db init      # Инициализация системы миграции
flask db migrate   # Создание новой миграции
flask db upgrade   # Применение миграций к базе данных
```

### 5 Запуск приложения
```bash
flask run
```

### Тестирование

```bash
# из корня проекта
pytest
```