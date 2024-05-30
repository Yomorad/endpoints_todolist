from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flasgger import Swagger

from db_actions import *

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "example"
app.config["MYSQL_PASSWORD"] = "example"
app.config["MYSQL_DB"] = "example"

mysql = MySQL(app)

# Инициализация Swagger
swagger = Swagger(app)

@app.route("/tasks", methods=["GET", "POST"])
def tasks_list_get_post():
    """
    Получить, добавить список всех задач
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      200:
        description: Успешный запрос. Возвращает список задач.
    """
    if request.method == "GET":
        # берём данные из бд
        data = sql_tasks_list_get()
        return jsonify(data)
    elif request.method == "POST":
        # проверяем наличие требуемого поля в запросе
        if "title" not in request.json:
            return jsonify({"error": "Title is required"}), 400
        # берём данные из запроса
        title = request.json["title"]
        description = request.json.get("description")
        # добавляем данные в бд
        data = sql_tasks_list_post(title, description)
        return jsonify(data)

@app.route("/tasks/<int:id>", methods=["GET", "PUT", "DELETE"])
def tasks_id_get_put_delete(id):
    """
    Получить, обновить или удалить задачу по ее ID
    ---
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: ID задачи
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      200:
        description: Успешный запрос. Возвращает данные задачи.
      400:
        description: Некорректный запрос.
    """
    if request.method == "GET":
        # берём данные из бд
        data = sql_tasks_id_get(id)
        return jsonify(data)
    elif request.method == "PUT":
        # проверяем наличие требуемых полей в запросе
        if ("title" not in request.json) and ("description" not in request.json):
            return jsonify({"error": "Title and description are required"}), 400
        # берём данные из запроса
        title = request.json.get("title")
        description = request.json.get("description")
        # обновляем данные в бд
        data = sql_tasks_id_put(id, title, description)
        return jsonify(data)
    elif request.method == "DELETE":
        # удаляем данные из бд
        data = sql_tasks_id_delete(id)
        return jsonify({"message": "Task deleted successfully"})

if __name__ == "__main__":
    # инициализируем бд, если ее нет
    sql_init_db()
    app.run(debug=True)