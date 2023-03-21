from flask_restx.reqparse import RequestParser

user_get_all_parser: RequestParser = RequestParser()

user_get_all_parser.add_argument(
    name='page',
    type=int,
    location='args',
    required=False,
    help='(optional) Page selector'
)

user_get_all_parser.add_argument(
    'year',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by year'
)

user_get_all_parser.add_argument(
    'did',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by Director ID'
)

user_get_all_parser.add_argument(
    'gid',
    type=int,
    location='args',
    required=False,
    help='(optional) Filter by Genre ID'
)

user_get_all_parser.add_argument(
    'status',
    type=str,
    location='args',
    required=False,
    choices=["new", ],
    help='(optional) Order by status'
)
