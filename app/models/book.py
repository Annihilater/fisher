from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(1000), nullable=False)
    isbn = Column(String(15), nullable=False, unique=True)
    author = Column(String(1000), default='未名')
    translator = Column(String(1000))
    binding = Column(String(100))
    publisher = Column(String(100))
    price = Column(String(100))
    pages = Column(String(100))
    pubdate = Column(String(50))
    summary = Column(String(5000))
    image = Column(String(1000))

    def __init__(self, **items):
        super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
