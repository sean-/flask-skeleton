# -*- coding:utf-8 -*-
from flask import render_template, request

from home import module

@module.route('/')
def index():
    remote_addr = request.environ['REMOTE_ADDR']
    return render_template('home/index.html', remote_addr=remote_addr)
