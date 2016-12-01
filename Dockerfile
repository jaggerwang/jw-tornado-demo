FROM daocloud.io/jaggerwang/python

ENV APP_PATH=/app
ENV DATA_PATH=/data

WORKDIR /root
RUN git clone https://github.com/jaggerwang/jw-pylib.git
ENV PYTHONPATH=/root/jw-pylib/src:$PYTHONPATH

ADD . $APP_PATH
WORKDIR $APP_PATH
RUN pip3 install -r requirements.txt

VOLUME $DATA_PATH

EXPOSE 8888

CMD supervisord
