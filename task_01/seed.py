import faker
import psycopg2

from config import db_config

STATUSES = [
    "to do",
    "in progress",
    "done",
]
USER_COUNT = 10
TASK_COUNT = 50


def generate_seed_data():
    fake = faker.Faker()

    users = [
        {
            "fullname": fake.name(),
            "email": fake.unique.email(),
        }
        for _ in range(USER_COUNT)
    ]

    tasks = [
        {
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": fake.random_int(min=1, max=len(STATUSES)),
            "user_id": fake.random_int(min=1, max=USER_COUNT),
        }
        for _ in range(TASK_COUNT)
    ]

    return users, tasks


def prepare_data_for_db():
    users, tasks = generate_seed_data()

    tuples_users = tuple((user["fullname"], user["email"]) for user in users)
    tuple_statuses = tuple((status,) for status in STATUSES)
    tuple_tasks = tuple(
        (
            task["title"],
            task["description"],
            task["status_id"],
            task["user_id"],
        )
        for task in tasks
    )

    return tuples_users, tuple_statuses, tuple_tasks


def seed_db():
    tuples_users, tuple_statuses, tuple_tasks = prepare_data_for_db()
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO users (fullname, email) VALUES (%s, %s)", tuples_users
                )
                cursor.executemany(
                    "INSERT INTO status (name) VALUES (%s)", tuple_statuses
                )
                cursor.executemany(
                    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    tuple_tasks,
                )
                conn.commit()

        print("Database seeded successfully.")
    except Exception as e:
        print(f"Error seeding database: {e}")


if __name__ == "__main__":
    seed_db()
