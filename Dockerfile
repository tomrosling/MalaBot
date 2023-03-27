# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg
RUN pip install --upgrade pip setuptools wheel poetry
RUN poetry install --no-dev --no-root

CMD exec poetry run python main.py
