from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/breweries.sqlite"

db = SQLAlchemy(app)

class Breweries(db.Model):
    __tablename__ = 'breweries'
    id = db.Column(db.Integer, primary_key=True)
    brewery = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)
    link = db.Column(db.String)

    def __repr__(self):
        return '<Breweries %r>' % (self.name)

class Beers(db.Model):
    __tablename__ = "beers"
    id = db.Column(db.Integer, primary_key=True)
    beer = db.Column(db.String)
    style = db.Column(db.String)
    abv = db.Column(db.Integer)
    ibu = db.Column(db.Integer)
    brewery = db.Column(db.String)

    def __repr__(self):
        return '<Beers %r>' % (self.name)

# Create database classes
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def markers():
    return render_template('search.html')

@app.route('/breweries')
def breweries():
    results = []
    for result in db.session.query(Breweries.brewery, Breweries.address, Breweries.city, Breweries.state, Breweries.lat, Breweries.lon, Breweries.link).group_by(Breweries.brewery).all():
        brewery_dict = {}
        brewery_dict['brewery'] = result.brewery
        brewery_dict['address'] = result.address
        brewery_dict['city'] = result.city
        brewery_dict['state'] = result.state
        brewery_dict['lat'] = result.lat
        brewery_dict['lon'] = result.lon
        brewery_dict['link'] = result.link
        results.append(brewery_dict)
    return jsonify(results)

@app.route('/menu/<brewery>')
def menu(brewery):
    beers = []
    for entry in db.session.query(Beers).filter(Beers.brewery == brewery).all():
        beer_dict = {}
        beer_dict['abv'] = entry.abv
        beer_dict['brewery'] = entry.brewery
        beer_dict['beer'] = entry.beer
        beer_dict['style'] = entry.style
        beer_dict['ibu'] = entry.ibu
        beers.append(beer_dict)

    return jsonify(beers)

@app.route('/search/<city>')
def table_city():
    table_city = []
    for c in db.session.query(Brewery_Beer).filter(Brewery_Beer.city == city).all():
        search_dict = {}
        search_dict['abv'] = c.abv
        search_dict['brewery'] = C.brewery
        search_dict['beer'] = c.beer
        search_dict['style'] = c.style
        search_dict['ibu'] = c.ibu
        table_data.append(search_dict)

    return jsonify(table_city)

@app.route('/search/<state>')
def table_state():
    table_state = []
    for s in db.session.query(Brewery_Beer).filter(Brewery_Beer.state == state).all():
        search_dict = {}
        search_dict['abv'] = s.abv
        search_dict['brewery'] = s.brewery
        search_dict['beer'] = s.beer
        search_dict['style'] = s.style
        search_dict['ibu'] = s.ibu
        table_data.append(search_dict)

    return jsonify(table_state)

if __name__ == '__main__':
    app.run(debug=True)
