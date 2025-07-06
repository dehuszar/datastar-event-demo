FROM python:latest 

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver"]
