from  flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model,UserMixin):
    __tablename__="admin"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    email = db.Column(db.Integer ,unique = True)
    password = db.Column(db.String)
    def get_id(self):
        return self.email


class Customer(db.Model,UserMixin):
    __tablename__="customer"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    email = db.Column(db.Integer ,unique = True)
    name = db.Column(db.String)
    password = db.Column(db.String )
    address = db.Column(db.String)
    status = db.Column(db.String,nullable = False)
    city = db.Column(db.String)
    sent_bookings = db.relationship("Booking",backref = "customer")
    def get_id(self):
        return self.email
    
class ServiceCategory(db.Model):
    __tablename__="servicecategory"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True) 
    name = db.Column(db.String,nullable = False , unique=True)
    descripiton = db.Column(db.String,nullable = False)
    base_price = db.Column(db.Integer)
    all_plans = db.relationship("ServicePlan",backref = "category")
    all_professional = db.relationship("Professional",backref = "category")


class Professional(db.Model,UserMixin):
    __tablename__="serviceprofessional"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    email = db.Column(db.Integer ,unique = True)
    name = db.Column(db.String,nullable = False)
    status = db.Column(db.String,nullable = False)
    password = db.Column(db.String )
    city = db.Column(db.String,nullable = False)
    experiance = db.Column(db.String , nullable= False)
    categroy_id = db.Column(db.Integer,db.ForeignKey("servicecategory.id"), nullable = False)
    recive_bookings = db.relationship("Booking",backref = "professional")
    all_plans = db.relationship("ServicePlan",backref = "professional")
    def get_id(self):
        return self.email


class ServicePlan(db.Model):
    __tablename__="serviceplan"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String,nullable = False)
    descripiton = db.Column(db.String,nullable = False)
    price = db.Column(db.Integer)
    categroy_id = db.Column(db.Integer,db.ForeignKey("servicecategory.id"), nullable = False)
    professional_id = db.Column(db.Integer , db.ForeignKey("serviceprofessional.id"), nullable = False)
    assoiciated_booking = db.relationship("Booking",backref = "plan")


class Booking(db.Model):
    __tablename__="Booking"
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    status = db.Column(db.String,nullable = False)
    rating = db.Column(db.Integer)
    customer_id = db.Column(db.Integer , db.ForeignKey("customer.id"), nullable = False)
    professional_id = db.Column(db.Integer , db.ForeignKey("serviceprofessional.id"), nullable = False)
    service_plan_id = db.Column(db.Integer , db.ForeignKey("serviceplan.id"), nullable = False)


