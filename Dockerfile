FROM python:3.9

#ENV PYTHONBUFFERED 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

#Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/

# Install dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . .

#CMD python /app/main/main.py 0.0.0.0:8000

CMD [ "flask", "run", "--host=0.0.0.0"]
