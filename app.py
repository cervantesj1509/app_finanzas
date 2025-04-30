from flask import Flask, request, render_template, redirect, url_for
import json, os

app = Flask(__name__)

# Ruta del archivo de usuarios
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

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuarios = cargar_usuarios()
    usuario = request.form["usuario"]
    clave = request.form["clave"]
    if usuario in usuarios and usuarios[usuario] == clave:
        return f"<h3>Bienvenido, {usuario} 🎉</h3><p><a href='/'>Cerrar sesión</a></p>"
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

if __name__ == "__main__":
    app.run(debug=True)
