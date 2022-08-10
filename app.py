import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth

from models import Actor,  Movie, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()
        if len(actors) == 0:
            abort(404)
        formated = []
        for actor in actors:
            formated.append(actor.format())
        return jsonify({'success': True, 'actors': formated})

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actor')
    def add_actor(jwt):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name is None or age is None or gender is None:
            abort(422)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({'success': True, 'actor': actor.format()})

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='post:actor')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({"success": True, "deleted": actor_id})
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actor')
    def modify_actor(jwt, actor_id):
        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name is not None:
            actor.name = name
        if age is not None:
            actor.age = age
        if gender is not None:
            actor.gender = gender
        actor.update()
        return jsonify({'success': True, 'actor': actor.format()})

    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movie(jwt):
        movies = Movie.query.order_by(Movie.id).all()
        if len(movies) == 0:
            abort(404)
        formated = []
        for movie in movies:
            formated.append(movie.format())
        return jsonify({'success': True, 'movies': formated})

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movie')
    def create_movie(jwt):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        cast = body.get('cast', None)
        if title is None or release_date is None or cast is None:
            abort(422)
        actors = []
        for c in cast:
            actor = Actor.query.filter(
                Actor.id == c).one_or_none()
            if actor is None:
                abort(404)
            actors.append(actor)
        movie = Movie(title=title, release_date=release_date)
        movie.insert(actors)
        return jsonify({'success': True})

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='post:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({"success": True, "deleted": movie_id})
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movie')
    def modify_movie(jwt, movie_id):
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        cast = body.get('cast', None)
        if title is not None:
            movie.name = title
        if release_date is not None:
            movie.release_date = release_date
        if cast is not None:
            movie.cast = []
            for c in cast:
                actor = Actor.query.filter(
                    Actor.id == c).one_or_none()
                if actor is None:
                    abort(404)
                movie.cast.append(actor)

        movie.update()
        return jsonify({'success': True, 'movie': movie.format()})

    # Cathces and handels 404 error

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    # Catches unprocessed errors

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False, 'error': 422, 'message': 'unprocessable'
        }), 422)
    # Cathces and handels authorization errors such as 401 and 403

    @app.errorhandler(AuthError)
    def auth_error(er):
        return jsonify({
            "success": False,
            "error": er.status_code,
            "message": er.error['description']
        }), er.status_code

    return app


# 404-422-400-401-403
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
