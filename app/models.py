from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

service_mechanic = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

service_inventory = db.Table(
    "services_inventory",
    Base.metadata,
    db.Column("inventory_id", db.ForeignKey("inventory.id")),
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"))
)

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates = "customer", cascade="all, delete") #this cascade will delete all records of their service tickets

class ServiceTicket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    serv_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    vin: Mapped[str] = mapped_column(db.String(100), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)

    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary=service_mechanic)
    service_ticket_items: Mapped[List["ServiceTicketItems"]] = db.relationship(back_populates="service")


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary=service_mechanic, back_populates="mechanics")

class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(db.String(150), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_ticket_items: Mapped[List["ServiceTicketItems"]] = db.relationship(back_populates = "part")

class ServiceTicketItems(Base):
    __tablename__ = "service_ticket_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"),nullable=False)
    inventory_id: Mapped[int] = mapped_column(db.ForeignKey("inventory.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    service: Mapped["ServiceTicket"] = db.relationship(back_populates="service_ticket_items")
    part: Mapped["Inventory"] = db.relationship(back_populates="service_ticket_items")


