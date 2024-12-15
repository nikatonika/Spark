FROM openjdk:11-slim

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip  build-essential 

WORKDIR /app  

COPY app.py ./

ADD https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.4.6/clickhouse-jdbc-0.4.6-all.jar ./

RUN pip3 install pyspark clickhouse-driver  # Устанавливаем библиотеки PySpark и ClickHouse Python драйвер

ENV PYTHONUNBUFFERED=1  

CMD ["spark-submit", "--jars", "/app/clickhouse-jdbc-0.4.6-all.jar", "/app/app.py"]
