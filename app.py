import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import pathlib

db = SQLAlchemy()
PATH = pathlib.Path(__file__).parent
DB_PATH = PATH.joinpath('static/db.db').resolve().__str__()
db_uri =  'sqlite:////' + DB_PATH

def create_app():
    app = flask.Flask(__name__,)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)
    migrate = Migrate(app, db)
    from views import main
    app.register_blueprint(main)


    return app

# @app.route()
# def my_index():
#     return flask.render_template('index.html', token="hello flask react")


# app.run(debug=True)

if __name__ == '__main__':
    app = create_app()
    print(len(sys.argv))
    if len(sys.argv) > 1:
        port = sys.argv[1]
        app.run(port=port, debug=True)
    else:
        app.run(port=5000, debug=True, host="0.0.0.0")