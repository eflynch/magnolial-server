from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from subprocess import call

from magnolial import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def runserver():
    app.run()

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
