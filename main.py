from server import app
from data import db_session, server_api


def main():
    db_session.global_init('db/all_users.sqlite')
    app.register_blueprint(server_api.blueprint)
    app.run(port=5000)


if __name__ == '__main__':
    main()
