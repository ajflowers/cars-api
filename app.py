import re
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cars_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors
    
    def __repr__(self):
        return f"<car {self.name}>"


@app.route('/')
def hello():
    return {"hello": "world"}


@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format."}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "id": car.id,
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        

        return {"count": len(results), "cars": results}

@app.route('/cars/<car_id>', methods = ['GET'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return {"message": "success", "car": response}

if __name__ == '__main__':
    app.run(debug=True)