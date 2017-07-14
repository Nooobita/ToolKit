# -*- coding=utf8 -*-

import time


def application(env, start_response):

    status = "200 OK"
    response_header = [('Content-Type', 'text/plain')]

    start_response(status, response_header)
    return [str(env)+"==Hello world from a simple WSGI application!--->%s\n"%time.ctime()]