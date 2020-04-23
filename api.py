import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Movie
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

@app.route('/movies')
def get_movies():
    selection = Movie.query.order_by(Movie.id).all()

    return "hi"