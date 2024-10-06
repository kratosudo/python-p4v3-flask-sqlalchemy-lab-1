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

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the database for the earthquake with the given ID
    earthquake = Earthquake.query.get(id)
    
    # If the earthquake is found, return its details
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    
    # If not found, return an error message
    else:
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitude >= parameter value
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the response data
    response_data = {
        "count": len(quakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
            for quake in quakes
        ]
    }
    
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
