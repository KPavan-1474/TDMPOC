FROM python:3.8-slim-buster

WORKDIR /opt/app

COPY . .

#COPY requirements.txt requirements.txt

RUN pip3 install -r ./pythonfusecode/requirements.txt

ENV FLASK_APP=./pythonfusecode/app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["waitress-serve", "--listen=*:8080",  "app:app"]