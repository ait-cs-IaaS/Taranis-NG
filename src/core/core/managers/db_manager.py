from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from core.managers.db_seed_manager import pre_seed
from flask_sqlalchemy.model import Model


db = SQLAlchemy()
migrate = Migrate()
BaseModel = db.make_declarative_base(Model)


def initialize(app):
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()
    pre_seed(app)
