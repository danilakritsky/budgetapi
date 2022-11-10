FROM python:3.11

ARG USERNAME=budgetapi
ARG PYTHON_VERSION=3.11.0

# add non root user https://www.baeldung.com/linux/docker-alpine-add-user
RUN chmod a+xw -R /home
RUN adduser --disabled-login ${USERNAME}
WORKDIR /home/${USERNAME}
RUN chmod a+xw -R /home/${USERNAME}
USER ${USERNAME}

# Configure Poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_VENV=/home/${USERNAME}/.local

# Install poetry
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
RUN poetry config virtualenvs.create false
RUN poetry completions bash >> ~/.bash_completion

COPY pyproject.toml .
RUN poetry install

COPY budgetapi/ ./budgetapi

ENTRYPOINT [ "sh" ]