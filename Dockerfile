FROM python:latest

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install flask gunicorn

ADD . $APP_HOME/
ENV FLASK_APP=myFlaskProject.py
CMD ["gunicorn", "-b", "0.0.0.0:3003", "myFlaskProject:app"]
