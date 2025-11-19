
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#La forma de definir una ruta en una aplicación Flask es a través del decorador @app.route, que registra la
#función decorada como una ruta. 
#Para manejar el path o ruta raíz de la aplicación, el método route recibe como parámetro la ‘/’,
app.config.from_pyfile("config.py")

from src.models import db
import src.rutas
if __name__ == '__main__': #El parámetro del constructor, __name__ es el nombre del módulo Python actual.
    app.run(debug=True) #el método .run() que inicia el servidor web de desarrollo
    db.create_all()

