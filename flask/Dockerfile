# base image
FROM python:3.7-alpine

RUN apk update && \
    apk add python3-dev postgresql-dev gcc musl-dev

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY app.py crud.py /usr/src/app/

# run server
CMD ["python3", "crud.py", "0.0.0.0:5000"]