
import json
import os
import webbrowser
from functools import wraps

from flask import Flask, url_for, render_template, jsonify, request, make_response
import webview

gui_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')  # development path

if not os.path.exists(gui_dir):  # frozen executable path
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')

server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching

@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@server.route('/')
def landing():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    return render_template('index.html', token=webview.token)


def run_server():
    server.run(host='127.0.0.1', port=23948, threaded=True)


if __name__ == '__main__':
    run_server()