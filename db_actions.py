
# MySQL курсор
def get_db_connection():
    from app import mysql
    con = mysql.connection
    cur = con.cursor()
    return con, cur

# MySQL инициализация бд
def sql_init_db():
    from app import app
    with app.app_context():
        con, cur = get_db_connection()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS tasks ( \
            id INT AUTO_INCREMENT PRIMARY KEY, \
            title VARCHAR(255), \
            description TEXT, \
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)"
        )
        cur.close()

# Запрос под представление tasks_list_get_post
def sql_tasks_list_get():
    con, cur = get_db_connection()
    cur.execute("SELECT * FROM tasks")
    data = cur.fetchall()
    cur.close()
    return data

# Запрос под представление tasks_list_get_post
def sql_tasks_list_post(title, description=None):
    con, cur = get_db_connection()
    cur.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description)
    )
    con.commit()
    cur.execute(
        "SELECT * FROM tasks WHERE title = %s",
        (title,),
    )
    data = cur.fetchall()
    cur.close()
    return data

# Запрос под представление tasks_id_get_put_delete
def sql_tasks_id_get(id):
    con, cur = get_db_connection()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    data = cur.fetchall()
    cur.close()
    return data

# Запрос под представление tasks_id_get_put_delete
def sql_tasks_id_put(id, title=None, description=None):
    con, cur = get_db_connection()
    if title is not None and description is not None:
        cur.execute(
            "UPDATE tasks SET title = %s, description = %s WHERE id = %s",
            (title, description, id),
        )
    elif title is not None:
        cur.execute(
            "UPDATE tasks SET title = %s WHERE id = %s",
            (title, id),
        )
    elif description is not None:
        cur.execute(
            "UPDATE tasks SET description = %s WHERE id = %s",
            (description, id),
        )
    con.commit()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    data = cur.fetchall()
    cur.close()
    return data

# Запрос под представление tasks_id_get_put_delete
def sql_tasks_id_delete(id):
    con, cur = get_db_connection()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    con.commit()
    cur.close()
