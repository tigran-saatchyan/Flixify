from flask_restx.reqparse import RequestParser

movie_get_all_parser: RequestParser = RequestParser()

movie_get_all_parser.add_argument(
    name='page',
    type=int,
    location='args',
    required=False,
    help='(optional) Page selector'
)

movie_get_all_parser.add_argument(
    'year',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by year'
)

movie_get_all_parser.add_argument(
    'director_id',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by Director ID'
)

movie_get_all_parser.add_argument(
    'genre_id',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by Genre ID'
)

movie_get_all_parser.add_argument(
    'status',
    type=str,
    location='args',
    required=False,
    choices=["new", ],
    help='(optional) Order by status'
)
