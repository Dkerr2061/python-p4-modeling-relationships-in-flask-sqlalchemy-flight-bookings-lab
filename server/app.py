#!/usr/bin/env python3
import ipdb

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Flight, Customer, Booking

app = Flask(__name__)

# configure a database connection to the local file examples.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

@app.route('/')
def index():
    flight = len(Flight.query.all())
    customer = len(Customer.query.all())
    booking = len(Booking.query.all())
    return f"<h1>Welcome! We have these number of flights {flight}, these many customers {customer} and these many bookings {booking}!</h1>"

@app.route('/flights')
def all_flights():
    flights = Flight.query.all()
    flight_list_in_dicts = [flight.to_dict(only=('id', 'airline')) for flight in flights]
    return make_response(flight_list_in_dicts, 200)

@app.route('/flights/<int:id>')
def flight_by_id(id):
    flight = db.session.get(Flight, id)

    if flight:
        body = flight.to_dict(rules=('-bookings.flight', '-bookings.customer'))
        status = 200
    else:
        body = {"message": f"Flight {id} was not found"}
        status = 404
    return make_response(body, status)

@app.route('/customers')
def all_customers():
    customers = Customer.query.all()
    customer_list_in_dict = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in customers]
    return make_response(customer_list_in_dict, 200)

@app.route('/customers/<int:id>')
def customer_by_id(id):
    customer = db.session.get(Customer, id)

    if customer:
        body = customer.to_dict(rules=('-bookings.customer', '-bookings.flight'))
        status = 200
    else:
        body = {"message": f"The customer {id} was not found."}
        status = 404
    return make_response(body, status)

@app.route('/bookings')
def all_bookings():
    bookings = Booking.query.all()
    booking_list_in_dict = [booking.to_dict(only=('id', 'price', 'destination', 'customer_id', 'flight_id')) for booking in bookings]
    return make_response(booking_list_in_dict, 200)

@app.route('/bookings/<int:id>')
def booking_by_id(id):
    booking = db.session.get(Booking, id)

    if booking:
        body = booking.to_dict(rules=('-flight.bookings', '-customer.bookings'))
        status = 200
    else:
        body = {"message": f"Booking {id} was not found."}
    return make_response(body, status)


if __name__ == "__main__":
    app.run(port=7777, debug=True)