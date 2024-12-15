import os
from flask import Flask, jsonify
import psycopg2
from kafka import KafkaProducer
import simplejson
import json

app = Flask(__name__)

PG_CONFIG = {
    "dbname": os.getenv("PG_DBNAME", "postgres"), 
    "user": os.getenv("PG_USER", "myuser"), 
    "password": os.getenv("PG_PASSWORD", "mypassword"), 
    "host": os.getenv("PG_HOST", "postgres-service"), 
    "port": int(os.getenv("PG_PORT", 5432))  
}

KAFKA_CONFIG = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"), 
    "topic": os.getenv("KAFKA_TOPIC", "customers") 
}

def fetch_customers():
    """Получение данных о клиентах из PostgreSQL."""
    print("Получение данных о клиентах из PostgreSQL.")
    connection = psycopg2.connect(**PG_CONFIG)  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM customers;")  
    rows = cursor.fetchall() 
    columns = [desc[0] for desc in cursor.description] 
    cursor.close()  
    connection.close() 
    return [dict(zip(columns, row)) for row in rows] 

def push_to_kafka(customers):
    """Отправка данных о клиентах в Kafka."""
    print("Отправка данных о клиентах в Kafka.")
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"], 
        value_serializer=lambda v: simplejson.dumps(v).encode("utf-8")
    )
    for customer in customers:
        producer.send(KAFKA_CONFIG["topic"], customer) 
    producer.flush()

@app.route("/fetch", methods=["GET"])
def fetch_and_push():
    """Получение данных из PostgreSQL и отправка в Kafka."""
    print("Получение данных из PostgreSQL и отправка в Kafka.")
    try:
        customers = fetch_customers() 
        if customers:
            push_to_kafka(customers)  
            return jsonify({
                "message": f"Отправлено {str(len(customers))} записей в Kafka.",
                "data": customers
            }), 200
        else:
            return jsonify({"message": "Записей о клиентах не найдено."}), 404
    except Exception as e:
        return ({"error": str(e)}), 500 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 5000)))
