from __main__ import app
import hashlib
from .models import db, Sucursal, Repartidor, Paquete, Transporte
from flask import request, render_template, session, redirect, url_for, flash
from datetime import datetime

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/opcion')
def opcion():
    return render_template('opciones_disponibles.html')

@app.route('/sucursalactual', methods=['POST', 'GET'])
def sucursalactual():
    if request.method == 'POST':
        sucursal_id = request.form['sucursal_id']
        session['sucursal_id'] = sucursal_id
        return redirect(url_for('opcion'))

    Sucursales = Sucursal.query.order_by(Sucursal.numero).all()
    return render_template('sucursalactual.html', sucursales=Sucursales)



@app.route('/<int:sucursalid>/funcionalidades')
def funcionalidades(sucursalid):
    if sucursalid:
        return render_template('opciones_disponibles.html')



@app.route('/registrar_paquete', methods=['GET', 'POST'])
def registrar_paquete():
    if request.method == 'POST':
        try:
            peso = request.form['peso']
            nomdes = request.form['nomdes']
            dirdes = request.form['dirdes']
            idsucursal = request.form['idsucursal']
            numeroenvio = int(datetime.utcnow().timestamp())  # Generar número de envío único basado en la marca de tiempo

            nuevo_paquete = Paquete(
                numeroenvio=numeroenvio,
                peso=float(peso),
                nomdestinatario=nomdes,
                dirdestinatario=dirdes,
                entregado=False,
                observaciones='',
                idsucursal=idsucursal,
            )

            db.session.add(nuevo_paquete)
            db.session.commit()
            flash('Paquete registrado con éxito', 'success')
            return redirect(url_for('registrar_paquete'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el paquete: {str(e)}', 'error')
            return redirect(url_for('registrar_paquete'))
    sucursales = Sucursal.query.order_by(Sucursal.numero).all()
    return render_template('recepcion_pedidos.html', sucursales=sucursales)

@app.route('/transporte_paquetes', methods=['GET', 'POST'])
def transporte_paquetes():
    if request.method == 'POST':
        try:
            sucursal_destino_id = request.form['sucursal_destino']
            paquetes_ids = request.form.getlist('paquetes')
            
            # Crear transporte
            fecha_hora_salida = datetime.utcnow()
            nuevo_transporte = Transporte(
                numerotransporte=str(int(fecha_hora_salida.timestamp())),  # Número de transporte único basado en la marca de tiempo
                fechahorasalida=fecha_hora_salida,
                idsucursal=sucursal_destino_id
            )
            db.session.add(nuevo_transporte)
            db.session.commit()

            # Asignar paquetes al transporte
            for paquete_id in paquetes_ids:
                paquete = Paquete.query.get(paquete_id)
                paquete.idtransporte = nuevo_transporte.id
            db.session.commit()

            # Formatear la fecha y hora de salida
            fecha_hora_salida_str = fecha_hora_salida.strftime('%Y-%m-%d %H:%M:%S')
            flash(f'Paquetes asignados al transporte con éxito. Fecha y hora de salida: {fecha_hora_salida_str}', 'success')
            return redirect(url_for('transporte_paquetes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al asignar paquetes al transporte: {str(e)}', 'error')
            return redirect(url_for('transporte_paquetes'))

    sucursales = Sucursal.query.order_by(Sucursal.numero).all()
    # Filtrar paquetes que no están asignados a ningún transporte
    paquetes = Paquete.query.filter_by(entregado=False, idrepartidor=None, idtransporte=None).all()
    return render_template('transporte_paquetes.html', sucursales=sucursales, paquetes=paquetes)


    sucursales = Sucursal.query.order_by(Sucursal.numero).all()
    paquetes = Paquete.query.filter_by(entregado=False, idrepartidor=None).all()
    return render_template('transporte_paquetes.html', sucursales=sucursales, paquetes=paquetes)

@app.route('/llegada_transporte', methods=['GET', 'POST'])
def llegada_transporte():
    if request.method == 'POST':
        try:
            transporte_id = request.form['transporteid']
            transporte = Transporte.query.get(transporte_id)
            if transporte:
                transporte.fechahorallegada = datetime.utcnow()
                db.session.commit()
                flash('Llegada del transporte registrada con éxito', 'success')
            return redirect(url_for('llegada_transporte'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la llegada del transporte: {str(e)}', 'error')
            return redirect(url_for('llegada_transporte'))

    sucursal_actual_id = session.get('sucursal_id')  # Suponiendo que la sucursal actual se guarda en sesión
    transportes_pendientes = Transporte.query.filter_by(fechahorallegada=None, idsucursal=sucursal_actual_id).all()
    return render_template('llegada_transporte.html', transportes=transportes_pendientes)

#Ruta asignar_repartidor en rutas.py:
#GET: Obtiene los repartidores y paquetes disponibles.
#POST: Asigna los paquetes seleccionados al repartidor seleccionado y guarda los cambios en la base de datos.        
@app.route('/asignar_repartidor', methods=['GET', 'POST'])
def asignar_repartidor():
    if request.method == 'POST':
        try:
            repartidor_id = request.form['repartidor']
            paquetes_ids = request.form.getlist('paquetes')
            
            # Asignar paquetes al repartidor
            for paquete_id in paquetes_ids:
                paquete = Paquete.query.get(paquete_id)
                paquete.idrepartidor = repartidor_id
            db.session.commit()

            flash('Paquetes asignados al repartidor con éxito', 'success')
            return redirect(url_for('asignar_repartidor'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al asignar paquetes al repartidor: {str(e)}', 'error')
            return redirect(url_for('asignar_repartidor'))
    
    sucursal_actual_id = session.get('sucursal_id')
    repartidores = Repartidor.query.filter_by(idsucursal=sucursal_actual_id).all()
    paquetes = Paquete.query.filter_by(entregado=False, idrepartidor=None).all()
    return render_template('asignar_repartidor.html', repartidores=repartidores, paquetes=paquetes)
    #Template asignar_repartidor.html:
    #Muestra un formulario con un desplegable de repartidores 
    # y una lista de paquetes no entregados y sin repartidor asignado.
    #Permite seleccionar un repartidor y varios paquetes.
    #Envía los datos seleccionados al servidor para procesar la asignación.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numero = request.form.get('numero')
        dni = request.form.get('dni')
        
        # Pide de la base de datos y verifica el repartidor
        repartidor = Repartidor.query.filter_by(numero=numero, dni=dni).first()
        
        if repartidor:
            session['name'] = repartidor.nombre
            session['idrepartidor'] = repartidor.id
            return redirect(url_for('entregar_paquete'))
        else:
            flash('Número de Repartidor o DNI incorrecto. Por favor, inténtelo de nuevo.', 'error')
    
    return render_template('login.html')

@app.route('/entregar_paquete', methods=['GET', 'POST'])
def entregar_paquete():
    if request.method == 'POST':
        numeroenvio = request.form.get('numeroenvio')
        repartidor_id = session.get('idrepartidor')
        
        # Buscar el paquete que coincide con el número de envío y está asignado a este repartidor
        paquete = Paquete.query.filter_by(numeroenvio=numeroenvio, idrepartidor=repartidor_id, entregado=False).first()
        
        if paquete:
            return render_template('entregar_paquete.html', paquete=paquete)
        else:
            flash('Paquete no encontrado o no asignado a este repartidor', 'error')
            return redirect(url_for('entregar_paquete'))

    return render_template('entregar_paquete.html')

@app.route('/registrar_entrega', methods=['POST'])
def registrar_entrega():
    if request.method == 'POST':
        paquete_id = request.form.get('paquete_id')
        estado = request.form.get('estado')
        observaciones = request.form.get('observaciones')
        nombre_dni_recibido = request.form.get('nombre_dni_recibido', '')
        razon = request.form.get('razon', None)
        otra_razon_text = request.form.get('otra_razon_text', '')

        try:
            paquete = Paquete.query.get(paquete_id)

            if paquete:
                if estado == 'entregado':
                    # Marcar el paquete como entregado y registrar observaciones
                    paquete.entregado = True
                    paquete.observaciones = f"Entregado a: {nombre_dni_recibido} - {observaciones}"
                    paquete.fechaentrega = datetime.utcnow()
                elif estado == 'no_entregado':
                    # Marcar el paquete como no entregado y registrar observaciones y razón
                    paquete.entregado = False
                    if razon:
                        paquete.observaciones = f"No entregado - Razón: {razon}"
                        if razon == 'otro' and otra_razon_text:
                            paquete.observaciones += f" - {otra_razon_text}"
                    else:
                        paquete.observaciones = "No entregado"
                if estado == 'entregado':
                    db.session.commit()
                    flash('Entrega registrada con éxito', 'success')
                    return redirect(url_for('entregar_paquete'))
                elif estado == 'no_entregado':
                    db.session.commit()
                    flash('Registro de no entregado correcto', 'success')
                    return redirect(url_for('entregar_paquete'))    
            else:
                flash('Paquete no encontrado', 'error')
                return redirect(url_for('entregar_paquete'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la entrega: {str(e)}', 'error')
            return redirect(url_for('entregar_paquete'))
