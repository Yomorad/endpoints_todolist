import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from flask_migrate import Migrate

app = Flask(__name__)

# MySQL Configuration
load_dotenv()
db_name = os.getenv("MYSQL_DB")
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)  # Инициализация Marshmallow для валидации и сериализации

# Определение модели
class Task(db.Model):
    """
    Модель для задач.

    Attributes:
        id (int): Уникальный идентификатор задачи.
        title (str): Название задачи (обязательно).
        description (str): Описание задачи (необязательно).
        created_at (datetime): Время создания задачи.
        updated_at (datetime): Время последнего обновления задачи.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Схема для валидации и сериализации задач
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

# Создание схемы для одиночной и множественной сериализации
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Инициализация Swagger для документирования API
swagger = Swagger(app)

@app.route("/tasks", methods=["GET", "POST"])
def tasks_list_get_post():
    """
    Обрабатывает запросы для получения списка задач и добавления новой задачи.

    Returns:
        list: Список задач (при GET-запросе) или объект новой задачи (при POST-запросе).
    """
    
    if request.method == "GET":
        tasks = Task.query.all()
        return tasks_schema.dump(tasks), 200  # Используем сериализацию

    elif request.method == "POST":
        errors = task_schema.validate(request.json)  # Валидация входных данных
        if errors:
            return {"error": errors}, 400  # Возвращаем ошибки валидации
        task = task_schema.load(request.json)  # Загружаем данные
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201  # Возвращаем сериализованный объект

@app.route("/tasks/<int:id>", methods=["GET", "PUT", "DELETE"])
def tasks_id_get_put_delete(id):
    """
    Обрабатывает запросы для получения, обновления и удаления конкретной задачи по ID.

    Args:
        id (int): Уникальный идентификатор задачи.

    Returns:
        dict: Объект задачи или сообщение об ошибке.
    """
    task = db.session.get(Task, id)
    if not task:
        return {"error": "Task not found"}, 404

    if request.method == "GET":
        return task_schema.dump(task), 200

    elif request.method == "PUT":
        errors = task_schema.validate(request.json)  # Валидация входных данных
        if errors:
            return {"error": errors}, 400  # Возвращаем ошибки валидации
        task = task_schema.load(request.json, instance=task)  # Обновляем экземпляр
        db.session.commit()
        return task_schema.dump(task), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}, 200

if __name__ == "__main__":
    app.run(debug=True)
