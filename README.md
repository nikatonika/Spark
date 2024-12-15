# Инфраструктура больших данных  
Цель: разработать часть ETL-пайплайн, который будет выполнять следующие задачи:

Извлекать данные из PostgreSql с использованием Python Connector.
Загружать эти данные в Kafka.
Трансформировать их с помощью Apache Spark Streaming.
Сохранять обработанные данные в ClickHouse для дальнейшего аналитического использования.
Разворачивать приложения мы будем с использованием Docker и Kubernetes, что упростит управление сервисами и их взаимодействие. Apache Spark также будет запускаться в Kubernetes. Для простоты мы положим его в контейнер.

Архитектура кластера:
![img arch](./img/arch.png)

Работающий  кластер:
![img claster_status](./img/claster_status.png)


плюс разработано  Spark-приложение, которое:  

*Рассчитывает средний доход (Income) для каждого возраста.   
*Сохраняет результаты в таблицу customers_transformed.   
*Настраивает подключение Spark-приложения к существующей инфраструктуре.   


Преобразованная таблица:
![img sel_transormed.png](./img/sel_transormed.png)

