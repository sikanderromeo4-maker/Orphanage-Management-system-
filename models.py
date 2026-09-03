from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='Staff')
    
    def get_id(self):
        return str(self.admin_id)

class Children(db.Model):
    __tablename__ = 'children'
    child_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    admission_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    residential_status = db.Column(db.String(50), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    medical_records = db.relationship('MedicalRecords', backref='child', cascade="all, delete-orphan")
    educational_records = db.relationship('EducationRecords', backref='child', cascade="all, delete-orphan")
    adoptions = db.relationship('Adoptions', backref='child', cascade="all, delete-orphan")

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    expenses = db.relationship('Expenses', backref='staff')

class Donors(db.Model):
    __tablename__ = 'donors'
    donor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    donor_type = db.Column(db.String(50), nullable=False)
    donations = db.relationship('Donations', backref='donor', cascade="all, delete-orphan")

class Donations(db.Model):
    __tablename__ = 'donations'
    donation_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id', ondelete="CASCADE"), nullable=False)
    amount_or_item = db.Column(db.String(100), nullable=False)
    donation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

class Volunteers(db.Model):
    __tablename__ = 'volunteers'
    volunteer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    assigned_duty = db.Column(db.String(100), nullable=False)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    item_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    reorder_threshold = db.Column(db.Integer, nullable=False, default=10)
    expenses = db.relationship('Expenses', backref='item')

class Expenses(db.Model):
    __tablename__ = 'expenses'
    expense_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id', ondelete="SET NULL"), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete="SET NULL"), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

class MedicalRecords(db.Model):
    __tablename__ = 'medical_records'
    record_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.child_id', ondelete="CASCADE"), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    visit_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

class EducationRecords(db.Model):
    __tablename__ = 'education_records'
    record_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.child_id', ondelete="CASCADE"), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    term = db.Column(db.String(20), nullable=False)

class Visitors(db.Model):
    __tablename__ = 'visitors'
    visitor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Adoptions(db.Model):
    __tablename__ = 'adoptions'
    adoption_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.child_id', ondelete="CASCADE"), nullable=False)
    verification_status = db.Column(db.String(50), nullable=False, default="Pending")
    finalization_date = db.Column(db.Date, nullable=True)

class Events(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)

class ChildEventParticipation(db.Model):
    __tablename__ = 'child_event_participation'
    child_id = db.Column(db.Integer, db.ForeignKey('children.child_id', ondelete="CASCADE"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id', ondelete="CASCADE"), primary_key=True)
    participation_notes = db.Column(db.Text, nullable=True)
