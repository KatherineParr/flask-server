from data.producto import productos
from flask import Flask, render_template, request, url_for, redirect, abort
from form import LoginForm

#NOTA PARA SELF, SI CARGA UNA NUEVA PAGINA O COSA CON F12, ES LADO SERVIDOR
#SI NO CARGA NADA NUEVO NI CAMBIA DE PAGINA ES LADO DE CLIENTE

#lo de arriba es cargando librerias, y, en el arriba, de producto, se especifica 
#la ruta del archivo, o sea, de donde se saca la info, y que info se saca

# Inicializamos la aplicación
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave"



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
    #comprobar si esta debtro de la lista (pero como no definimos una id hay que hacerlo con un if)
    # if idProducto not in productos:
    
    # if 0 <= idProducto < len(productos)
    #     abort(404) #abortar si el id no esta en productos y redirige a 404
    return render_template("producto.html", idProducto=idProducto, producto=productos[idProducto])

@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("contacto.html")

@app.route("/contacto", methods=["POST"])
def contacto_post():
    nombre = request.form.get("nombre")
    mensaje = request.form["mensaje"]
    return render_template("contacto-datos.html", nombre=nombre, mensaje=mensaje)

@app.route("/filtrar")
def filtrar():
    return render_template("filtrar.html")

@app.route("/filtrar-datos", methods=["GET"])
def filtrar_datos():
    precio_min = request.args.get("precio_min", type=float)
    print(f"Precio minimo: {precio_min}")
    precio_max = request.args.get("precio_max", type=float)
    print(f"Precio maximo: {precio_max}")
    productos_filtrados = [
        producto for producto in productos 
        if producto["precio"] >= precio_min and producto["precio"] <= precio_max
    ]
    print(f"Productos filtrados: {productos_filtrados}")
    #return render_template("filtrar-datos.html")
    return render_template("catalogo.html", nombre="Filtrado", lista_productos=productos_filtrados)


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    #validate compruenba si la peticion post y si se validan todos los campos
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        print(f"El usuario es {email} con la contraseña {password}")

        return redirect(url_for('gracias'))
    return render_template('login.html', form=form)

@app.route("/gracias")
def gracias():
    return render_template("gracias.html")


# para perzonalizar los errores para que no salgan 404 y otros
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404




if __name__ == "__main__":
    # host='0.0.0.0' es VITAL en Docker para que el servidor sea accesible desde fuera del contenedor
    # debug=True hará que el servidor se reinicie automáticamente si cambias este archivo
    app.run(host="0.0.0.0", port=5000, debug=True)

