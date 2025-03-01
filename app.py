from flask import Flask
from backend.models import db

app = None
def initialise_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_app.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app

initialise_app()


from backend.routes import *

if __name__ == "__main__":
    app.run(debug=True)