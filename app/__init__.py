import dash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required

db = SQLAlchemy()


def create_app(config=None):

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from auth import models as auth_models

    user_datastore = SQLAlchemyUserDatastore(db, auth_models.User, auth_models.Role)
    app.security = Security(app, user_datastore)

    from .controllers import main
    app.register_blueprint(main)

    register_dashapps(app)

    return app


def register_dashapps(app):
    from dashapp.layout import layout
    from dashapp.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    dash_app = dash.Dash(__name__, server=app, external_stylesheets=external_stylesheets,
                         url_base_pathname='/dashboard/')

    dash_app.title = "Dashboard"
    dash_app.layout = layout
    register_callbacks(dash_app)
    _protect_dashviews(dash_app)


def _protect_dashviews(dashapp):
    """Защита страниц с диаграммами"""
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])