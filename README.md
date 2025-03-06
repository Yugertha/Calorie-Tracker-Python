This page is the planner and journal for the back-end that is in conjunction with the  [[planner for the app]] pages.

In this page I will go through the steps that I took to make the back-end in python using flask and sqlalchemy as a libraries with the help of [Dave Gray's resource](https://www.youtube.com/watch?v=z3YMz-Gocmw&list=WL&index=3) 

I will try to go through all of the steps that I took in order to make it so that I understand them better and so that I improve on them and add features that I have the vision to add like a workout tracker and global syncing. 

## configuring the environment 

- first create the folder
- create the python env 
```bash
python -m venv .venv
```

- activate the environment 
```bash
source .venv/Scripts/activate
```

- create the api file
```bash
touch api.py
```

- add the packages that are required:
```bash
pip install flask flask_restful flask_sqlalchemy
```

- generate the requirement file for future use 
```bash
pip freeze > requiremnet.txt
```

- now start importing the dependencies into the api.py
```python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshall_with, abort
from datetime import datetime
```

- add the app flask
- and run the app in debug mode(only during dev delete debug for prod)
- create the models 
```python
class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Date, default=datetime.today, nullable=False)
    calories = db.relationship('Calorie', back_populates='meal', cascade='all, delete orphan')

    def __repr__(self):
        return f'Meal(day = {Meal.day}, calories = {Meal.calories})'
    
class Calorie(db.Model):
    __tablename__ = 'calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_item = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', back_populates='calories')
```

