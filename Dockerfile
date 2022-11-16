FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG HOME_DIR=/home/budgetapi
RUN addgroup budgetapi \
    && adduser \
    --home ${HOME_DIR} \
    --disabled-password \
    --ingroup budgetapi \
    --gecos GECOS budgetapi
ENV HOME=${HOME_DIR}

# Configure Poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_VENV=${HOME}/.local

# Install poetry
RUN python3 -m venv ${POETRY_VENV} \
    && ${POETRY_VENV}/bin/pip install -U pip setuptools \
    && ${POETRY_VENV}/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
RUN poetry config virtualenvs.create false
RUN poetry completions bash >> ~/.bash_completion

COPY pyproject.toml ${HOME}
COPY README.md ${HOME}
COPY budgetapi/ ${HOME}/budgetapi/

RUN chown -R budgetapi:budgetapi $HOME
USER budgetapi
WORKDIR ${HOME}
RUN poetry install --without dev

WORKDIR ${HOME}/budgetapi

