ninechan
========

A vulnerable web application for various penetration testing modules built with Flask and MongoDB. This application
includes a simple bot written with ZombieJS running on NodeJS that acts as a admin user. This allows e.g. exploitation
of XSS.

### Goals
This application is meant to fill the gap of missing challenges within common vulnimages/wargames/etc for some
penetration testing tools. These include:

* Exploitable XSS injections (with a bot)
* Weak session tokens (TBD)
* ...

## Prepare Environment
Flask application dependencies:
* Python 2.7
* MongoDB

Bot dependencies:
* Node.js
* npm

The `scripts` directory includes several helper scripts. In order to initialized the basic environment, run the
following command:

```
scripts/deploy-virtualenv.sh
```

This will create a virtual environment for Python and Node.js. Additionally, it will install all required dependencies.

## Web Application (Flask)
The `Flask` web application located in `ninechan` should be executed from within a `virtualenv` environment. The
`scripts` directory includes two helper scripts to accomplish this. The most basic production setup can be started
by executing the `run-virtualenv.sh` script:

```
scripts/run-virtualenv.sh
```

However, during development, one might want to run the application with a slightly different setup, like a separate
development database so the production database won't be spammed:

```
scripts/run-virtualenv-dev.sh
```

## Bot (Zombie.js)
The bot, which executes tasks in the context of the `admin` user resides in `ninechan-bot`. It should also be
executed from within a virtual environment. The `deploy-virtualenv.sh` installs `nodeenv`, so we can use `node` and
`npm` from within the virtual environment like we would do with `python` and `pip`:

```
env/bin/node ninechan-bot/bot.js
```

The `scripts` directory also includes a helper script for the bot:

```
scripts/run-bot.sh
```
