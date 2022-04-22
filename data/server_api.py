import flask
from flask import jsonify, request

# I'll do some blueprint roots for server api

blueprint = flask.Blueprint(
    'server_api',
    __name__,
    template_folder='templates'
)
