import flask
from flask import jsonify, request

from data import db_session
from data.users import User

# I'll do some blueprint roots for server api

blueprint = flask.Blueprint(
    'server_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    return jsonify(
        {
            'users':
                [item.to_dict(only=('email', 'name', 'created_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    return jsonify(
        {
            'user': user.to_dict(only=(
                'email', 'name', 'created_date', 'events'))

        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'name', 'password']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    user = User(
        email=request.json['email'],
        name=request.json['name']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'Not found'})

    db_sess.delete(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})
