from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import csv

from flask import Flask, render_template, redirect, jsonify


Base = declarative_base()

 class Breweries(Base):
     __tablename__ = 'breweries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    lat = Column(Integer)
    lon = Column(Integer)
    link = Column(String)

class Beers(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    beer = Column(String)
    style = Column(String)
    abv = Column(Integer)
    ibu = Column(Integer)

engine = create_engine('sqlite:///breweries.sqlite')
session = Session(engine)
Base.metadata.create_all(engine)

with open('./data/breweries.csv') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    for Breweries_Brewery, Name, Score, Style, ABV, Address, Lat, Lon, Link in reader:
        session.add(Breweries(
            name=Breweries_Brewery,
            address=Address,
            lat=Lat,
            lon=Lon,
            link=Link
        ))

        session.add(Beers(
                abv=ABV,
                name=Breweries_Brewery,
                beer=Name,
                score=Score,
                style=Style
            ))

    session.commit()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/search')
def markers():
    return render_template('search.html')

@app.route('/breweries')
def breweries():
    session = Session(engine)
    results = []
    for result in session.query(Breweries.name, Breweries.address, Breweries.lat, Breweries.lon, Breweries.link).group_by(Breweries.name).all():
        brewery_dict = {}
        brewery_dict['name'] = result.name
        brewery_dict['address'] = result.address
        brewery_dict['lat'] = result.lat
        brewery_dict['lon'] = result.lon
        brewery_dict['link'] = result.link
        results.append(brewery_dict)
    return jsonify(results)

@app.route('/menu/<brewery>')
def menu(brewery):
    session = Session(engine)
    beers = []
    for beer in session.query(Beers).filter(Beers.name == brewery).all():
        beer_dict = {}
        beer_dict['ABV'] = beer.abv
        beer_dict['Brewery'] = beer.name
        beer_dict['Beer'] = beer.beer
        beer_dict['Style'] = beer.style
        beer_dict['Score'] = beer.score
        beers.append(beer_dict)

    return jsonify(beers)

@app.route('/table_data')
def table_data():
    session = Session(engine)
    table_data = []
    for entry in session.query(Beers).all():
        search_dict = {}
        search_dict['ABV'] = entry.abv
        search_dict['Brewery'] = entry.name
        search_dict['Beer'] = entry.beer
        search_dict['Style'] = entry.style
        search_dict['Score'] = entry.score
        table_data.append(search_dict)

    return jsonify(table_data)

# Breweries.__table__.drop(engine)
# Beers.__table__.drop(engine)

if __name__ == '__main__':
    app.run(debug=True)
