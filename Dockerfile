# Reference: https://bmaingret.github.io/blog/2021-11-15-Docker-and-Poetry#multi-stage-build

ARG APP_NAME=example-publisher
ARG APP_PACKAGE=example_publisher
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.10.4
ARG POETRY_VERSION=1.2.2

#
# Stage: base
#

FROM python:$PYTHON_VERSION as base

ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $APP_PATH
COPY . .

#
# Stage: development
#

FROM base as development

ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH
RUN poetry install

ENV APP_NAME=$APP_NAME

ENTRYPOINT ["poetry", "run"]
CMD ["$APP_NAME"]

#
# Stage: build
#

FROM base as build

ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output constraints.txt --without-hashes

#
# Stage: production
#

FROM python:$PYTHON_VERSION as production

ARG APP_NAME
ARG APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Get build artifact wheel and install it respecting dependency versions
WORKDIR $APP_PATH
COPY --from=build $APP_PATH/dist/*.whl ./
COPY --from=build $APP_PATH/constraints.txt ./
RUN pip install ./*.whl --requirement constraints.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["$APP_NAME"]
