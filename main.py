from server import app
from data import db_session, server_api
import os


def main():
    db_session.global_init('db/all_users.sqlite')
    app.register_blueprint(server_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
