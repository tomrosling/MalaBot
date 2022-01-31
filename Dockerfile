# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-alpine

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apk add --update --no-cache ffmpeg gcc g++ openssl-dev libffi-dev musl-dev make libsodium-dev opus-dev
RUN pip install --upgrade pip # Update pip because grpcio takes _forever_ to install on the default/older version
RUN LIBSODIUM_MAKE_ARGS=-j4 pip install --no-cache-dir -r requirements.txt # LIBSODIUM_MAKE_ARGS to improve PyNaCl build time: https://github.com/Lucas-C/pynacl/blob/patch-1/INSTALL.rst

CMD exec python main.py
