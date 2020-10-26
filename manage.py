#!/usr/bin/env python3

import sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import db
from app.config import config
from app.factory import create_app, create_api


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.option('-e', dest="email", default=None)
@manager.option('-u', dest="username", default=None)
@manager.option('-p', dest="password", default=None)
def setup(email, username, password):
    """ Setup UserDatastore and Roles. Add -a <email> to create default admin user with email and password=password
    """

    from datetime import datetime
    from app import models, db
    from flask_security import SQLAlchemyUserDatastore

    # create roles
    with app.app_context():
        db.create_all()
        store = SQLAlchemyUserDatastore(db, models.User, models.Role)

        # Add roles
        for name, description in [
            ("Admin", "Administration"),
        ]:
            try:
                store.create_role(name=name, description=description)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

            # optional: add admin user
            if email or username or password:
                store.create_user(username=username, email=email, password=password, roles=["Admin"])
                models.User.get_user("admin").confirmed_at = datetime.now()
                db.session.commit()


@manager.command
def testmail():
    """ Test mail transport
    """
    from flask_mail import Message
    from app import mail

    msg = Message("Hello", sender=config["mail_from"], recipients=config["admins"])
    mail.send(msg)


@manager.command
def web():
    """Start web application"""
    app.run(debug=True)


@manager.command
def api():
    app2 = create_api()
    app2.run(debug=True)


@manager.command
def sql():
    """ Openss a mysql prompt
    """
    from subprocess import Popen

    parts = config["sql_database"].split("/")
    database = parts[-1].strip()
    user = parts[2].split(":")[0].strip()
    password = parts[2].split(":")[1].split("@")[0].strip()
    host = parts[2].split("@")[1].strip()
    args = [
        "mysql",
        "-h",
        host,
        "-u",
        user,
        "--password={}".format(password),
        "-D",
        database,
    ]
    Popen(args).wait()


if __name__ == "__main__":
    manager.run()
