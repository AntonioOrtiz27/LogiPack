from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy(app)

#Modelado de clases a partir de la base de datos con sus respectivas tablas.
class Sucursal(db.Model):
    __tablename__ = 'sucursal'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String, nullable=False)
    provincia = db.Column(db.String, nullable=False)
    localidad = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=False)
    repartidores = db.relationship('Repartidor', backref='sucursal', cascade="all, delete-orphan")
    paquetes = db.relationship('Paquete', backref='sucursal', cascade="all, delete-orphan")
    transportes = db.relationship('Transporte', backref='sucursal', cascade="all, delete-orphan")

class Repartidor(db.Model):
    __tablename__ = 'repartidor'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    dni = db.Column(db.String, nullable=False)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    paquetes = db.relationship('Paquete', backref='repartidor', cascade="all, delete-orphan")

class Paquete(db.Model):
    __tablename__ = 'paquete'
    id = db.Column(db.Integer, primary_key=True)
    numeroenvio = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    nomdestinatario = db.Column(db.String(80), unique=True, nullable=False)
    dirdestinatario = db.Column(db.String(80), nullable=True)
    entregado = db.Column(db.Boolean, nullable=False, default=False)
    observaciones = db.Column(db.String(120), nullable=True)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    idtransporte = db.Column(db.Integer, db.ForeignKey('transporte.id'), nullable=True)
    idrepartidor = db.Column(db.Integer, db.ForeignKey('repartidor.id'), nullable=True)

class Transporte(db.Model):
    __tablename__ = 'transporte'
    id = db.Column(db.Integer, primary_key=True)
    numerotransporte = db.Column(db.String, nullable=False)
    fechahorasalida = db.Column(db.DateTime, nullable=False)
    fechahorallegada = db.Column(db.DateTime, nullable=True)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    paquetes = db.relationship('Paquete', backref='transporte', cascade="all, delete-orphan")


