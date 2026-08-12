from core.database import SessionLocal
from sqlalchemy.orm import Session
from users.model import UserModel
from tasks.models import TaskModel
from faker import Faker

faker = Faker()


def seed_user(db):
    user = UserModel(username=faker.user_name(), email=faker.email())
    user.set_password("12345678")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User created with Username: {user.username}")
    return user


def seed_tasks(db, user, count=15):
    tasks_list = []
    for _ in range(15):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=faker.sentence(nb_words=6),
                description=faker.text(),
                is_completed=faker.boolean(),
            )
        )
    db.add_all(tasks_list)
    db.commit()
    print(f"added 15 tasks for user id {user.id}")


def main():
    db = SessionLocal()

    try:
        user = seed_user(db)
        tasks = seed_tasks(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
