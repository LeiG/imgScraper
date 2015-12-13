"""
Define SQLite database to store images.
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    '''
    Image (object)
    --------------
    id: identifier (Integer)
    brand: brand name (String)
    code: product code (String)
    sourceUrl: source url (String)
    eventDate: date retreived (Date)
    price: regular price (Integer)
    salePrice: sale price (Integer)
    ImagePath: local path (String)
    '''
    __tablename__ = "images"

    id = Column(Integer, primary_key = True)
    brand = Column(String)
    category = Column(String)
    code = Column(String)
    sourceUrl = Column(String)
    eventDate = Column(Date)
    price = Column(Integer)
    salePrice = Column(Integer)
    imagePath = Column(String)


def create_db():
    # create tables
    engine = create_engine('sqlite:///images.db', echo=True)
    Base.metadata.create_all(engine)
