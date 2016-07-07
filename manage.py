import sys
import os
import pymongo
import sqlalchemy
import flask.ext.script as flask_script

import ninechan

__author__ = 'takeshix'

manager = flask_script.Manager(ninechan.app)


@manager.command
def populate():
    """Populate the database. This will add the default admin user."""
    # CREATE DATABASE ninechan;
    # GRANT ALL ON ninechan.* TO 'ninechan'@'%' IDENTIFIED BY 'ninechan1337';
    # CREATE TABLE mails (id INT AUTO_INCREMENT PRIMARY KEY ,sender VARCHAR(50),receiver VARCHAR(50),subject VARCHAR(100),message VARCHAR(500), timestamp VARCHAR(50));
    pass


@manager.command
def cleanup():
    """Cleanup the database and upload path. This deletes all image
    files that are not associated with any post in the database."""
    pass


@manager.command
def purge():
    """Purge the complete database."""
    pass


def main():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        manager.add_command(
            "runserver",
            flask_script.Server(
                host='0.0.0.0'
            )
        )
        # TODO Add command to populate database
        # e.g. create admin user with password and set superuser rights
        # TODO Add command to clean unused files
        # e.g. check if static/images is empty when the database is empty
        # TODO Add command to clean database
        # e.g. delete the complete database
        manager.run()
        return 0
    except KeyboardInterrupt:
        return 2
    except:
        return 1

if __name__ == "__main__":
    sys.exit(main())
