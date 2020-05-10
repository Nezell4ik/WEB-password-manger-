from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('url', required=True)
parser.add_argument('login', required=True)
parser.add_argument('user_id', required=True, type=int)
