#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''


class Scientists(Resource):

    def get(self):
        scientists = [scientist.to_dict(only=('id', 'name', 'field_of_study')) for scientist in Scientist.query.all()]

        return make_response(
            scientists,
            200
        )
    
    def post(self):
        try:
            new_scientist = Scientist(
                name=request.json.get('name'),
                field_of_study=request.json.get('field_of_study')
            )

            db.session.add(new_scientist)
            db.session.commit()

            return make_response(new_scientist.to_dict(), 201)
        except:
            return make_response({"errors": ["validation errors"]}, 400)
        
    
api.add_resource(Scientists, '/scientists')

class ScientistByID(Resource):

    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()

        if scientist:
            response = scientist.to_dict(rules=('-missions.scientist', '-missions.planet.missions'))
            return make_response(response, 200)
        else:
            response = make_response(
                {"error": "Scientist not found"},
                404
            )
            return response
        
    def patch(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        if(scientist):
            try:
                for attr in request.json:
                    setattr(scientist, attr, request.json[attr])

                db.session.commit()
                response = scientist.to_dict(only=('id', 'name', 'field_of_study'))
                return make_response(response, 202)
            except:
                response = {
                    "errors": ["validation errors"]
                }
                return make_response(response, 400)
        else:
            response = {
                "error": "Scientist not found"
            }
            return make_response(response, 404)
            
    def delete(self, id):
        scientist = db.session.get(Scientist, id)

        if(scientist):
            db.session.delete(scientist)
            db.session.commit()
            response = {}
            return make_response(response, 204)
        else:
            response = {
                "error": "Scientist not found"
            }
            return make_response(response, 404)
        
api.add_resource(ScientistByID, '/scientists/<int:id>')

class Planets(Resource):

    def get(self):
        planets = [planet.to_dict(only=('id', 'name', 'distance_from_earth', 'nearest_star')) for planet in Planet.query.all()]

        return make_response(
            planets,
            200
        )
        
api.add_resource(Planets, '/planets')

class NewMission(Resource):

    def post(self):
        try:
            new_mission = Mission(
                name=request.json.get('name'),
                scientist_id=request.json.get('scientist_id'),
                planet_id=request.json.get('planet_id')
            )

            db.session.add(new_mission)
            db.session.commit()
            response = new_mission.to_dict(rules=('-planet.missions', '-scientist.missions'))
            return make_response(response, 201)
        except:
            response = {
                "errors": ["validation errors"]
            }
            return make_response(response, 400)
        
api.add_resource(NewMission, '/missions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
