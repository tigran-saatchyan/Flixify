from flixify.dao import DirectorDAO, GenreDAO, MovieDAO, UserDAO
from flixify.services import AuthService, DirectorService, MovieService, \
    GenreService, \
    UserService
from flixify.setup.db import db

director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)


movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)


genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)


user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

auth_service = AuthService(user_service)
