import flask
import sqlalchemy.exc
from flask import jsonify, request

from data import db_session
from data.users import User


blueprint = flask.Blueprint(
    'server_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')  # Get all users info(id, email, name and created date of each account)
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    return jsonify(
        [
            item.to_dict(only=('id', 'email', 'name', 'created_date')) for item in users
        ]
    )


@blueprint.route('/api/users/<string:user_email>', methods=['GET'])  # Get user info(email, name, created date, events and friends list)
def get_user(user_email):
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    for user in users:
        print(user.email == user_email)
        if user.email == user_email:
            user_found = db_sess.query(User).get(user.id)

            return jsonify(
                user_found.to_dict(only=('email', 'name', 'created_date', 'events', 'friends_list'))
            )

    return jsonify({'error': 'Not found'})


# @blueprint.route('/api/users/<int:friend_id>/<int:self_id>', methods=['POST'])
# def add_to_friends_requests(friend_id, self_id):
#     db_sess = db_session.create_session()
#     friend = db_sess.query(User).get(friend_id)
#     self = db_sess.query(User).get(self_id)
#
#     friend.add_friend_request('Anatoly')
#
#     db_sess.commit()
#
#     return jsonify({'error':'Not available'})


@blueprint.route('/api/register', methods=['POST'])  # Registration
def register():
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

    try:
        db_sess.add(user)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError as sql_IE:
        return jsonify({'error': 'Already exists'})
    except Exception as e:
        return jsonify({'error': 'Bad request'})

    return jsonify({'success': 'OK'})


@blueprint.route('/api/login', methods=['POST'])
def login():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'password']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    for user in users:
        if user.email == request.json['email'] and user.check_password(request.json['password']):
            return jsonify({'success': 'OK'})

    return jsonify({'error': 'Authorisation Error'})


@blueprint.route('/api/delete_user', methods=['POST'])
def delete_user(user_email):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'password']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    for user in users:
        if user.email == request.json['email']:
            if user.check_password(request.json['password']):
                db_sess.delete(user)
                db_sess.commit()
                return jsonify({'success': 'OK'})
            else:
                return jsonify({'error': 'Authorisation Error'})
    return jsonify({'error': 'Not found'})
