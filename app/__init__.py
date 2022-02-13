import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL').replace("://", "ql://", 1),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    from app.database.model import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.resources.routes import api, initialize_routes
    initialize_routes(api)
    api.init_app(app)

    from app.common.encrypt import bcrypt
    bcrypt.init_app(app)

    return app
