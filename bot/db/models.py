from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String, nullable=False)  # Фамилия
    name = Column(String, nullable=False)     # Имя
    patronymic_name = Column(String)          # Отчество
    email = Column(String, nullable=False)    # Email
    employee_id = Column(String)              # Табельный номер
    employee_organisation = Column(String)    # Организация
    employee_position = Column(String)        # Должность
    telegram_id = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)     # 'unauthorized', 'admin', 'authorized'
    registration_status = Column(String, default="pending")  # 'pending', 'approved', 'rejected'
    reports = relationship("Report", back_populates="user")

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="draft")  # 'draft', 'ready', 'sent'
    user = relationship("User", back_populates="reports")
    tickets = relationship("Ticket", back_populates="report", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="report", cascade="all, delete-orphan")

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    ticket_number = Column(String, nullable=False)
    ticket_date = Column(String, nullable=False)
    ticket_price = Column(Float, nullable=False)
    report = relationship("Report", back_populates="tickets")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    order_number = Column(String, nullable=False)
    order_date = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Срок командировки (количество дней)
    report = relationship("Report", back_populates="orders")