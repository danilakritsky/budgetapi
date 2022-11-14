FROM python:3.11

ARG PYTHON_VERSION=3.11.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Configure Poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_VENV=/root/.local

# Install poetry
RUN python3 -m venv ${POETRY_VENV} \
    && ${POETRY_VENV}/bin/pip install -U pip setuptools \
    && ${POETRY_VENV}/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
RUN poetry config virtualenvs.create false
RUN poetry completions bash >> ~/.bash_completion


WORKDIR /root
COPY pyproject.toml .
RUN poetry install
COPY budgetapi/ /root/budgetapi
WORKDIR /root/budgetapi
