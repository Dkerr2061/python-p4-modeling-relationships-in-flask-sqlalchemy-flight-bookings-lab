from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# contains definitions of tables and associated schema constructs
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
class Flight(db.Model, SerializerMixin):
    __tablename__ = 'flights'

    # serialize_rules = ('-bookings.flight', '-bookings.customer')

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String)

    bookings = db.relationship('Booking', back_populates='flight', cascade='all')

    def __repr__(self):
        return f"<Flight # {self.id}, airline: {self.airline}>"

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # serialize_rules = ('-bookings.flight', '-bookings.customer')

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    bookings = db.relationship('Booking', back_populates='customer', cascade='all')

    flights = association_proxy('bookings', 'flight', creator=lambda flight_obj: Booking(flight= flight_obj))

    def __repr__(self):
        return f"<Customer # {self.id}, First name: {self.first_name}, Last name: {self.last_name}>"

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    # serialize_rules = ('-customer.bookings', '-flight.bookings')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    destination = db.Column(db.String)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    flight = db.relationship('Flight', back_populates='bookings')

    customer = db.relationship('Customer', back_populates='bookings')

    def __repr__(self):
        return f"<Booking # {self.id}, Price: {self.price}, Destination: {self.destination}, Flight ID: {self.flight_id}, Customer ID: {self.customer_id}>"