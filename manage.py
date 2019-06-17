from app import create_app, db
from config import Config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_security.utils import hash_password

app = create_app(Config)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def quickstart():
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(name="user", description="Simple User Role")

    if not app.security.datastore.get_user("admin@local.ru"):
        app.security.datastore.create_user(email="admin@local.ru", user_name="admin", password=hash_password("admin"))
    db.session.commit()

    app.security.datastore.add_role_to_user("admin@local.ru", "admin")
    db.session.commit()


if __name__ == "__main__":
    manager.run()
