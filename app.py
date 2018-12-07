from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import csv

from flask import Flask, render_template, redirect, jsonify


Base = declarative_base()

class Breweries(Base):
    __tablename__ = 'breweries'
    id = Column(Integer, primary_key=True)
    brewery = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    lat = Column(Integer)
    lon = Column(Integer)
    link = Column(String)

class Beers(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True)
    brewery = Column(String)
    beer = Column(String)
    style = Column(String)
    abv = Column(Integer)
    ibu = Column(Integer)

engine = create_engine('sqlite:///breweries.sqlite')
session = Session(engine)
Base.metadata.create_all(engine)

with open('./data/breweries_final.csv', encoding='utf8') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    for brewery, beer, abv, ibu, style, address, city, state, latitude, longitude, website in reader:
        session.add(Breweries(
            brewery=brewery,
            address=address,
            lat=latitude,
            lon=longitude,
            link=website
        ))

        session.add(Beers(
                beer=beer,
                abv=abv,
                ibu=ibu,
                style=style,
                brewery=brewery
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
    for result in session.query(Breweries.brewery, Breweries.address, Breweries.lat, Breweries.lon, Breweries.link).group_by(Breweries.name).all():
        brewery_dict = {}
        brewery_dict['brewery'] = result.brewery
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
    for beer in session.query(Beers).filter(Beers.beer == brewery).all():
        beer_dict = {}
        beer_dict['abv'] = beer.abv
        beer_dict['brewery'] = beer.brewery
        beer_dict['beer'] = beer.beer
        beer_dict['style'] = beer.style
        beer_dict['ibu'] = beer.ibu
        beers.append(beer_dict)

    return jsonify(beers)

@app.route('/table_data')
def table_data():
    session = Session(engine)
    table_data = []
    for entry in session.query(Beers).all():
        search_dict = {}
        search_dict['abv'] = entry.abv
        search_dict['brewery'] = entry.brewery
        search_dict['beer'] = entry.beer
        search_dict['style'] = entry.style
        search_dict['ibu'] = entry.ibu
        table_data.append(search_dict)

    return jsonify(table_data)

# Breweries.__table__.drop(engine)
# Beers.__table__.drop(engine)

if __name__ == '__main__':
    app.run(debug=True)
