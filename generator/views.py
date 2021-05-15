import socket
import random
import struct
import time
import psycopg2
from psycopg2 import extras

now = int(round(time.time() * 1000000000))


from django.shortcuts import render
from influxdb import InfluxDBClient

# Create your views here.
from ts.settings import IP_INFLUXDB, USER_INFLUX, PASS_INFLUX, PORT_INFLUX


def influx_connection(database, timeout=None):
    if timeout:
        client_influx = InfluxDBClient(IP_INFLUXDB, PORT_INFLUX, USER_INFLUX, PASS_INFLUX, database,
                                       timeout=timeout)
    else:
        client_influx = InfluxDBClient(IP_INFLUXDB, PORT_INFLUX, USER_INFLUX, PASS_INFLUX, database)

    return client_influx


def write_points(n):
    initial_time = time.time()
    empresas = ['fcetina', 'megabit', 'megabit2']
    points_ip_visited = []
    now = int(round(time.time() * 1000000000))
    client_influx = influx_connection('trafico-wisphub')
    for i in range(n):
        ip_random = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        dowload_bits = random.randrange(20000)
        upload_bits = random.randrange(1000)
        cliente_id = random.randrange(1000, 1100)
        empresa_id = random.randrange(1, 3)
        empresa_slug = empresas[empresa_id - 1]

        points_ip_visited.append(
            "ip_visited,id_empresa={0},empresa={1},cliente_id={2},ip_visited={3} download={4} {5}".format(
                empresa_id, empresa_slug, cliente_id, str(ip_random), str(dowload_bits), now))
    client_influx.write_points(points_ip_visited, protocol='line', batch_size=10000)

    end_time = time.time()
    time_elapsed = end_time - initial_time

    print "Se escribieron {0} puntos en {1} s".format(str(n), time_elapsed)


def create_db_influx(database):
    client_influx = influx_connection('trafico-wisphub')
    client_influx.create_database(database)


def write_points_timescale(n):
    initial_time = time.time()
    empresas = ['fcetina', 'megabit', 'megabit2']
    db_conn = psycopg2.connect(dbname='trafico-wisphub', user='fernando', host='3.132.97.208', password='fernando1234')
    cursor = db_conn.cursor()
    insert_query = "INSERT INTO ip_visited (time, id_empresa, empresa, cliente_id, ip_visited, download) VALUES (%s, %s, %s, %s, %s, %s)"
    my_data = []
    for i in range(n):
        ip_random = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        dowload_bits = random.randrange(20000)
        upload_bits = random.randrange(1000)
        cliente_id = random.randrange(1000, 1100)
        empresa_id = random.randrange(1, 3)
        empresa_slug = empresas[empresa_id - 1]

        record_to_insert = (
        "now()", empresa_id, empresa_slug, cliente_id, ip_random, dowload_bits)
        my_data.append(record_to_insert)

    # cursor.executemany(insert_query, my_data)
    extras.execute_batch(cursor, insert_query, my_data, 10000)
    db_conn.commit()
    cursor.close()
    db_conn.close()
    end_time = time.time()
    time_elapsed = end_time - initial_time

    print "Se escribieron {0} puntos en {1} s".format(str(n), time_elapsed)