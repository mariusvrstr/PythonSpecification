from src.common.specification import Specification, apply_specification
from src.database.sqllite_database import SQLLiteDatabase
from src.database import db_models
from src.database.db_models import User
from typing import List

'''
Compiles but filtering with _or / _and is not working as expected
'''

database = SQLLiteDatabase()
db_models.Base.metadata.create_all(database.engine)

session = database.create_session()

def add_users():
    user1 = User(name="John Doe", age=30, email="johndoe@somedom.com", is_active=True)
    user2 = User(name="Jane Doe", age=25, email="janedoe@example.com", is_active=True)
    user3 = User(name="Bob Smith", age=40, email="bobsmith@example.com", is_active=False)

    session.add_all([user1, user2, user3])
    session.commit()

if session.query(User).count() == 0:
    add_users()

user_is_active = Specification(lambda user: user.is_active == True)
user_part_of_example = Specification(lambda user: user.email.endswith("@example.com"))

spec = user_is_active.or_specification(user_part_of_example)

query = session.query(User)
filtered_query = apply_specification(query, spec)
found_users = filtered_query.all()

for user in found_users:
    print(f"User [{user.name}] - [{user.email}]")




