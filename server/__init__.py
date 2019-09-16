from flask import Flask, render_template, request, json, jsonify
from flask_static_compress import FlaskStaticCompress
import jinja2
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import uuid


from core.utils import makeError


# new app
app = Flask(__name__, root_path='.')
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.static_folder = 'static'
FlaskStaticCompress(app)
