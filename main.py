from server import app
from data import db_session, server_api
import os

ON_HEROKU = os.environ.get('ON_HEROKU')


def main():
    db_session.global_init('db/all_users.sqlite')
    app.register_blueprint(server_api.blueprint)
    app.run(port=int(os.environ.get('PORT', 17995)))


if __name__ == '__main__':
    main()
