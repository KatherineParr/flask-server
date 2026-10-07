from flask import Flask, render_template, url_for

# Inicializamos la aplicación
app = Flask(__name__)

productos = [
    {"nombre": "Teclado Mecanico", "precio": 49.99, "disponible": True},
    {"nombre": "Ratón Optico", "precio": 19.99, "disponible": False},
    {"nombre": "Monitor 4K", "precio": 299.99, "disponible": True},
]


# Ruta 1: Devuelve un HTML muy básico
@app.route("/")
def home():
    # return """
    #     <h1>¡Hola desde Flask en Docker!!!!</h1>
    #     <p>Este es tu primer servidor Python funcionando.</p>
    # """
    return render_template ("index.html")

@app.route("/saludo/<name>")
def saludo(name):
    return render_template("saludo.html", name=name)


# ruta /multiplicar/numero1/numero2 que recibe dos enteros y devuelve su multiplicación.
# Por ejemplo /multiplicar/3/4 debe devolver "Multiplicar 3 x 4 es 12".
@app.route("/multiplicar/<int:n1>/<int:n2>")
def multiplicar(n1, n2):
    return f"<h1>Multiplicar {n1} por {n2} es {n1 * n2}</h1>"

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", nombre="algo", lista_productos=productos)

    
@app.route("/catalogo/<int:idProducto>")
def producto(idProducto):
    return render_template("producto.html", idProducto=idProducto, producto=productos[idProducto])




if __name__ == "__main__":
    # host='0.0.0.0' es VITAL en Docker para que el servidor sea accesible desde fuera del contenedor
    # debug=True hará que el servidor se reinicie automáticamente si cambias este archivo
    app.run(host="0.0.0.0", port=5000, debug=True)
