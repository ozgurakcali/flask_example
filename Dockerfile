FROM python:3

# Prepare container
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip nginx supervisor
RUN pip3 install uwsgi

# Copy app files
RUN mkdir -p /usr/src/app
COPY ./ /usr/src/app
WORKDIR ./usr/src/app

# Install requirements
RUN pip3 install -r requirements.txt

# Run migrations
RUN flask db upgrade

COPY ./deployment/nginx.conf /etc/nginx/sites-enabled/default

CMD supervisord -c /usr/src/app/deployment/supervisord.conf