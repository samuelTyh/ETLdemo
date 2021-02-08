# NOTE: paths are relative to the project root since the build context we specify is the project root

FROM puckel/docker-airflow:1.10.8
USER root

ENV PYTHONPATH $PYTHONPATH:$AIRFLOW_HOME/dags

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN rm $AIRFLOW_HOME/airflow.cfg

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

USER airflow