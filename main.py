from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/proyecto'

db = SQLAlchemy(app)

class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    idCuenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreCuenta = db.Column(db.String(30))
    balanceInicial = db.Column(db.Integer)
    agregado = db.Column(db.Date)

    def __init__(self, nombreCuenta, balanceInicial, agregado):
        self.nombreCuenta = nombreCuenta
        self.balanceInicial = balanceInicial
        self.agregado = agregado

db.create_all()

@app.route('/')
def index():
    # Me devuelve todos los registros de la tabla mentores o SELECT*FROM mentores
    cuenta = Cuenta.query.all()
    return render_template("listar.html", cuen=cuenta)


@app.route('/agregar')
def agregar():
    return render_template('lista.html')
    #return render_template('agregar.html')


@app.route('/grabar', methods=['GET', 'POST'])
def grabar():
    if request.method == "POST":
        nom = request.form.get("nombreCuenta")
        bal = request.form.get("balanceInicial")
        agr = request.form.get("agregado")


        if nom and bal:
            # Insertarlo en la entidad
            cuenta = Cuenta(nom, bal, agr)
            db.session.add(cuenta)
            db.session.commit()
    return redirect(url_for("index"))


@app.route('/eliminar/<int:id>')
def eliminar(id):
    # select * from mentores where id=4
    cuenta = Cuenta.query.filter_by(idCuenta=id).first()
    db.session.delete(cuenta)
    db.session.commit()
    cuentas = Cuenta.query.all()
    return render_template("listar.html", cuen=cuentas)


@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    # Traer el mentor que voy a modificar
    cuenta = Cuenta.query.filter_by(idCuenta=id).first()
    if request.method == "POST":
        nom = request.form.get("nombreCuenta")
        bal = request.form.get("balanceInicial")
        agr = request.form.get("agregado")
        if nom and bal:
            #Actualizando los datos del mentor
            cuenta.nombreCuenta = nom
            cuenta.balanceInicial = bal
            cuenta.agregado = agr
            #Grabar fisicamente los cambios en la tabla
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", cue=cuenta)



app.run(debug=True, port=8000)