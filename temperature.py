# coding: utf-8
#!/usr/bin/env python

import os
import logging
import datetime
import sqlite3
from DS18B20 import (DS18B20,
                     NotReady)

db_path = os.path.join(os.path.expanduser("~"), ".ds18b20/values.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `temperature` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `sensor` CHAR(15),
        `origin` INT,
        `degrees_c` FLOAT,
        `degress_f` FLOAT,
        `createtime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );""")
conn.commit()


def save_to_db(name, orign_value, degrees_c, degress_f, time=None):
    time = datetime.datetime.now() if not time else time
    params = (name, orign_value, degrees_c, degress_f, time)
    try:
        cursor.execute("""
            insert into temperature
             (sensor, origin, degrees_c, degress_f, createtime)
             values (?, ?, ?, ?, ?)""", params)
        conn.commit()
    except sqlite3.OperationalError, e:
        logging.error(e.message)


def get_value():
    sensors = DS18B20.get_sensors()
    for sensor in sensors:
        sensor_name = sensor.sensor_name
        try:
            origin, degrees_c, degress_f = sensor.get_temperature()
        except NotReady, e:
            logging.warning(e.message)
            origin = degrees_c = degress_f = None
        time = datetime.datetime.now()
        save_to_db(sensor_name, origin, degrees_c, degress_f, time)


if __name__ == "__main__":
    # name = "28-abcdefghijklmno"
    # origin = 2000
    # c = origin / 1000
    # f = origin * 9 / 5000 + 32
    # time = datetime.datetime.now()
    # save_to_db(name, origin, c, f, time)
    get_value()
    sql = """select * from temperature order by id desc limit 1"""
    for row in cursor.execute(sql):
        print row
