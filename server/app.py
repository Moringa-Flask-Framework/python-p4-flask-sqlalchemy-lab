#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id==id).first()
    # print(animal)
    if not animal:
        response= make_response('<h1>No such animal</h1>', 404)
        return response
    else:
        response_body=f'''
        <h1>Animal details</h1>
        <ul>
            <li>ID: {animal.id}</li>
            <li>Name: {animal.name}</li>
            <li>Species: {animal.species}</li>
            <li>Zookeper: {animal.zookeeper.name}</li>
            <li>Enclosure: {animal.enclosure.environment}</li>
        </ul>
        
        '''
        response= make_response(response_body, 200)
        return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zk = Zookeeper.query.filter(Zookeeper.id== id).first()
    if not zk:
        response= make_response ('<h1>No zokeeper with id {id}</h1>', 404)
    else:
        animals= [animal for animal in zk.animals]
        if not animals:
            response_body='This zokeeper does not work with any animals'
            response = make_response(response_body, 404)
            return response
        else:
            for animal in animals:
                response_body= f'''
                <h3>Informations about zookeeper {zk.name}:</h3>
                <ul>
                    <li>ID: {zk.id}</li>
                    <li>Name: {zk.name}</li>
                    <li>Animal: {animal.name}</li>
                </ul>
                    '''
                response= make_response(response_body, 200)
                return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure= Enclosure.query.filter(Enclosure.id==id).first()
    if not enclosure:
        response=make_response('<h1>No such enclosure.</h1>',404)
        return response
    else:
        animals= [animal for animal in enclosure.animalss]
        if not animals:
            response_body=f"There are no animals in this enclosure."
            response= make_response(response_body, 404)
            return response
        else:
            for animal in animals:
                response_body= f'''
                <h3>Enclosure Details</h3>     
                <li>ID: {enclosure.id}</l1> 
                <li>Name: {enclosure.environment}</li>
                <li>Open to Visitors {enclosure.open_to_visitors}</li>
                <li>Animal: {animal.name}</li>
                '''
                response=make_response(response_body, 200)
                return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
