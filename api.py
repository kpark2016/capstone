import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
#from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

@app.route('/movies')
def get_movies():
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]

    return jsonify({
        'success': True,
        'movies': movies,
        'totalMovies': len(Movie.query.all())
    })

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    
    if movie is None:
        abort(404)

    try:
        movie.delete()
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        return jsonify({
            'success': True,
            'deleted': movie_id,
            'movies': movies,
            'totalMovies': len(Movie.query.all())
        })

    except:
        abort(422)

@app.route('/movies', methods=['POST'])
def create_movie():
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    try:
        movie = Movie(
            title=title,
            release_date=release_date,
            )

        movie.insert()
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        return jsonify({
            'success': True,
            'created': movie.id,
            'movies': movies,
            'totalMovies': len(Movie.query.all())
        })

    except:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    try:
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        movie.title = title
        movie.release_date = release_date
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        return jsonify({
            'success': True,
            'updated': movie.id,
            'movies': movies,
            'totalMovies': len(Movie.query.all())
        })

    except:
        abort(422)

@app.route('/actors')
def get_actors():
    selection = Actor.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in selection]

    return jsonify({
        'success': True,
        'actors': actors,
        'totalActors': len(Actor.query.all())
    })

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    
    if actor is None:
        abort(404)

    try:
        actor.delete()
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        return jsonify({
            'success': True,
            'deleted': actor_id,
            'actors': actors,
            'totalActors': len(Actor.query.all())
        })

    except:
        abort(422)

@app.route('/actors', methods=['POST'])
def create_actor():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
        actor = Actor(
            name=name,
            age=age,
            gender=gender
            )

        actor.insert()
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        return jsonify({
            'success': True,
            'created': actor.id,
            'actors': actors,
            'totalActors': len(Actor.query.all())
        })

    except:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
def update_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    try:
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        actor.name = name
        actor.age = age
        actor.gender = gender

        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        return jsonify({
            'success': True,
            'updated': actor.id,
            'actors': actors,
            'totalActors': len(Actor.query.all())
        })

    except:
        abort(422)