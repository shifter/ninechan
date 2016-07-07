#!/bin/sh
ENV="env"

main (){
    VIRTUALENV="$(which virtualenv)"
    PYTHON27="$(which python2.7)"

    if [ -z "$VIRTUALENV" -o -z "$PYTHON27" ]; then
        echo "Make shure Python 2.7 and virtualenv are installed"
        exit 1
    fi

    $VIRTUALENV -p python2.7 $ENV
    . $ENV/bin/activate
    pip install -r requirements.txt
    nodeenv -p --node=system --with-npm
    npm install -g async mongodb zombie chance
}

main