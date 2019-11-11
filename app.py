from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelos ---------------------------------------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200))
    echo = db.Column(db.Boolean)


# Rutas -----------------------------------------------------
# Ruta Princial
@app.route('/')
def home():
    listatareas = Task.query.order_by(desc(Task.id))
    #listatareas = Task.query.all()
    return render_template('index.html', tareas=listatareas)


# Ruta de Insersion de tarea
@app.route('/crear-tarea', methods=['POST'])
def create():
    objTarea = Task(contenido=request.form['task'], echo=False)
    db.session.add(objTarea)
    db.session.commit()
    return redirect(url_for('home'))


# Ruta edita la tarea
@app.route('/echo/<id>')
def done(id):
    varTask = Task.query.filter_by(id=int(id)).first()
    varTask.echo = not (varTask.echo)
    db.session.commit()
    return redirect(url_for('home'))


# Ruta de eliminacion de tarea
@app.route('/borrar-tarea/<id>')
def delete(id):
    varTask = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run()
    #app.run('0.0.0.0', 8080, debug=True)
