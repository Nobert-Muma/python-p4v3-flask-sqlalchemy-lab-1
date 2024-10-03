# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    earthquake=Earthquake.query.filter(Earthquake.id==id).first()
    if earthquake:
        body={
            'id':earthquake.id,
            'location':earthquake.location,
            'magnitude':earthquake.magnitude,
            'year':earthquake.year
        }
        status_code=200
        headers={}
    else:
        body={
            'message':'Earthquake 9999 not found.'
        }
        status_code=404
        headers={}
    return make_response(body, status_code, headers)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def find_magnitude(magnitude):
    earthquakess=Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    earthquakes=[]
    if earthquakess:
        for earthquake in earthquakess:
            earthquakes.append(earthquake)
        response_body={
            'count':len(earthquakes),
            'quakes':earthquakes
        }
        status_code=200
        headers={}
    else:
        response_body={
            'count':0,
            'quakes':[]
        }
        status_code=200
        headers={}
    return make_response(response_body, status_code, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
