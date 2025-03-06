from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Resource, Api, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db= SQLAlchemy(app)
api = Api(app)

class Meal(db.Model):
    __tablename__= 'meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Date, default=datetime.today, nullable=False)
    calories = db.relationship('Calorie', back_populates='meal', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Meal(day = {self.day}, calories = {self.calories})'

class Calorie(db.Model):
    __tablename__  = 'calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_item = db.Column(db.String(255), nullable=False)
    calorie_count = db.Column(db.Integer, nullable=False)
    meal = db.relationship('Meal', back_populates='calories')


calorieFields = {
    'id': fields.Integer,
    'food_item': fields.String,
    'calorie_count': fields.Integer,
}

mealFields = {
    'id': fields.Integer,
    'day': fields.String,
    'calories': fields.List(fields.Nested(calorieFields))
}

class Meals(Resource):
    @marshal_with(mealFields)
    def get(self):
        meals = Meal.query.all()
        return meals
    
    @marshal_with(mealFields)
    def post(self):
        data = request.json
        try:
            day = datetime.strptime(data['day'], '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Invalid date format, use YYYY-MM-DD.'}, 400
        meal = Meal(day = day)
        for calorie in data['calories']:
            calorie_item = Calorie(
                food_item = calorie['food_item'],
                calorie_count = calorie['calorie_count']
            )
            meal.calories.append(calorie_item)
            
        db.session.add(meal)
        db.session.commit()
        return meal, 201
    
class get_meal(Resource):
    @marshal_with(mealFields)
    def get(self, id):
        meal = Meal.query.filter_by(id = id).first()
        if not meal:
            abort(404)
        return meal 
    
    @marshal_with(mealFields)
    def patch(self, id):
        data = request.get_json()
        meal = Meal.query.filter_by(id = id).first()
        if not meal:
            abort(404)
        if 'day'in data:
            try:
                meal.day = datetime.strptime(data['day'], '%Y-%m-%d').date()
            except ValueError:
                return {'message': 'Invalid date format. use YYYY-MM-DD'},400
        
        if 'calories' in data:
            meal.calories.clear()
            for calorie in data['calories']:
                try:
                    calorie_item  = Calorie(
                        food_item = calorie['food_item'],
                        calorie_count = calorie['calorie_count']
                    )
                    meal.calories.append(calorie_item)
                except KeyError:
                    return {'message': 'Each calorie entry must include a food item and calorie count.'}
        db.session.commit()
        return meal, 200

    @marshal_with(Resource)
    def delete(self, id):
        meal = Meal.query.filter_by(id = id).first()
        if not meal:
            abort(404)
        db.session.delete(meal)
        db.session.commit()
        return 'meal deleted'
    
api.add_resource(Meals, '/api/meals/')
api.add_resource(get_meal, '/api/meals/<int:id>')

@app.route('/')
def index():
    return '<h1>api for calculating calories</h1>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=42069, debug=True)
