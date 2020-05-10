from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.passwords import Password
from data.reqparse import parser


def abort_if_passwords_not_found(passwords_id):
    session = db_session.create_session()
    passwords = session.query(Password).get(passwords_id)
    if not passwords:
        abort(404, message=f"Password {passwords_id} not found")


class PasswordsResource(Resource):
    def get(self, passwords_id):
        abort_if_passwords_not_found(passwords_id)
        session = db_session.create_session()
        passwords = session.query(Password).get(passwords_id)
        return jsonify({'passwords': passwords.to_dict(
            only=('url', 'login', 'user_id'))})

    def delete(self, passwords_id):
        abort_if_passwords_not_found(passwords_id)
        session = db_session.create_session()
        passwords = session.query(Password).get(passwords_id)
        session.delete(passwords)
        session.commit()
        return jsonify({'success': 'OK'})


class PasswordsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        passwords = session.query(Password).all()
        return jsonify({'passwords': [item.to_dict(
            only=('url', 'login', 'user.name')) for item in passwords]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        passwords = Password(
            url=args['url'],
            login=args['login'],
            user_id=args['user_id']
        )
        session.add(passwords)
        session.commit()
        return jsonify({'success': 'OK'})
