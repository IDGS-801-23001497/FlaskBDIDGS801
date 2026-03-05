from . import maestros
from flask import render_template, request, redirect, url_for
from forms import UserForm3
import forms
from models import Maestros,db


@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de Maestros {nombre}"

@maestros.route('/maestros')
def listado_maestros():
    create_form=forms.UserForm3(request.form)
    maestro=Maestros.query.all()
    return render_template('maestros/listadoMaestros.html',form=create_form,maestro=maestro)

@maestros.route('/maestros/registrar', methods=['GET','POST'])
def registrar_maestro():
    create_form=forms.UserForm3(request.form)
    if request.method=='POST':
        mstr=Maestros(nombre=create_form.nombre.data,
			   apellidos=create_form.apellidos.data,
			   email=create_form.email.data,
			   especialidad=create_form.especialidad.data)
        db.session.add(mstr)
        db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))
    return render_template('maestros/registro_maestros.html', form=create_form)

@maestros.route('/maestros/detalles')
def detalles_maestro():
	create_form=forms.UserForm3(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		mstr1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		nombre=mstr1.nombre
		apellidos=mstr1.apellidos
		email=mstr1.email
		especialidad=mstr1.especialidad
	return render_template('maestros/detalles_maestros.html',matricula=matricula, nombre=nombre, apellidos=apellidos, email=email, especialidad=especialidad)

@maestros.route('/maestros/editar', methods=['GET','POST'])
def editar_maestro():
	create_form=forms.UserForm3(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		mstr1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=mstr1.nombre
		create_form.apellidos.data=mstr1.apellidos
		create_form.email.data=mstr1.email
		create_form.especialidad.data=mstr1.especialidad
	if request.method=='POST':
		matricula=create_form.matricula.data
		mstr1 = db.session.query(Maestros).filter (Maestros.matricula==matricula).first()
		mstr1.matricula=matricula
		mstr1.nombre=str.rstrip(create_form.nombre.data)
		mstr1.apellidos=create_form.apellidos.data
		mstr1.email=create_form.email.data
		mstr1.especialidad=create_form.especialidad.data
		db.session.add(mstr1)
		db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))
	return render_template('maestros/editar_maestros.html',form=create_form)


@maestros.route('/maestros/eliminar', methods=['GET','POST'])
def eliminar_maestro():
	create_form=forms.UserForm3(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		mstr1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		if mstr1:
			create_form.matricula.data=mstr1.matricula
			create_form.nombre.data=mstr1.nombre
			create_form.apellidos.data=mstr1.apellidos
			create_form.email.data=mstr1.email
			create_form.especialidad.data=mstr1.especialidad
			return render_template("maestros/eliminar_maestros.html", form=create_form)
	if request.method == 'POST':
		matricula = create_form.matricula.data
		alum = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		if alum:
			db.session.delete(alum)
			db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))




