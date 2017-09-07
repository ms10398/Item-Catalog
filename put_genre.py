from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Movies

"""
    Used to populate, the genre table.
"""
engine = create_engine('sqlite:///MovieDatabase.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

genres = ['Romantic', 'Comedy', 'Sci-Fi', 'Horror', 'Drama', 'Suspense']

for name in genres:
    genreList = session.query(Genre).filter_by(name = name).one_or_none()
    if not genreList:
        genre = Genre(name = name)
        session.add(genre)
        session.commit()
        print name + " Added to Database!"
    else:
        print name + " Already in Database!"
