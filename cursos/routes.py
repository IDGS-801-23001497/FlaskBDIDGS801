from . import cursos
from flask import render_template, request, redirect, url_for
from forms import CursoForm
import forms
from models import Curso, db, Maestros

@cursos.route('/cursos')
def listado_cursos():
    create_form = forms.CursoForm(request.form)
    curso = Curso.query.all()
    return render_template('cursos/listadoCursos.html', form=create_form, curso=curso)

@cursos.route('/cursos/registrar', methods=['GET', 'POST'])
def registrar_curso():
    form = CursoForm(request.form)
    # Cargar los maestros para la lista desplegable
    maestros_db = Maestros.query.all()
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_db]
    
    # El profe te pidió CSRFProtect, asegúrate de que form.validate() lo pase
    if request.method == 'POST' and form.validate():
        nuevo_curso = Curso(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            maestro_id=form.maestro_id.data
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))
        
    return render_template('cursos/cursos.html', form=form)

@cursos.route('/cursos/detalles')
def detalles_curso():
    # Buscamos por el ID del curso, no por matrícula
    id_curso = request.args.get('id')
    curso = db.session.query(Curso).filter(Curso.id == id_curso).first()
    
    # Pasamos el objeto curso completo al template para que accedas a curso.nombre, curso.maestro.nombre, etc.
    return render_template('cursos/detalles.html', curso=curso)

@cursos.route('/cursos/editar', methods=['GET', 'POST'])
def editar_curso():
    form = forms.CursoForm(request.form)
    id_curso = request.args.get('id')
    curso_editar = db.session.query(Curso).filter(Curso.id == id_curso).first()
    
    # ¡IMPORTANTE! Al igual que en registrar, debes cargar los maestros para el SelectField
    maestros_db = Maestros.query.all()
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_db]

    if request.method == 'GET':
        # Precargar los datos en el formulario
        form.nombre.data = curso_editar.nombre
        form.descripcion.data = curso_editar.descripcion
        form.maestro_id.data = curso_editar.maestro_id
        
    if request.method == 'POST' and form.validate():
        # Actualizar los datos del curso
        curso_editar.nombre = form.nombre.data
        curso_editar.descripcion = form.descripcion.data
        curso_editar.maestro_id = form.maestro_id.data
        
        db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))
        
    return render_template('cursos/editar.html', form=form)

@cursos.route('/cursos/eliminar', methods=['GET', 'POST'])
def eliminar_curso():
    form = forms.CursoForm(request.form)
    id_curso = request.args.get('id')
    curso_eliminar = db.session.query(Curso).filter(Curso.id == id_curso).first()
    
    if request.method == 'GET':
        if curso_eliminar:
            # Precargamos los datos solo para mostrarlos en modo lectura antes de borrar
            form.nombre.data = curso_eliminar.nombre
            form.descripcion.data = curso_eliminar.descripcion
            return render_template("cursos/eliminar.html", form=form, curso=curso_eliminar)
            
    if request.method == 'POST':
        if curso_eliminar:
            db.session.delete(curso_eliminar)
            db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))