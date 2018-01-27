FROM python:3.6

EXPOSE 8000
RUN mkdir /app/
COPY . /app/srv

WORKDIR /app/srv/
RUN pip install pipenv
RUN pwd
RUN pipenv install
RUN echo "SHELL=/bin/bash" > .env
RUN cat .env

WORKDIR /app/srv/WhoWolf
RUN chmod +x /app/srv/WhoWolf/entrypoint.sh
ENTRYPOINT /app/srv/WhoWolf/entrypoint.sh
