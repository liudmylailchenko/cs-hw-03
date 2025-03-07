import psycopg2
from config import db_config

sql_queries = [
    # Отримати всі завдання певного користувача за його user_id.
    """
    SELECT * FROM tasks
    WHERE user_id = 3;
    """,
    # Вибрати завдання за певним статусом
    """
    SELECT * FROM tasks
    WHERE status_id = (SELECT id FROM status WHERE name = 'to do');
    """,
    # Оновити статус конкретного завдання
    """
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = 'in progress')
    WHERE id = 2;
    """,
    # Отримати список користувачів, які не мають жодного завдання
    """
    SELECT * FROM users
    WHERE id NOT IN (SELECT user_id FROM tasks);
    """,
    # Додати нове завдання для конкретного користувача.
    """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES ('New Task', 'Description', 1, 3);
    """,
    # Отримати всі завдання, які ще не завершено
    """
    SELECT * FROM tasks
    WHERE status_id != (SELECT id FROM status WHERE name = 'done');
    """,
    # Видалити конкретне завдання
    """
    DELETE FROM tasks
    WHERE id = 2;
    """,
    # Знайти користувачів з певною електронною поштою.
    """
    SELECT * FROM users
    WHERE email = 'test@example.com';"
    """,
    # Оновити ім'я користувача.
    """
    UPDATE users
    SET fullname = 'New Name'
    WHERE id = 1;
    """,
    # Отримати кількість завдань для кожного статусу.
    """
    SELECT status.name, COUNT(*) AS task_count
    FROM tasks
    JOIN status ON tasks.status_id = status.id
    GROUP BY status.name;
    """,
    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    """
    SELECT * FROM tasks
    WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@example.com');
    """,
    # Отримати список завдань, що не мають опису.
    """
    SELECT * FROM tasks
    WHERE description IS NULL;
    """,
    # Вибрати користувачів та їхні завдання, які є у статусі
    """
    SELECT users.fullname, tasks.title
    FROM users
    JOIN tasks ON users.id = tasks.user_id
    WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
    """,
    # Отримати користувачів та кількість їхніх завдань.
    """
    SELECT users.fullname, COUNT(tasks.id) AS task_count
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.fullname;
    """,
]


def execute_sql_query(sql_query):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None


if __name__ == "__main__":
    for sql_query in sql_queries:
        print(f"Executing SQL query: {sql_query}")
        result = execute_sql_query(sql_query)
        if result:
            print("Result:")
            for row in result:
                print(row)
