from flask import Flask, render_template, request, url_for, redirect, flash
import json
import os

# Inicializo el microframework de 'flask'.
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesaria para usar flash

ARCHIVO_JSON = "reservas.json"

class Reserva:
    def __init__(self, nombre_huesped, noches, tarifa_noche):
        self.nombre_huesped = nombre_huesped
        self.noches = int(noches)
        self.tarifa_noche = float(tarifa_noche)
        self.total_pagar = self.noches * self.tarifa_noche

    # Método para convertir la instancia en un diccionario.
    def to_dict(self):
        return {
            "nombre_huesped": self.nombre_huesped,
            "noches": self.noches,
            "tarifa_noche": self.tarifa_noche,
            "total_pagar": self.total_pagar
        }

# Función para leer todos los registros que existan en el archivo JSON.
def leer_reservas():
    if not os.path.exists(ARCHIVO_JSON):
        return []
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        try:
            data = json.load(archivo)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def guardar_reservas(lista_reservas):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(lista_reservas, archivo, ensure_ascii=False, indent=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    reservas = leer_reservas()
    reserva_editar = None
    indice_editar = ""
    sort_order = request.args.get('sort_order', 'desc') # Por defecto, descendente

    if request.method == 'POST':
        nombre_huesped = request.form['nombre_huesped']
        noches = request.form['noches']
        tarifa_noche = request.form['tarifa_noche']
        indice = request.form.get('indice') # Usar .get para evitar errores si no existe

        # Validación del backend
        if not nombre_huesped or not noches or not tarifa_noche:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("index"))

        if any(char.isdigit() for char in nombre_huesped):
            flash("El nombre del huésped no debe contener números.", "error")
            return redirect(url_for("index"))

        try:
            noches_val = int(noches)
            tarifa_noche_val = float(tarifa_noche)
            if noches_val <= 0 or tarifa_noche_val <= 0:
                flash("El número de noches y la tarifa deben ser valores positivos.", "error")
                return redirect(url_for("index"))
        except (ValueError, TypeError):
            flash("Por favor, ingrese valores numéricos válidos para noches y tarifa.", "error")
            return redirect(url_for("index"))

        reserva = Reserva(nombre_huesped, noches_val, tarifa_noche_val)

        if indice:
            try:
                indx = int(indice)
                if 0 <= indx < len(reservas):
                    reservas[indx] = reserva.to_dict()
                    guardar_reservas(reservas)
                    flash("Reserva actualizada correctamente.", "success")
            except (ValueError, TypeError):
                flash("Índice de edición inválido.", "error")
        else:
            reservas.append(reserva.to_dict())
            guardar_reservas(reservas)
            flash("Reserva guardada correctamente.", "success")

        return redirect(url_for("index"))

    # Lógica de ordenamiento
    if sort_order == 'asc':
        reservas.sort(key=lambda x: x.get('total_pagar', 0))
    else:
        reservas.sort(key=lambda x: x.get('total_pagar', 0), reverse=True)

    # Lógica para editar
    if 'edit' in request.args:
        try:
            indx = int(request.args.get('edit'))
            if 0 <= indx < len(reservas):
                reserva_editar = reservas[indx]
                indice_editar = indx
        except (ValueError, TypeError):
            flash("Índice para editar no válido.", "error")

    return render_template('index2.html',
                           reservas=reservas,
                           reserva_editar=reserva_editar,
                           indice_editar=indice_editar,
                           sort_order=sort_order)

@app.route('/eliminar/<int:indice>', methods=["POST"])
def eliminar(indice):
    reservas = leer_reservas()
    if 0 <= indice < len(reservas):
        reservas.pop(indice)
        guardar_reservas(reservas)
        flash("Reserva eliminada correctamente.", "success")
    else:
        flash("No se pudo eliminar la reserva.", "error")

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
