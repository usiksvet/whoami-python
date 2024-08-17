import os

from flask import Flask, request

app = Flask(__name__, instance_relative_config=True)

@app.route('/ip')
def ip():
  ip_address = request.remote_addr
  return ip_address

@app.route('/healthcheck')
def healthcheck():
  return "OK"
