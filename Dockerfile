FROM python:3.8-slim-buster

RUN mkdir -p /app
COPY rsyslog_postgres_tools /app/rsyslog_postgres_tools
COPY scripts /app/scripts
COPY test_rsyslog_postgres_tools /app/test_rsyslog_postgres_tools
COPY dev-requirements.txt requirements.txt README.md LICENSE run_rp_tools.py setup.py \
  VERSION yoyo.ini /app/
RUN ls /app/
RUN cd /app/ && python3 -m pip install -r /app/requirements.txt && python3 setup.py install
CMD /app/run_rp_tools.py
