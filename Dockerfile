FROM python:3.11-alpine

ARG USERNAME=budgetapi
ARG PYTHON_VERSION=3.11.0

RUN apk update

# add non root user https://www.baeldung.com/linux/docker-alpine-add-user
RUN adduser -D ${USERNAME}
USER ${USERNAME}
WORKDIR /home/${USERNAME}

COPY ./budgetapi ./budgetapi
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT [ "sh" ]