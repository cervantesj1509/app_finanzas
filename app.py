from flask import Flask, request, render_template, redirect, url_for
import json, os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "usuarios.json")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def cargar_usuarios():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f)

def ruta_movimientos(usuario):
    return os.path.join(DATA_FOLDER, f"movimientos_{usuario}.json")

def guardar_movimiento(usuario, movimiento):
    ruta = ruta_movimientos(usuario)
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            movimientos = json.load(f)
    else:
        movimientos = []
    movimientos.append(movimiento)
    with open(ruta, "w") as f:
        json.dump(movimientos, f, indent=2)

def cargar_movimientos(usuario):
    ruta = ruta_movimientos(usuario)
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    return []

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuarios = cargar_usuarios()
    usuario = request.form["usuario"]
    clave = request.form["clave"]
    if usuario in usuarios and usuarios[usuario] == clave:
        return redirect(url_for("dashboard", usuario=usuario))
    return "<p>Usuario o clave incorrectos</p><p><a href='/'>Volver</a></p>"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuarios = cargar_usuarios()
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario in usuarios:
            return "<p>El usuario ya existe</p><p><a href='/registro'>Intentar de nuevo</a></p>"
        usuarios[usuario] = clave
        guardar_usuarios(usuarios)
        return redirect(url_for("index"))
    return render_template("registro.html")

@app.route("/movimiento", methods=["GET", "POST"])
def movimiento():
    if request.method == "POST":
        usuario = request.form["usuario"]
        movimiento = {
            "tipo": request.form["tipo"],
            "categoria": request.form["categoria"],
            "monto": float(request.form["monto"]),
            "fecha": request.form["fecha"],
            "descripcion": request.form["descripcion"],
            "registro": datetime.now().isoformat()
        }
        guardar_movimiento(usuario, movimiento)
        return redirect(url_for("dashboard", usuario=usuario))
    return render_template("movimiento.html")

@app.route("/dashboard")
def dashboard():
    usuario = request.args.get("usuario")
    movimientos = cargar_movimientos(usuario)

    total_ingresos = sum(m["monto"] for m in movimientos if m["tipo"] == "ingreso")
    total_egresos = sum(m["monto"] for m in movimientos if m["tipo"] == "egreso")
    balance = total_ingresos - total_egresos

    # Calcular categorías para gráfico
    categorias = defaultdict(float)
    for m in movimientos:
        if m["tipo"] == "egreso":
            categorias[m["categoria"]] += m["monto"]

    return render_template("dashboard.html",
        usuario=usuario,
        movimientos=movimientos,
        total_ingresos=round(total_ingresos, 2),
        total_egresos=round(total_egresos, 2),
        balance=round(balance, 2),
        categorias=list(categorias.keys()),
        valores=list(categorias.values())
    )

if __name__ == "__main__":
    app.run(debug=True)
