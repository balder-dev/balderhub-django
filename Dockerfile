FROM python:3.10-alpine

WORKDIR /code

COPY . /code

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0

RUN pip install -r requirements.txt
RUN pip install -e .
