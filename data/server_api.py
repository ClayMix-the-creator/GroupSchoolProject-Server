import flask
from flask import jsonify, request

# I'll do some blueprint roots for server api

blueprint = flask.Blueprint(
    'server_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    return jsonify(
        {
            'error': 'error'
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(
        {
            'error': 'error'
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    return jsonify(
        {
            'error': 'error'
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify(
        {
            'error': 'error'
        }
    )
