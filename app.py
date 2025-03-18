from flask import Flask
from backend.models import db
from flask_login import LoginManager
from backend.api import api
app = None
def initialise_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_app.sqlite3"
    app.config["SECRET_KEY"] = "mysecretkey"
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(a):
        user = db.session.query(Customer).filter_by(email = a).first() or \
                db.session.query(Admin).filter_by(email= a).first() or \
                db.session.query(Professional).filter_by(email = a).first()
        return user

    db.init_app(app)
    api.init_app(app)
    with app.app_context():
        db.create_all()

    app.app_context().push()
    return app

initialise_app()


from backend.routes import *


if __name__ == "__main__":
    app.run(debug=True)