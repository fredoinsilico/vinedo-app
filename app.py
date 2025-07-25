### 1. app.py

from flask import Flask, render_template, request, redirect, url_for
from model import db, Vino
from config import DevelopmentConfig, ProductionConfig
import os



app = Flask(__name__)
env = os.environ.get("FLASK_ENV", "development")

if env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    vinos = Vino.query.all()
    return render_template('index.html', vinos=vinos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nuevo_vino = Vino(
            nombre=request.form['nombre'],
            tipo=request.form['tipo'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock'])
        )
        db.session.add(nuevo_vino)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    vino = Vino.query.get_or_404(id)
    if request.method == 'POST':
        vino.nombre = request.form['nombre']
        vino.tipo = request.form['tipo']
        vino.precio = float(request.form['precio'])
        vino.stock = int(request.form['stock'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', vino=vino)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    vino = Vino.query.get_or_404(id)
    db.session.delete(vino)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
