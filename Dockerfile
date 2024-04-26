FROM python:3.11
LABEL author='SenalW'
ARG USER="swisscom"
ARG GROUP="swisscom"
ARG UID=1001
ARG GID=1001

WORKDIR /my-cool-service

RUN apt-get update  \
    && apt-get dist-upgrade -y \
    && apt-get install make -y \
    && apt-get install wget -y

# Create a non-root user and group with specified UID and GID
RUN groupadd -r -g $GID $GROUP && useradd -d /my-cool-service -u $UID -r -g $USER $GROUP

# Set ownership of the working directory to the created user and group
RUN chown -R $USER:$GROUP /my-cool-service

# Some container orchestration platforms (including K8s) validates
# non-root users based on integer instead of string.
# Use UID instead of username for ease of use.
USER $UID

COPY --chown=$USER:$GROUP Makefile .
COPY --chown=$USER:$GROUP requirements.txt .
COPY --chown=$USER:$GROUP requirements-style.txt .
COPY --chown=$USER:$GROUP settings.py .

RUN make setup
RUN make install

COPY --chown=$USER:$GROUP src ./src/
COPY --chown=$USER:$GROUP resources ./resources/
COPY --chown=$USER:$GROUP authz ./authz/
COPY --chown=$USER:$GROUP certs ./certs/

ENTRYPOINT ["make", "run"]
