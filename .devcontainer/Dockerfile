FROM mcr.microsoft.com/devcontainers/base:bullseye

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install python-dev default-libmysqlclient-dev

RUN chmod -R a+w /usr/local
