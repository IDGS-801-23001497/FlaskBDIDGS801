
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from maestros.routes import maestros
from alumnos import alumnos as alumnos
import forms
from flask_migrate import Migrate, migrate
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
csrf=CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
@app.route("/index")
def index():
	create_form=forms.UserForm2(request.form)
	alumno=Alumnos.query.all()
	return render_template("index.html",form=create_form,alumno=alumno)
	
@app.errorhandler(404)
def  page_not_found(e):
	return render_template('404.html'),404



if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(debug=True)
	
