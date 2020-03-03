import pprint

from flask import current_app
from flask_script.commands import ShowUrls

from app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
app = create_app('development')

manager = Manager(app)
# manager.add_command("runserver", Server())
manager.add_command('db', MigrateCommand)
manager.add_command("urls", ShowUrls())
manager.add_command("do", print('asshole'))


@manager.command
def dumpconfig():
    pprint.pprint(current_app.config)


@manager.command
def output(a,b):
    "print something"
    sum = a + b
    print("sum:", sum)


manager.run()
