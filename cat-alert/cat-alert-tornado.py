#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: xudong.wang
@file: helloworld.py
@time: 2017/11/23 10:44

写日志的命令
python helloworld.py -port=8092 -log_file_prefix=/tmp/torn.log
貌似不对的
"""

import os
import ssl
import logging
from datetime import datetime as dt

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import tornado.options
from tornado.options import define, options

from sender import sender_mail, sender_sms, sender_weixin

LOG = logging.getLogger(__name__)


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, cat-alert server is running!")


class GetHandler(RequestHandler):

    def get(self):
        logging.info("**Request to get handler!")
        logging.info('req url: ' + self.request.uri)
        dic = {'status': 'ok'}
        print('args list:', self.request.arguments)
        # get all get params
        for k in self.request.arguments.keys():
            v = self.get_argument(k, default=None, strip=False)
            dic.update({k: v})
        print('response dict: ', dic)
        self.write(dic)


class PostHandler(RequestHandler):

    def post(self):
        logging.info("**Request to post handler!")
        logging.info('req url: ' + self.request.uri)
        dic = {'status': 'ok'}
        print('args list:', self.request.arguments)
        for k in self.request.arguments.keys():
            v = self.get_argument(k, default=None, strip=False)
            dic.update({k: v})
        self.write(dic)


class CatAlertHandler(RequestHandler):

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_status(200)


class SendMailHandler(CatAlertHandler):

    def get(self):
        self.write('hello mail')

    def post(self):
        try:
            logging.info("**Request to post handler!")
            logging.info('req url: ' + self.request.uri)
            dic = dict()
            print('args list:', self.request.arguments)
            for k in self.request.arguments.keys():
                v = self.get_argument(k, default=None, strip=False)
                dic.update({k: v})
            sender_obj = sender_mail(dic)

            if sender_obj != 0:
                sender_obj.send()
            self.write('200')
        except Exception as e:
            logging.info("error in SendMailHandler: %s" % str(e))


class SendSmsHandler(CatAlertHandler):

    def get(self):
        self.write('hello sms')

    def post(self):
        try:
            logging.info("**Request to post handler!")
            logging.info('req url: ' + self.request.uri)
            dic = dict()
            print('args list:', self.request.arguments)
            for k in self.request.arguments.keys():
                v = self.get_argument(k, default=None, strip=False)
                dic.update({k: v})
            sender_obj = sender_sms(dic)
            if sender_obj != 0:
                sender_obj.send()
            self.write('200')
        except Exception as e:
            logging.info("error in SendSmsHandler: %s" % str(e))


class SendWeixinHandler(CatAlertHandler):

    def get(self):
        self.write('hello weixin')

    def post(self):
        try:
            logging.info("**Request to post handler!")
            logging.info('req url: ' + self.request.uri)
            dic = dict()
            print('args list:', self.request.arguments)
            for k in self.request.arguments.keys():
                v = self.get_argument(k, default=None, strip=False)
                dic.update({k: v})
            sender_obj = sender_weixin(dic)
            if sender_obj != 0:
                sender_obj.send()
            self.write('200')
        except Exception as e:
            logging.info("error in SendWeixinHandler: %s" % str(e))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/get", GetHandler),
    (r"/post", PostHandler),
    (r"/mail/", SendMailHandler),
    (r"/sms/", SendSmsHandler),
    (r"/weixin/", SendWeixinHandler),
])

if __name__ == "__main__":
    application.listen(9000)
    print("main 1 getEffectiveLevel = ", LOG.getEffectiveLevel())
    print("tornado default log level = ", tornado.options.options.logging)
    tornado.options.options.logging = "debug"  # % dt.now().strftime('%Y%m%d-%H%M%S')
    tornado.options.parse_command_line()

    print("main getEffectiveLevel = ", LOG.getEffectiveLevel())
    tornado.ioloop.IOLoop.instance().start()

