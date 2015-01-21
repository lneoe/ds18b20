# coding: utf-8

import os
import logging
import datetime
import tornado.web
import sqlite3
import tornado.httpserver
import tornado.ioloop
from tornado.options import parse_command_line
from tornado.web import url
# from tornado.escape import json_encode


conn = sqlite3.connect(
    os.path.join(os.path.expanduser("~"), ".ds18b20/values.db"))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def get_pretty_data(gt=None, lt=None):
    query_str = ["select createtime, degrees_c from temperature"]
    params = []

    if not gt and not lt:
        where_q = (" where createtime between date('now') and "
                   "date('now', 'start of day', '+1 day')")
        query_str.append(where_q)

    else:
        condition = []
        if gt:
            params.append(gt)
            condition.append(" createtime > ? ")
        if lt:
            params.append(lt)
            condition.append(" createtime < ? ")
        query_str.append(" where " + ' and '.join(condition))

    sql = ''.join(query_str)
    rows = cursor.execute(sql, params)

    # pretty result
    labels = list()
    data = list()
    for row in rows:
        labels.append(row["createtime"])
        data.append(row["degrees_c"])

    lowest = min(data)
    highest = max(data)
    average = sum(data) / len(data)

    return {"labels": labels, "data": data, "lowest": lowest,
            "highest": highest, "average": average}


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        gt = self.get_argument("gt", None)
        lt = self.get_argument("lt", None)
        data = get_pretty_data(gt=gt, lt=lt)
        return self.render("index.html", data=data)


class TemperatureVauleHandler(tornado.web.RequestHandler):

    def get(self):
        sql = ("select createtime, degrees_c from temperature")
        labels = list()
        data = list()
        rows = cursor.execute(sql)
        for row in rows:
            print row
            labels.append(row["createtime"])
            data.append(row["degrees_c"])
        return self.render_string({"labels": labels, "data": data})


if __name__ == "__main__":
    parse_command_line()
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="cookie_secret",
        debug=True,
        gzip=True,
    )
    handlers = (
        url(r"/", IndexHandler, name="index"),
        url(r"/api/data", TemperatureVauleHandler, name="data-api")
    )
    app = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000, "0.0.0.0")
    logging.warn("Server start at 0.0.0.0:8000")
    tornado.ioloop.IOLoop.instance().start()
