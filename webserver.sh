#!/bin/bash -x

#docker=$(which podman)
docker=$(which docker)

function usage(){
    echo "some commands to build, run and check the webserver"
    echo "$0 [--build] [--run] [--check]"
    exit 0
}

function build {
    $docker build -t webserver .
}

function run {
    $docker run -dp 127.0.0.1:8080:8080 webserver
}

function check {
    sep=\;
    column='Krankenhauskosten'
    echo "check ${column}"
    curl -X POST --data-binary "@test.csv" http://localhost:8080/stats/\?column\=$column\&sep\=$sep || exit $?
    column=ICD%20E11%20%2D%20liegt%20vor
    echo "check ${column}"
    curl -X POST --data-binary "@test.csv" http://localhost:8080/stats/\?column\=$column\&sep\=$sep || exit $?
}

if test "$1" == "--build"; then
    build
    exit $?
fi

if test "$1" == "--run"; then
    run
    exit $?
fi

if test "$1" == "--check"; then
    check
    exit $?
fi

usage
