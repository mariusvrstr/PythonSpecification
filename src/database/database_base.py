from abc import abstractmethod
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class DatabaseBase():    
    engine = None

    def __init__(self) -> None:
        self.engine = self._create_engine()

    @abstractmethod
    def _create_engine(self):
        pass

    def create_session(self) -> Session:
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return session()
