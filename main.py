from src.common.specification import Specification, And, Or
from src.database.sqllite_database import SQLLiteDatabase
from src.database import db_models
from src.database.db_models import User
from typing import List

''' ISSUES
Works in a user list but not as a DB Query
'''

database = SQLLiteDatabase()
db_models.Base.metadata.create_all(database.engine)

class UserIsActive(Specification):
  def is_satisfied_by(self, user:User):
    # print(f'User [{user.name}] check if active [{user.is_active}] ')
    return user.is_active

class FromSpecificDomain(Specification):
    domain = None
    def __init__(self, domain) -> None:
        self.domain = domain
        super().__init__()
    
    def is_satisfied_by(self, user:User):
        # print(f'User [{user.name}] check domain [{user.email}]') 
        return user.email.endswith(self.domain)  

session = database.create_session()

def add_users():
    user1 = User(name="John Doe", age=30, email="johndoe@somedom.com", is_active=True)
    user2 = User(name="Jane Doe", age=25, email="janedoe@example.com", is_active=True)
    user3 = User(name="Bob Smith", age=40, email="bobsmith@example.com", is_active=False)

    session.add_all([user1, user2, user3])
    session.commit()

if session.query(User).count() == 0:
    add_users()

specification = (UserIsActive() & FromSpecificDomain(domain="@example.com"))

all_users = session.query(User).all()

results = []

for user in all_users:
    if specification.is_satisfied_by(user):
        results.append(user)

'''
Not working
results = session.query(User).filter(specification.is_satisfied_by(User)).all()
'''

for item in results:
    print(f"Found [{item.name}] - [{item.email}]")










