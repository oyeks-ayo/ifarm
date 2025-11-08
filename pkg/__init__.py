from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate # type: ignore
from flask_mail import Mail # type: ignore
from config import config
from pkg.models import db

csrf = CSRFProtect()
mail = Mail()

def create_app():
    from pkg import models
    app = Flask(__name__,instance_relative_config=True) 
    app.config.from_object(config.Appconfig) #TO MAKE THE CONFIG ITEMS CREATED IN PKG/CONFIG.PY AVAILABLE
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app,db)

    return app

app = create_app()

# from pkg import user_routes, admin_routes,models,forms
from pkg.routes import user_routes, admin_routes