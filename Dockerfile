FROM python:3

ENV APP_PATH=/app
ENV DATA_PATH=/data

WORKDIR $APP_PATH

COPY ./Pipfile* ./
RUN pip install pipenv
RUN pipenv sync

COPY . .

VOLUME $DATA_PATH

EXPOSE 8888

CMD pipenv run python -m jwtornadodemo.app
