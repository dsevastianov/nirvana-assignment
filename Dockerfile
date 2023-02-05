# Using lightweight alpine image
FROM python:3.10-alpine as base

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

# Install dev dependencies for debugging
RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "--debugger", "-h", "0.0.0.0", "-p", "5000"]
  