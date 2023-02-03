# Using lightweight alpine image
FROM python:3.10-alpine

# Installing packages
RUN apk update
RUN pip install pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
COPY aggregator ./aggregator
COPY api ./api

# Install API dependencies
RUN pipenv install --system --deploy