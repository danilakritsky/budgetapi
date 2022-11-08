FROM alpine:latest

ARG USERNAME=budgetapi
ARG PYTHON_VERSION=3.11.0

RUN apk update \
    && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        bash \
        curl \
        git \
        python3 \
        python3-dev \
        gcc \
        musl-dev \
        libc-dev \
        libffi-dev \
        make \
        zlib-dev \
        openssl-dev \
        readline-dev \
        ncurses-dev \
        sqlite-dev \
        bzip2-dev \
        xz-dev \
        # install build-base to install greenlet
        # https://stackoverflow.com/questions/11912878/gcc-error-gcc-error-trying-to-exec-cc1-execvp-no-such-file-or-directory
        build-base

# running apk add py3-pip results in broken pip: importlib.metadata.PackageNotFoundError: No package metadata was found for pip
# # use ensurepip to add pip
# RUN python3 -m ensurepip --upgrade
# RUN python3 -m pip install --upgrade pip

# add non root user
# https://www.baeldung.com/linux/docker-alpine-add-user
RUN adduser -D ${USERNAME}
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# installing pyenv
# https://gist.github.com/jprjr/7667947
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT="/home/${USERNAME}/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv local ${PYTHON_VERSION}

# installing poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/${USERNAME}/.local/bin:$PATH"
COPY pyproject.toml .
RUN poetry install

USER root
RUN chmod a+wx pyproject.toml
RUN apk add net-tools
USER ${USERNAME}


ENTRYPOINT [ "sh" ]