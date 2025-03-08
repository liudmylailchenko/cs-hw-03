from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
import certifi


try:
    client = MongoClient(
        "mongodb+srv://liudmylailchenko7:wi8ZzRXU9GfEpQFy@test-cluster.spv21.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster",
        tlsCAFile=certifi.where(),
        server_api=ServerApi("1"),
    )

    db = client.test

    client.admin.command("ping")
    print("Connected successfully to MongoDB!")
except errors.ConnectionFailure as e:
    print(f"Error connecting to MongoDB: {e}")
except errors.PyMongoError as e:
    print(f"An error occurred: {e}")


def py_mongo_error_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")

    return wrapper


@py_mongo_error_decorator
def get_all_cats():
    cats = db.cats.find({})
    for cat in cats:
        print(cat)


@py_mongo_error_decorator
def find_by_name(name):
    cat = db.cats.find_one({"name": name})
    print(cat)


@py_mongo_error_decorator
def update_age(name, age):
    db.cats.update_one({"name": name}, {"$set": {"age": age}})
    print(f"Age for {name} updated successfully")


@py_mongo_error_decorator
def add_feature(name, feature):
    db.cats.update_one({"name": name}, {"$push": {"features": feature}})
    print(f"Feature {feature} for {name} added successfully")


@py_mongo_error_decorator
def delete_by_name(name):
    db.cats.delete_one({"name": name})
    print(f"{name} deleted successfully")


@py_mongo_error_decorator
def delete_all():
    db.cats.delete_many({})
    print("All cats deleted successfully")


if __name__ == "__main__":
    while True:
        try:
            user_input = input("Enter command: ")
            if user_input == "all":
                get_all_cats()
            elif user_input == "find":
                name = input("Enter name: ")
                find_by_name(name)
            elif user_input == "update age":
                name = input("Enter name: ")
                age = int(input("Enter age: "))
            elif user_input == "add feature":
                name = input("Enter name: ")
                feature = input("Enter feature: ")
                add_feature(name, feature)
            elif user_input == "delete":
                name = input("Enter name: ")
                delete_by_name(name)
            elif user_input == "delete all":
                delete_all()
            elif user_input == "exit":
                print("Goodbye!")
                break
        except KeyboardInterrupt as e:
            print("Goodbye!")
            break
