FROM python:3.11

RUN apt-get -y update && apt-get install -y \
    python3-flask \
    python3-pandas \
    gunicorn
    
ADD . /webserver
WORKDIR /webserver

# development warning
RUN echo 'using gunicorn without separate webserver. You may want to add nginx / apache in production. See https://flask.palletsprojects.com/en/2.3.x/deploying/'
## globally available server
#CMD /usr/bin/python3 -m flask --app webserver run --host=0.0.0.0 --port 8080
# using gunicorn with one worker thread
CMD /usr/bin/gunicorn 'webserver:app' -b 0.0.0.0:8080
EXPOSE 8080
