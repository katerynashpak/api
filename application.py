from flask import Flask, request

#can find this in the documentation for flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 




#create sqlite database called data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



class Drink(db.Model): #for sql alchemy we define the columns id, name, and description
    id = db.Column(db.Integer, primary_key=True) #create an id column
    name = db.Column(db.String(80), unique=True, nullable=False) #create a name column
    description = db.Column(db.String(120)) #create a description column

    def __repr__(self): #self is the object, this function is used every time we print a drink
        return f"{self.name} - {self.description}"





@app.route('/') #route #a decorator that Flask provides to assign URLs in our app to functions easily
def index(): #create a method
    return 'Hello!'



@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}

        output.append(drink_data)

    return {"drinks": output}



@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "yeet!@"}