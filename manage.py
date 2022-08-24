import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# Solucion para el error: ModuleNotFoundError: No module named 'flask._compat'
#from flask_script._compat import text_type

from app import app, db


#app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

#----Para inicalizar la migracion----
# py manage.py db init
#----Para generar la migracion----
# py manage.py db migrate
# py manage.py db upgrade

# Otros comandos
# flask db stamp head  # To set the revision in the database to the head, without performing any migrations. You can change head to the required change you want.
# flask db migrate     # To detect automatically all the changes.
# flask db upgrade     # To apply all the changes.