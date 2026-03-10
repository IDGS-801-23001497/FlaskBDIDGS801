from . import inscripciones
from flask import render_template, request, redirect, url_for
from models import db, Alumnos, Curso
import forms

@inscripciones.route('/inscripciones')
def listado_inscripciones():
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()
    return render_template('inscripciones/listado_inscripciones.html', alumnos=alumnos, cursos=cursos)

@inscripciones.route('/inscripciones/registrar', methods=['GET', 'POST'])
def registrar_inscripcion():
    form = forms.InscripcionForm(request.form)
    
   
    alumnos_db = Alumnos.query.all()
    cursos_db = Curso.query.all()
    
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos_db]
    form.curso_id.choices = [(c.id, c.nombre) for c in cursos_db]

    
    if request.method == 'POST' and form.validate():
        
        
        alumno = db.session.query(Alumnos).filter(Alumnos.id == form.alumno_id.data).first()
        curso = db.session.query(Curso).filter(Curso.id == form.curso_id.data).first()
        
        
        if curso not in alumno.cursos:
            
            alumno.cursos.append(curso) 
            db.session.commit()
            
        return redirect(url_for('inscripciones.listado_inscripciones'))

    return render_template('inscripciones/registrar_inscripcion.html', form=form)