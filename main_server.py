# 所有的请求全部使用 Basic Auth
import json
import logging
import os
import sys
import time
import traceback
from json import JSONDecodeError
from logging import handlers

from flask_cors import CORS
from flask import Flask, request, jsonify, g

# 定义logger: 放在头部就好
from playhouse.shortcuts import model_to_dict

from config import PORT

# 初始化app
from libs.envs import setup_app, ELC_LOGGER, DATABASE_APP_PROXY
from libs.models import ELC_TABLES, FunctionModel

app = Flask(__name__)
CORS(app)


@app.before_request
def _start_timer():
    g.request_start_time = time.time()
    DATABASE_APP_PROXY.connect()

@app.teardown_request
def _end_timer(exc):
    if not DATABASE_APP_PROXY.is_closed():
        DATABASE_APP_PROXY.close()
    ELC_LOGGER.logger.info('[time stat] total: {:.5g}s'.format(time.time() - g.request_start_time))


@app.route('/api/functions', methods=['GET'])
def get_operators():
    functions = FunctionModel.select()
    return jsonify({"status": "ok", "result": [model_to_dict(f) for f in functions]}), 200


# 发起一次运行
@app.route('/api/run', methods=['POST'])
def start_run():
    return jsonify({"status": "ok"}), 200


# 得到所有运行的列表
@app.route('/api/runs', methods=['GET'])
def get_runs():
    return jsonify({"status": "ok"}), 200


# 得到运行的详情
@app.route('/api/run/<run_id>', methods=['POST'])
def get_run_detail(run_id):
    return jsonify({"status": "ok"}), 200


def init_app():
    with DATABASE_APP_PROXY:
        # 确保table存在
        DATABASE_APP_PROXY.create_tables(ELC_TABLES)
        _elc_add = FunctionModel.get_or_create(name='elc_add')[0]
        _elc_add.outputs = ['sum_result']
        _elc_add.inputs = ['a', 'b']
        _elc_add.save()
        _elc_mul = FunctionModel.get_or_create(name='elc_mul')[0]
        _elc_mul.outputs = ['mul_result']
        _elc_mul.inputs = ['a', 'b']
        _elc_mul.save()
        _elc_pow = FunctionModel.get_or_create(name='elc_pow')[0]
        _elc_pow.outputs = ['pow_result']
        _elc_pow.parameters = {'a': 2}
        _elc_pow.inputs = ['x']
        _elc_pow.save()


if __name__ == '__main__':
    setup_app()
    init_app()
    app.run(host='0.0.0.0', port=PORT, debug=True)
