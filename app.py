from flask import Flask, request, render_template, redirect, url_for
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "usuarios.json")

# Crear carpeta de datos si no existe
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Crear archivo de usuarios si no existe
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

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuarios = cargar_usuarios()
    usuario = request.form["usuario"]
    clave = request.form["clave"]
    if usuario in usuarios and usuarios[usuario] == clave:
        return redirect(url_for("movimiento"))
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
        return f"<p>✅ Movimiento guardado correctamente para {usuario}</p><p><a href='/movimiento'>Registrar otro</a></p><p><a href='/'>Volver al inicio</a></p>"
    return render_template("movimiento.html")

if __name__ == "__main__":
    app.run(debug=True)
