# coding:utf-8

from __future__ import division
import os
import logging

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')


class SensorException(Exception):

    """
    Sensor exception
    """
    pass


# class SensorNotFound(SensorException):

#     """
#     there is no sensors
#     """
#     pass


class NotReady(SensorException):

    """
    sensor not ready to get temperature value
    """
    pass


class DS18B20():
    BASE_DIRECTORY = "/sys/bus/w1/devices"

    def __init__(self, sensor_name):
        self.sensor_name = sensor_name

    @classmethod
    def get_sensors(cls):
        """
        maybe multi sensor
        """
        return [cls(s) for s in os.listdir(cls.BASE_DIRECTORY)
                if s.startswith("28")]

    def get_temperature(self):
        try:
            origin = self.get_origin()
        except NotReady, e:
            logging.error(e.message)
            raise e
        else:
            degrees_c = origin / 1000
            degrees_f = origin * 9 / 5000 + 32
            return origin, degrees_c, degrees_f

    def get_origin(self):
        """
        get origin value
        """
        with open(self.sensor_path) as f:
            lines = f.readlines()
            if lines[0].strip()[-3:] != "YES":
                raise NotReady("temperature value not ready")
            return float(lines[1].split("=")[1])

    @property
    def sensor_path(self):
        return os.path.join(self.BASE_DIRECTORY, self.sensor_name, 'w1_slave')


if __name__ == "__main__":
    sensors = DS18B20.get_sensors()
    if sensors:
        # "\u00B0"
        print(sensors[0].get_temperature())
