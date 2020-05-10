import flask
from flask import jsonify, request
from data import db_session
from data.passwords import Password

blueprint = flask.Blueprint('passwords_api', __name__, template_folder='templates')


@blueprint.route('/api/passwords')
def get_passwords():
    session = db_session.create_session()
    passwords = session.query(Password).all()
    return jsonify(
        {
            'passwords': [item.to_dict(only=('url', 'login', 'user.name')) for item in passwords]
        }
    )


@blueprint.route('/api/passwords/<int:passwords_id>', methods=['GET'])
def get_one_passwords(passwords_id):
    session = db_session.create_session()
    passwords = session.query(Password).get(passwords_id)
    if not passwords:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'passwords': passwords.to_dict(only=('url', 'login', 'user_id'))
        }
    )


@blueprint.route('/api/passwords', methods=['POST'])
def create_passwords():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['url', 'login', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    passwords = Password(
        url=request.json['url'],
        login=request.json['login'],
        user_id=request.json['user_id']
    )
    session.add(passwords)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/passwords/<int:passwords_id>', methods=['DELETE'])
def delete_passwords(passwords_id):
    session = db_session.create_session()
    passwords = session.query(Password).get(passwords_id)
    if not passwords:
        return jsonify({'error': 'Not found'})
    session.delete(passwords)
    session.commit()
    return jsonify({'success': 'OK'})
