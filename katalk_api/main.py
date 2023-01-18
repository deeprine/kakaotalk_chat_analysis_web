import operator

from sanic import Sanic, response
from sanic.response import json
from concurrent.futures import ThreadPoolExecutor
import os
import argparse
import sys
import time
import re

from datetime import datetime
from time import gmtime, strftime, localtime

import asyncio
import logging.config
import argparse
from sanic_jinja2 import SanicJinja2
from sanic_session import Session
import jinja2
import datetime
import pandas as pd
from time import sleep

from katalk_preprocessing import *

import ssl

logging.config.fileConfig('./configs/logging.conf', disable_existing_loggers=False)

path=os.path.join(os.path.dirname(__file__), 'templates')
templateLoader = jinja2.FileSystemLoader(searchpath=path)
templateEnv = jinja2.Environment(loader=templateLoader)

app = Sanic(__name__)
# app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.static('/static', './static')

# session = Session(app, interface=InMemorySessionInterface())
jinja = SanicJinja2(app, session=Session)
# session_interface = InMemorySessionInterface()
logger = logging.getLogger(__name__)
streamHandler = logging.StreamHandler()
fileMaxByte = 1024 * 1024 * 100
fileHandler = logging.handlers.RotatingFileHandler('leekatalk.log', maxBytes=fileMaxByte, backupCount=10)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel('INFO')

current_time = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]

def get_duration(start_time, use_str=True):
    process_time = (time.time() - start_time) * 1000
    if use_str:
        process_time = '{0:.2f}'.format(process_time)
    return process_time

# def check_input(input_data, requred_fields):
#     for field_key in requred_fields:
#         if field_key not in input_data:
#             return False, field_key
#     return True, ''

def printError(err, logger):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.error(f"error={repr(err)}")
    logger.error(f"exc_type={repr(exc_type)}, filename={repr(fname)}, line_no={repr(exc_tb.tb_lineno)}")

def printError2(err):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f"error={repr(err)}")
    print(f"exc_type={repr(exc_type)}, filename={repr(fname)}, line_no={repr(exc_tb.tb_lineno)}")

async def server_error_handler(request, exception):
    printError(exception, logger)
    template = templateEnv.get_template("500.html")
    return jinja.render(template, request)

app.error_handler.add(Exception, server_error_handler)

# @app.middleware('request')
# async def add_session_to_request(request):
#     # before each request initialize a session
#     # using the client's request
#     await session_interface.open(request)
#
# @app.middleware('response')
# async def save_session(request, response):
#     # after each request save the session,
#     # pass the response to set client cookies
#     await session_interface.save(request, response)

@app.route('/information')
async def information(request):
    template = templateEnv.get_template('/gaein.html')
    return jinja.render(template, request, current_time = current_time)

@app.route('/')
async def main_page(request):
    template = templateEnv.get_template('/index.html')
    return jinja.render(template, request, current_time = current_time)

@app.route("/file_process", methods=['GET', 'POST'])
async def file_process(request):
    if request.method == 'POST':
        if request.files['katalk_file'][0].body:
            file = request.files['katalk_file'][0].body
            txt_name = 'katalk_file.txt'

            with open(txt_name, "wb") as binary_file:
                binary_file.write(file)
                binary_file.close()

            result, title, user_unique = kakaotalk_api(txt_name)
            if len(user_unique) > 2:
                danche = True
            else:
                danche = False

            os.remove('katalk_file.txt')
            template = templateEnv.get_template('/result_page.html')
            return jinja.render(template, request, result = result, title = title, current_time = current_time,
                                user_unique =  user_unique, danche = danche)

    return response.redirect('/index.html')

# @app.route("/")
# async def index(request):
#     return response.redirect('/index.html')

if __name__ == "__main__":
    # ssl = {'cert': '/root/katalk/cert.crt',ㅎ 'key': '/root/katalk/cert.key'}
    app.run(host="127.0.0.1", port=8080, debug=True)
    # app.run(host="0.0.0.0", port=8888, debug=True)
