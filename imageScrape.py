import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from imageScraper.defTable import create_db
from imageScraper.brands import coach, katespade


if __name__ == "__main__":
    # create the databse
    create_db()

    # fire up the database
    engine = create_engine('sqlite:///images.db', echo = True)
    Session = sessionmaker(bind = engine)
    session = Session()

    # create folder
    mainPath = os.path.expanduser('~/Google Drive/Coco shopping/brands')
    if not os.path.exists(mainPath):
        os.mkdir(mainPath)

    # scrape coach
    # coachScraper = coach.CoachScraper(mainPath = mainPath, session = session)
    # coachScraper.traverseSite()

    # scrape katespade
    katespadeScraper = katespade.KateSpadeScraper(mainPath = mainPath, session = session)
    katespadeScraper.traverseSite()
