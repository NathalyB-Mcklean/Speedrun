from flask import Flask, request, render_template, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
import openpyxl
import matplotlib.pyplot as plt
import io
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)

@app.route('/descargar_csv')
def descargar_csv():
    registros = Registro.query.all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos del Sensor"
    
    ws.append(["Fecha y Hora", "Temperatura", "Humedad"])
    
    for registro in registros:
        ws.append([datetime.now(), registro.temperatura, registro.humedad])
    
    obj = io.BytesIO()
    wb.save(obj)
    obj.seek(0)
    
    response = make_response(obj.getvalue())
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=datos_sensor.xlsx"
    
    return response

@app.route('/descargar_grafica')
def descargar_grafica():
    registros = Registro.query.all()
    temperaturas = [r.temperatura for r in registros]
    humedades = [r.humedad for r in registros]

    plt.figure(figsize=(10,5))
    plt.plot(temperaturas, label='Temperatura (°C)', color='blue')
    plt.plot(humedades, label='Humedad (%)', color='green')
    plt.title('Datos del Sensor')
    plt.xlabel('Tiempo')
    plt.legend()
    
    obj = io.BytesIO()
    plt.savefig(obj, format='png')
    obj.seek(0)

    response = make_response(obj.getvalue())
    response.headers["Content-Type"] = "image/png"
    response.headers["Content-Disposition"] = "attachment; filename=grafica_datos_sensor.png"
    
    return response

@app.route('/datos', methods=['GET'])
def datos():
    registros = Registro.query.all()
    return render_template('datos.html', registros=registros)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
