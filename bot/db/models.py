from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronimic_name = Column(String)
    email = Column(String)
    employee_id = Column(String)
    employee_organisation = Column(String)
    employee_position = Column(String)
    telegram_id = Column(String, unique=True)
    role = Column(String)
    registration_status = Column(String)
    reports = relationship("Report", back_populates="user")

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    user = relationship("User", back_populates="reports")
    tickets = relationship("Ticket", back_populates="report")
    orders = relationship("Order", back_populates="report")

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'))
    ticket_number = Column(String)
    ticket_date = Column(String)
    ticket_price = Column(Float)
    report = relationship("Report", back_populates="tickets")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'))
    order_number = Column(String)
    order_date = Column(String)
    duration = Column(Integer)
    report = relationship("Report", back_populates="orders")