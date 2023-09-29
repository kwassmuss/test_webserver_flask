FROM python:3.11

RUN apt-get -y update && apt-get install -y \
    python3-flask \
    python3-pandas

# build webserver
ADD . /webserver
WORKDIR /webserver

# development warning
RUN echo 'this is a development build, for deploying to production see https://flask.palletsprojects.com/en/2.3.x/deploying/'

## locally available server
# CMD /usr/bin/python3 -m flask --app webserver run
## globally available server
CMD /usr/bin/python3 -m flask --app webserver run --host=0.0.0.0 --port 8080
EXPOSE 8080
