ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-alpine

ARG DJANGO_VERSION

WORKDIR /code

COPY . /code

ENV PYTHONPATH="$PYTHONPATH:/code/tests/app/bookstore"
ENV DJANGO_SETTINGS_MODULE=bookstore.settings

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0

RUN pip install -r requirements.txt
RUN pip install -e .
RUN if [ -n "$DJANGO_VERSION" ]; then pip install "Django~=${DJANGO_VERSION}"; fi
