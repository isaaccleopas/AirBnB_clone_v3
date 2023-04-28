#!/usr/bin/python3

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""The Flask web application instance"""


app.register_blueprint(app_views)
