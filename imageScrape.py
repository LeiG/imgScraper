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
    if not os.path.exists('./brands'):
        os.mkdir('./brands')

    # scrape coach
    # coachScraper = coach.CoachScraper(coach.HOMEURL, coach.BRAND, session)
    # coachScraper.traverseSite()

    # scrape katespade
    katespadeScraper = katespade.KateSpadeScraper(katespade.HOMEURL, katespade.BRAND, session)
    katespadeScraper.traverseSite()
