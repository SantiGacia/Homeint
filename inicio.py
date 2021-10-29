from flask import Flask, g, render_template, request, redirect, url_for, session, json, jsonify
import pymysql
from flask_mysqldb import MySQL,MySQLdb
#import os
#from werkzeug.utils import secure_filename

app = Flask(__name__)
# sesion
app.secret_key = 'mysecretkey'
#carpeta de subida
#app.config['UPLOAD_FOLDER'] = './pdfs'

#definir la base de datos para flask_mysqldb
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'r_humanos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# Clase de usuarios
class user:
    def __init__(self,id,username,password,id_funcion,funcion):
        self.id = id
        self.username = username
        self.password = password
        self.id_funcion = id_funcion
        self.funcion = funcion
    def __repr__(self):
        return '<User:{self.username}>'

#Objeto de la clase usuarios
users=[]

@app.route('/login')
def login():
    return render_template("login.html")

#@app.before_request
#def before_request():
#    if 'user_id' in session:
#        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
#        cursor = conn.cursor()
#        cursor.execute('select a.idUsuario, a.Usuario, a.Password, a.Nombre, a.Perfil, b.idPerfil, b.Descripcion from usuario a, perfil_admo b '
#        'where a.idUsuario=%s and b.idPerfil=a.Perfil', (session['user_id']))
#        dato = cursor.fetchone()
#        users.clear()
#        users.append(user(id=dato[0], username=dato[1], password=dato[2], id_funcion=dato[4], funcion=dato[5]))
#        g.user=users[0]


@app.route('/inicio', methods=['POST'])
def inicio():
    session.pop('user_id', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ##
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select idUsuario, Usuario, Password, Nombre, Perfil from usuario where Usuario = %s and Password = %s', (username, password))
        dato = cursor.fetchone()
        if dato==None:
            error = "Usuario y/o Contraseña Incorrectos."
            return render_template("error_usuario.html", des_error=error)
        else:
            session['user_id'] = dato[0]
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id')
    return render_template("login.html")

# Menu Principal
@app.route('/')
def home():
    return render_template("home.html")

##Habilidad
@app.route('/habilidad')
def habilidad():
    return render_template("habilidad.html")

@app.route('/habilidad_agr', methods=['POST'])
def habilidad_agr():
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from habilidad where Descripcion = %s', (aux_descripcion))
        habilidades = cursor.fetchone()
        if (habilidades[0] != 0):
            error = "La Habilidad ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_habilidad")
        else:
            cursor.execute('insert into habilidad (Descripcion) values (%s)', (aux_descripcion))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_habilidad'))

@app.route('/agr_datos_habilidad')
def agr_datos_habilidad():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idHabilidad, Descripcion from habilidad order by Descripcion')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_habilidad.html", habs = datos )

@app.route('/bo_habilidad/<string:id>')
def bo_habilidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from puesto_has_habilidad where idHabilidad = {0}'.format(id))
    solicitudes = cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "La habilidad tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_habilidad")
    else:
        cursor.execute('delete from habilidad where idHabilidad = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_habilidad'))

@app.route('/ed_habilidad/<string:id>')
def ed_habilidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idHabilidad, Descripcion from habilidad where idHabilidad = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_habilidad.html", habs = dato[0])

@app.route('/modifica_habilidad/<string:id>', methods=['POST'])
def modifica_habilidad(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from habilidad where Descripcion = %s',(descrip))
        habilidades = cursor.fetchone()
        if (habilidades[0] != 0):
            error = "La Habilidad ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_habilidad")
        else:
            cursor.execute('update habilidad set  Descripcion=%s where idHabilidad=%s', (descrip,id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_habilidad'))
    return redirect(url_for('agr_datos_habilidad'))


# Carrera
@app.route('/carrera')
def carrera():
    return render_template("carrera.html")

@app.route('/carrera_agr', methods=['POST'])
def carrera_agr():
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from carrera where Descripcion = %s', (aux_descripcion))
        carreras = cursor.fetchone()
        if (carreras[0] != 0):
            error = "La Carrera ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_carrera")
        else:
            cursor.execute('insert into carrera (Descripcion) values (%s)', (aux_descripcion))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_carrera'))


@app.route('/modifica_carrera/<string:id>', methods=['POST'])
def modifica_carrera(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from carrera where Descripcion = %s',(descrip))
        carreras = cursor.fetchone()
        if (carreras[0] != 0):
            error = "La Carrera ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_carrera")
        else:
            cursor.execute('update carrera set  Descripcion=%s where idCarrera=%s', (descrip,id))
            conn.commit()
            conn.close()
    return redirect(url_for('agr_datos_carrera'))

@app.route('/ed_carrera/<string:id>')
def ed_carrera(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, Descripcion from carrera where idCarrera = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_carrera.html", nivel = dato[0])


@app.route('/agr_datos_carrera')
def agr_datos_carrera():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_carrera.html", niveles = datos )

@app.route('/bo_carrera/<string:id>')
def bo_carrera(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from solicitud where idCarrera = {0}'.format(id))
    solicitudes = cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "La carrera tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_carrera")
    else:
        cursor.execute('delete from carrera where idCarrera = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_carrera'))




# Medio Publicidad
@app.route('/publicidad')
def publicidad():
    return render_template("publicidad.html")

@app.route('/publicidad_agr', methods=['POST'])
def publicidad_agr():
    if request.method == 'POST':
        aux_descripcion = request.form['nombre_e']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from mediopublicidad where Descripcion = %s', (aux_descripcion))
        publicidades = cursor.fetchone()
        if (publicidades[0] != 0):
            error = "El Medio de Publicidad ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_publicidad")
        else:
            cursor.execute('insert into mediopublicidad (Descripcion) values (%s)',(aux_descripcion))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_publicidad'))

@app.route('/bo_publicidad/<string:id>')
def bo_publicidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from anuncio where idMedioPublicidad = {0}'.format(id))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El medio tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_publicidad")
    else:
        cursor.execute('delete from mediopublicidad where idMedioPublicidad = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_publicidad'))

@app.route('/agr_datos_publicidad')
def agr_datos_publicidad():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by idMedioPublicidad')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_publicidad.html", niveles = datos )

@app.route('/ed_publicidad/<string:id>')
def ed_publicidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad where idMedioPublicidad = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_publicidad.html", nivel=dato[0])

@app.route('/modifica_publicidad/<string:id>', methods=['POST'])
def modifica_publicidad(id):
    if request.method == 'POST':
        aux_descripcion = request.form['nombre_e']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from mediopublicidad where Descripcion = %s', (aux_descripcion))
        publicidades = cursor.fetchone()
        if (publicidades[0] != 0):
            error = "El Medio de Publicidad ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_publicidad")
        else:
            cursor.execute('update mediopublicidad set Descripcion=%s where idMedioPublicidad=%s',(aux_descripcion, id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_publicidad'))


# Nivel Academico
@app.route('/nivel_academico')
def nivel_academico():
    return render_template("nivel_academico.html")

@app.route('/nivel_agr', methods=['POST'])
def nivel_agr():
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from nivelacademico where Descripcion = %s',(aux_descripcion))
        niveles = cursor.fetchone()
        if (niveles[0] != 0):
            error = "El Nivel Academico ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_nivel_academico")
        else:
            cursor.execute('insert into nivelacademico (Descripcion) values (%s)', (aux_descripcion))
            conn.commit()
            conn.close()
    return redirect(url_for('agr_datos_nivel_academico'))

@app.route('/bo_nivel/<string:id>')
def bo_nivel(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from candidato_has_nivelacademico where idNivelAcademico = {0}'.format(id))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El nivel tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_nivel_academico")
    else:
        cursor.execute('delete from nivelacademico where idNivelAcademico = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_nivel_academico'))

@app.route('/agr_datos_nivel_academico')
def agr_datos_nivel_academico():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, descripcion from nivelacademico order by descripcion')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_nivel_academico.html", niveles = datos )

@app.route('/ed_nivel/<string:id>')
def ed_nivel(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico where idNivelAcademico = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_nivel_academico.html", nivel = dato[0])

@app.route('/modifica_nivel/<string:id>', methods=['POST'])
def modifica_nivel(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from nivelacademico where Descripcion = %s',(descrip))
        niveles = cursor.fetchone()
        if (niveles[0] != 0):
            error = "El Nivel Academico ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_nivel_academico")
        else:
            cursor.execute('update nivelacademico set  descripcion=%s where idNivelAcademico=%s', (descrip, id))
            conn.commit()
            conn.close()
    return redirect(url_for('agr_datos_nivel_academico'))


# Datos de la empresa
@app.route('/datos_empresa')
def datos_empresa():
    return render_template("datos_empresa.html")


@app.route('/datos_empresa_agr', methods=['POST'])
def datos_empresa_agr():
    if request.method == 'POST':
        aux_nombre = request.form['nom_empresa']
        aux_descripcion = request.form['descripcion']
        aux_estructura = request.form['estructura_juridica']
        aux_razon = request.form['razon_social']
        aux_correo = request.form['correo']
        aux_domicilio = request.form['domicilio']
        aux_telefono = request.form['tel']
        aux_encargado = request.form['encargado']
        aux_CIF = request.form['CIF']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('insert into datos_de_empresa '
                       '(Nombre_de_empresa, Descripcion, Telefono, Domicilio, E_Mail, RazonSocial, Estructura_Juridica, Encargado, CIF_Empresa) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (aux_nombre, aux_descripcion, aux_estructura, aux_razon, aux_correo,
                        aux_domicilio, aux_telefono, aux_encargado, aux_CIF))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_empresa'))


@app.route('/agr_datos_empresa')
def agr_datos_empresa():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select Nombre_de_empresa, Descripcion, Telefono, Domicilio, E_Mail, RazonSocial, '
                   'Estructura_Juridica, Encargado, CIF_Empresa from datos_de_empresa order by Nombre_de_empresa')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_datos_empresa.html", niveles=datos)


@app.route('/modificar_datos_empresa/<string:id>', methods=['POST'])
def modificar_datos_empresa(id):
    if request.method == 'POST':
        aux_nombre = request.form['nom_empresa']
        aux_descripcion = request.form['descripcion']
        aux_estructura = request.form['estructura_juridica']
        aux_razon = request.form['razon_social']
        aux_correo = request.form['correo']

        aux_acta = request.form['acta_consti']

        aux_domicilio = request.form['domicilio']
        aux_telefono = request.form['tel']
        aux_encargado = request.form['encargado']

        aux_noescpub = request.form['no_esct_publica']
        aux_libroescpub = request.form['libro_esct_publica']
        aux_fechaescpub = request.form['fecha_esct_publica']
        aux_feescpub = request.form['fe_esct_publica']
        aux_npescpub = request.form['np_esct_publica']
        aux_ciuescpub = request.form['ciu_escpub']

        aux_CIF = request.form['CIF']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute(
            'update datos_de_empresa set Nombre_de_empresa=%s,Descripcion=%s, Telefono=%s, Domicilio=%s, E_Mail=%s, Acta_constitutiva=%s,RazonSocial=%s, Estructura_Juridica=%s, Encargado=%s, CIF_Empresa=%s,No_Escriturapub=%s, Libro_Escriturapub=%s, Fecha_Escriturapub=%s, Fe_Escriturapub=%s, NP_Escriturapub=%s, Ciu_Escriturapub=%s'
            'where Nombre_de_empresa=%s', (
            aux_nombre, aux_descripcion, aux_telefono, aux_domicilio, aux_correo, aux_acta, aux_razon, aux_estructura,
            aux_encargado, aux_CIF, aux_noescpub, aux_libroescpub, aux_fechaescpub, aux_feescpub, aux_npescpub,
            aux_ciuescpub, id))
        conn.commit()
        conn.close()
    return redirect(url_for('agr_datos_empresa'))


@app.route('/bo_datos_empresa/<string:id>')
def bo_datos_empresa(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from datos_de_empresa where Nombre_de_empresa = {0}'.format(id))
    conn.commit()
    conn.close()
    return redirect(url_for('agr_datos_empresa'))


@app.route('/ed_datos_empresa/<string:id>')
def ed_datos_empresa(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select Nombre_de_empresa, Descripcion, Telefono, Domicilio, E_Mail, RazonSocial, '
                   'Estructura_Juridica, Encargado, CIF_Empresa,`Acta_constitutiva`,`No_Escriturapub`,`Libro_Escriturapub`,`Fecha_Escriturapub`,`Fe_Escriturapub`,`NP_Escriturapub`,`Ciu_Escriturapub`'
                   'from datos_de_empresa where Nombre_de_empresa = %s', (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template('edi_datos_empresa.html', nivel=dato[0])


# Puesto

#------------------------------- puesto -------------------------------------------------
@app.route('/puesto')
def puesto():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion from puesto '
                   'order by Descripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_puesto.html", puestos=datos)

@app.route('/agrega_puesto', methods=['POST'])
def agrega_puesto():
    if request.method == 'POST':
        aux_des = request.form['descripcion']
        aux_sal = request.form['salario']
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from puesto where Descripcion = %s',(aux_des))
        puestos = cursor.fetchone()
        if (puestos[0] != 0):
            error = "El Puesto ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/puesto")
        else:
            cursor.execute('insert into puesto (Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion) '
                           'values (%s,%s,%s,%s,%s)',(aux_des, aux_sal,aux_ben, aux_bon, aux_aut))
            conn.commit()
            cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
                           'from puesto where idPuesto=(select max(idPuesto) from puesto)')
            datos = cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto,c.idHabilidad, c.Experiencia '
                           ' from puesto a, habilidad b,puesto_has_habilidad c '
                           ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=(select max(idPuesto) from puesto)')
            datos1=cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma,c.Nivel from puesto a, idioma b,puesto_has_idioma c '
                           'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma '
                           'and c.idPuesto=(select max(idPuesto) from puesto)')
            datos2=cursor.fetchall()
            cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()
            cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()
            conn.close()
            return render_template("edi_puesto.html", puestos = datos, pue_habs=datos1,pue_idis=datos2, habs=datos3, idiomas=datos4 )

@app.route('/nvo_puesto')
def nvo_puesto():
    return render_template("puesto.html")

@app.route('/modifica_puesto/<string:id>', methods=['POST'])
def modifica_puesto(id):
    if request.method == 'POST':
        aux_des =request.form['descripcion']
        aux_sal = request.form['salario']
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update puesto set Descripcion=%s, SalarioMensual=%s, Beneficios=%s, Bonos=%s, Aprobacion=%s '
                       'where idpuesto=%s', (aux_des, aux_sal,aux_ben, aux_bon,aux_aut,id))
        conn.commit()
        conn.close()
        return redirect(url_for('puesto'))


@app.route('/ed_puesto/<string:id>')
def ed_puesto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
    'from puesto where idPuesto=%s', (id))
    datos=cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
    ' from puesto a, habilidad b,puesto_has_habilidad c '
    ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (id))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
    'from puesto a, idioma b,puesto_has_idioma c '
    'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (id))
    datos2=cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos = datos, pue_habs=datos1,
    pue_idis=datos2, habs=datos3, idiomas=datos4 )

@app.route('/bo_puesto/<string:id>')
def bo_puesto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from solicitud where idPuesto = {0}'.format(id))
    solicitudes = cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El puesto tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/puesto")
    else:
        cursor.execute('delete from puesto_has_idioma where idPuesto = {0}'.format(id))
        conn.commit()
        cursor.execute('delete from puesto_has_habilidad where idPuesto = {0}'.format(id))
        conn.commit()
        cursor.execute('delete from puesto where idPuesto = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('puesto'))

@app.route('/agrega_hab_pto/<string:id>', methods=['POST'])
def agrega_hab_pto(id):
    if request.method == 'POST':
        aux_pto=request.form['pto']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from puesto_has_habilidad where idHabilidad = %s and idPuesto=%s',(aux_hab,aux_pto))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "Esta habilidad ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/puesto")
        else:
            cursor.execute('insert into puesto_has_habilidad (idPuesto, idHabilidad, Experiencia) '
                           'values (%s,%s,%s)',(aux_pto,aux_hab,aux_exp))
            conn.commit()
            cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
                           'from puesto where idPuesto=%s', (aux_pto))
            datos = cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto,c.idHabilidad, c.Experiencia '
                           ' from puesto a, habilidad b,puesto_has_habilidad c '
                           ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (aux_pto))
            datos1 = cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                           'from puesto a, idioma b,puesto_has_idioma c '
                           'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (aux_pto))
            datos2 = cursor.fetchall()
            cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()
            cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()
            conn.close()
            return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)


@app.route('/agrega_idio_pto/<string:id>', methods=['POST'])
def agrega_idio_pto(id):
    if request.method == 'POST':
        aux_pto = request.form['ptoi']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from puesto_has_idioma where idIdioma = %s and idPuesto=%s',(aux_idi,aux_pto))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "Este idioma ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/puesto")
        else:
            cursor.execute('insert into puesto_has_idioma (idPuesto, idIdioma, Nivel) '
                           'values (%s,%s,%s)',(aux_pto,aux_idi,aux_niv))
            conn.commit()
            cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
                           'from puesto where idPuesto=%s', (aux_pto))
            datos = cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                           ' from puesto a, habilidad b,puesto_has_habilidad c '
                           ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (aux_pto))
            datos1 = cursor.fetchall()
            cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                           'from puesto a, idioma b,puesto_has_idioma c '
                           'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (aux_pto))
            datos2 = cursor.fetchall()
            cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()
            cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()
            conn.close()
            return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)

@app.route('/bo_hab_pto/<string:idP>/<string:idH>')
def bo_hab_pto(idP,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s and idHabilidad=%s',(idP,idH))
    conn.commit()
    cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
    'from puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
    ' from puesto a, habilidad b,puesto_has_habilidad c '
    ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (idP))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
    'from puesto a, idioma b,puesto_has_idioma c '
    'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1,pue_idis=datos2, habs=datos3, idiomas=datos4)

@app.route('/bo_idi_pto/<string:idP>/<string:idI>')
def bo_idi_pto(idP,idI):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_idioma where idPuesto =%s and idIdioma=%s',(idP,idI))
    conn.commit()
    cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion '
                   'from puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                   'from puesto a, habilidad b,puesto_has_habilidad c '
                   'where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (idP))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                   'from puesto a, idioma b,puesto_has_idioma c '
                   'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)

# Idioma
@app.route('/idioma')
def idioma():
    return render_template("idioma.html")

@app.route('/idioma_agr', methods=['POST'])
def idioma_agr():
    if request.method == 'POST':
        aux_idioma = request.form['fidioma']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from idioma where Lenguaje = %s', (aux_idioma))
        idiomas = cursor.fetchone()
        if (idiomas[0] != 0):
            error = "El Idioma ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_idioma")
        else:
            cursor.execute('insert into idioma (Lenguaje) values (%s)',(aux_idioma))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_idioma'))

@app.route('/modifica_idioma/<string:id>', methods=['POST'])
def modifica_idioma(id):
    if request.method == 'POST':
        aux_idioma = request.form['fidioma']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from idioma where Lenguaje = %s', (aux_idioma))
        idiomas = cursor.fetchone()
        if (idiomas[0] != 0):
            error = "El Idioma ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_idioma")
        else:
            cursor.execute('update idioma set  Lenguaje=%s where idIdioma=%s',(aux_idioma,id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_idioma'))

@app.route('/bo_idioma/<string:id>')
def bo_idioma(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from puesto_has_idioma where idIdioma = {0}'.format(id))
    solicitudes = cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El idioma tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_idioma")
    else:
        cursor.execute('delete from idioma where idIdioma = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_idioma'))


@app.route("/agr_datos_idioma")
def agr_datos_idioma():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
    'select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_idioma.html", niveles=datos)

@app.route('/ed_idioma/<string:id>')
def ed_idioma(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idIdioma,Lenguaje from idioma where idIdioma = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_idioma.html", nivel = dato[0])



#Area
@app.route('/area')
def area():
    return render_template("area.html")

@app.route('/area_agr', methods=['POST'])
def area_agr():
    if request.method == 'POST':
        aux_area = request.form['nom_area']
        aux_descripcion = request.form['desc']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from area where AreaNombre = %s', (aux_area))
        areas = cursor.fetchone()
        if (areas[0] != 0):
            error = "El Area ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_area")
        else:
            cursor.execute('insert into area (AreaNombre, AreaDescripcion) values (%s, %s)',(aux_area, aux_descripcion))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_area'))

@app.route("/agr_datos_area")
def agr_datos_area():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre, AreaDescripcion from area ')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_area.html", areas = datos )

@app.route('/ed_area/<string:id>')
def ed_area(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre, AreaDescripcion from area where idArea = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_area.html", tarea = dato[0])

@app.route('/modifica_area/<string:id>', methods=['POST'])
def modifica_area(id):
    if request.method == 'POST':
        aux_area = request.form['nom_area']
        aux_descripcion = request.form['desc']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from area where AreaNombre = %s', (aux_area))
        areasnom = cursor.fetchone()
        cursor.execute('select count(*) from area where AreaDescripcion = %s', (aux_descripcion))
        areasdesc = cursor.fetchone()
        if (areasnom[0] != 0):
            if (areasdesc[0] != 0):
                error = "El Area ya se encuentra agregado."
                return render_template("error.html", des_error=error, paginaant="/agr_datos_area")
            else:
                cursor.execute('update area set AreaNombre=%s, AreaDescripcion=%s where idArea=%s',(aux_area,aux_descripcion, id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_area'))
        else:
            cursor.execute('update area set AreaNombre=%s, AreaDescripcion=%s where idArea=%s',(aux_area,aux_descripcion, id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_area'))

@app.route('/bo_area/<string:id>')
def bo_area(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from solicitud where idArea = {0}'.format(id))
    solicitudes = cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El area tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_area")
    else:
        cursor.execute('delete from area where idArea = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_area'))



#Jornada
@app.route('/jornada')
def jornada():
    return render_template("jornada.html")

@app.route('/jor_agr', methods=['POST'])
def jor_agr():
    if request.method == 'POST':
        aux_area = request.form['nom_area']
        aux_descripcion = request.form['desc']
        aux_fino= request.form['find']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from jornada where jorNombre = %s', (aux_area))
        areas = cursor.fetchone()
        if (areas[0] != 0):
            error = "La jornada ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_jor")
        else:
            cursor.execute('insert into jornada (jorNombre, Descripcion) values (%s, %s)',(aux_area, aux_descripcion))
            conn.commit()
            cursor.execute('INSERT INTO jordesc (name, idJornada) SELECT Descripcion, IdJornada FROM jornada where val=%s',(aux_fino))             
            conn.commit()
            cursor.execute('update jornada set val = %s',(1))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_jor'))

@app.route("/agr_datos_jor")
def agr_datos_jor():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idJornada, jorNombre, Descripcion from jornada ')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_jor.html", areas = datos )

@app.route('/ed_jor/<string:id>')
def ed_jor(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idJornada, jorNombre, Descripcion from jornada where idJornada = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_jor.html", tarea = dato[0])

@app.route('/modifica_jor/<string:id>', methods=['POST'])
def modifica_jor(id):
    if request.method == 'POST':
        aux_area = request.form['nom_area']
        aux_descripcion = request.form['desc']
        aux_val=request.form['val']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from jornada where jorNombre = %s', (aux_area))
        areasnom = cursor.fetchone()
        cursor.execute('select count(*) from jornada where Descripcion = %s', (aux_descripcion))
        areasdesc = cursor.fetchone()
        if (areasnom[0] != 0):
            if (areasdesc[0] != 0):
                error = "La jornada ya se encuentra agregada."
                return render_template("error.html", des_error=error, paginaant="/agr_datos_jor")
            else:
                cursor.execute('update jornada set jorNombre=%s, Descripcion=%s, val=%s where idJornada=%s',(aux_area,aux_descripcion,aux_val, id))
                conn.commit()
                cursor.execute('update  jordesc set name=%s where idJornada=%s',(aux_descripcion,id))             
                conn.commit()
                cursor.execute('update jornada set val = %s',(1))
                conn.close()
                return redirect(url_for('agr_datos_jor'))
        else:
            cursor.execute('update jornada set jorNombre=%s, Descripcion=%s, val=%s where idJornada=%s',(aux_area,aux_descripcion,aux_val, id))
            conn.commit()
            cursor.execute('update  jordesc set name=%s where idJornada=%s',(aux_descripcion,id))             
            conn.commit()
            cursor.execute('update jornada set val = %s',(1))
            conn.close()
            return redirect(url_for('agr_datos_jor'))


@app.route('/bo_jor/<string:id>')
def bo_jor(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from jornada where idJornada = {0}'.format(id))
    conn.commit()
    conn.close()
    return redirect(url_for('agr_datos_jor'))

# Contacto
@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/contacto_agr', methods=['POST'])
def contacto_agr():
    if request.method == 'POST':
        aux_nombre = request.form['nombre']
        aux_domicilio = request.form['dom']
        aux_razon = request.form['razon']
        aux_tel = request.form['tel']
        aux_email = request.form['email']
        aux_link = request.form['link']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from contacto where Nombre = %s', (aux_nombre))
        contactos = cursor.fetchone()
        if (contactos[0] != 0):
            error = "El Contacto ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_contacto")
        else:
            cursor.execute('insert into contacto (Nombre,Domicilio,Razon_Social,Telefono,Email,Link) values (%s,%s,%s,%s,%s,%s)',
                           (aux_nombre, aux_domicilio, aux_razon, aux_tel,aux_email,aux_link))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_contacto'))

@app.route("/agr_datos_contacto")
def agr_datos_contacto():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idcontacto,Nombre,Domicilio,Razon_Social,Telefono from contacto ')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_contacto.html", contactos = datos )

@app.route('/ed_contacto/<string:id>')
def ed_contacto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idcontacto,Nombre,Domicilio,Razon_Social,Telefono,Email,Link from contacto where idcontacto = %s', (id))
    dato=cursor.fetchall()
    conn.close()
    return render_template("edi_Contacto.html", tcontacto = dato[0])

@app.route('/modifica_contacto/<string:id>', methods=['POST'])
def modifica_contacto(id):
    if request.method == 'POST':
        aux_nombre = request.form['nombre']
        aux_domicilio = request.form['dom']
        aux_razon = request.form['razon']
        aux_tel = request.form['tel']
        aux_email = request.form['email']
        aux_link = request.form['link']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from contacto where Nombre = %s', (aux_nombre))
        contactos = cursor.fetchone()
        if (contactos[0] != 0):
            error = "El Contacto ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/agr_datos_contacto")
        else:
            cursor.execute('update contacto set  Nombre=%s,Domicilio=%s,Razon_Social=%s,Telefono=%s,Email=%s,Link=%s where idcontacto=%s',
                       (aux_nombre, aux_domicilio, aux_razon, aux_tel,aux_email,aux_link, id))
            conn.commit()
            conn.close()
            return redirect(url_for('agr_datos_contacto'))

@app.route('/bo_contacto/<string:id>')
def bo_contacto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from anuncio where idcontacto = {0}'.format(id))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El contacto tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/agr_datos_contacto")
    else:
        cursor.execute('delete from contacto where idcontacto = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('agr_datos_contacto'))

#PROCESOS DE LA EMPRESA

#Solicitud
@app.route('/solicitud')
def solicitud():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select * from solicitud')
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud ')

    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_solicitud.html", solicitudes=datos)

@app.route('/nvo_solicitud')
def nvo_solicitud():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre from area')
    datos1 = cursor.fetchall()
    cursor.execute('select idPuesto, Descripcion from puesto')
    datos2 = cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico')
    datos3 = cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion from carrera')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstatus_Solicitud, Descripcion from estatus_solicitud')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("agrega_solicitud.html", areas=datos1, puestos=datos2, niveles=datos3, carreras=datos4, estados=datos5)

@app.route('/agrega_solicitud', methods=['POST'])
def agrega_solicitud():
    if request.method == 'POST':
        aux_fec = request.form['fecha']
        aux_are = request.form['area_sol']
        aux_pue = request.form['Puesto_sol']
        aux_niv = request.form['Nivel_sol']
        aux_car = request.form['Carrera_sol']
        aux_vac = request.form['Vacantes_sol']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        #---------------------estatus de la solicitud 1 pendiente de aprobacion 2 aprobada (si el puesto------------#
        cursor.execute('select Aprobacion from puesto where idPuesto= %s', (aux_pue))
        req_ap= cursor.fetchone ()
        if req_ap[0]==0:
            # El puesto requiere de autorización
            cursor.execute('insert into solicitud (FechaSolicitud, idArea, idPuesto, idNivelAcademico, idCarrera, '
                           'NumeroVacante, idEstatus_Solicitud) values (%s,%s,%s,%s, %s,%s,1)',(aux_fec, aux_are, aux_pue, aux_niv, aux_car, aux_vac))
        else:
            # El puesto no requiere autorización
            cursor.execute(
                'insert into solicitud (FechaSolicitud, idArea, idPuesto, idNivelAcademico, idCarrera, NumeroVacante, idEstatus_Solicitud) '
                'values (%s,%s,%s,%s, %s,%s,2)',(aux_fec, aux_are, aux_pue, aux_niv, aux_car, aux_vac))

        conn.commit()
        cursor.execute(
            ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            ' from solicitud a, area b, puesto c, estatus_solicitud d '
            ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

        datos = cursor.fetchall()
        conn.close()
    return render_template("tabla_solicitud.html", solicitudes=datos)

@app.route('/ed_solicitud/<string:id>')
def ed_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idSolicitud, FechaSolicitud, NumeroVacante, idArea, idPuesto, idNivelAcademico, idCarrera, idEstatus_Solicitud '
                   'from solicitud where idSolicitud=%s',(id))
    datos=cursor.fetchall()
    cursor.execute('select idArea, AreaNombre from area')
    datos1 = cursor.fetchall()
    cursor.execute('select idPuesto, Descripcion from puesto')
    datos2 = cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico')
    datos3 = cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion from carrera')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstatus_Solicitud, Descripcion from estatus_solicitud')
    datos5 = cursor.fetchall()
    cursor.execute('select NumeroVacante from solicitud')
    datos6 = cursor.fetchall()
    conn.close()
    return render_template("edi_solicitud.html", solicitudes=datos, areas=datos1, puestos=datos2, niveles=datos3, carreras=datos4, estados=datos5, vacantes=datos6[0])

@app.route('/modifica_solicitud/<string:id>', methods=['POST'])
def modifica_solicitud(id):
    if request.method == 'POST':
        aux_fec = request.form['fecha']
        aux_are = request.form['area_sol']
        aux_pue = request.form['Puesto_sol']
        aux_niv = request.form['Nivel_sol']
        aux_car = request.form['Carrera_sol']
        aux_vac = request.form['Vacantes_sol']
        aux_est = request.form['Estatus_sol']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        cursor.execute('update solicitud set FechaSolicitud=%s, idArea=%s, idPuesto=%s, idNivelAcademico=%s, '
                       'idCarrera=%s, NumeroVacante=%s, idEstatus_Solicitud=%s '
                       'where idSolicitud= %s',(aux_fec,aux_are,aux_pue,aux_niv,aux_car,aux_vac,aux_est,id))
        conn.commit()
        cursor.execute(
            ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            ' from solicitud a, area b, puesto c, estatus_solicitud d '
            ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud ')

        datos = cursor.fetchall()
        conn.close()
    return render_template("tabla_solicitud.html", solicitudes=datos)

@app.route('/bo_solicitud/<string:id>')
def bo_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from solicitud where idsolicitud = {0}'.format(id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud ')

    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_solicitud.html", solicitudes=datos)

#AutorizaSolicitud
@app.route('/autoriza_solicitud')
def autoriza_solicitud():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select * from solicitud')
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_autoriza_solicitud.html", solicitudes=datos)

@app.route('/aut_solicitud/<string:id>')
def aut_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('update solicitud set idEstatus_Solicitud=2 where idSolicitud=%s', (id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_autoriza_solicitud.html", solicitudes=datos)

@app.route('/can_solicitud/<string:id>')
def can_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('update solicitud set idEstatus_Solicitud=6 where idSolicitud=%s', (id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_autoriza_solicitud.html", solicitudes=datos)

#Publicacion de Solicitud
@app.route('/a_publicar')
def a_publicar():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3)')

    datos=cursor.fetchall()
    conn.close()
    return render_template("publicacion.html", solicitudes = datos)

@app.route('/crea_pub/<string:id>')
def crea_pub(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (id))

    dato = cursor.fetchone()
    cursor.execute(
        ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        ' from anuncio a, contacto b, mediopublicidad c '
        ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',(id))
    datos = cursor.fetchall()

    cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
    datos1 = cursor.fetchall()
    cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)

@app.route('/agrega_publicacion', methods=['POST'])
def agrega_publicacion():
    if request.method == 'POST':
        aux_sol = request.form['n_solicitud']
        aux_fep = request.form['fecha_pub']
        aux_fec = request.form['fecha_cie']
        aux_solicitantes = request.form['n_solicitantes']
        aux_con = request.form['contacto']
        aux_med = request.form['medio']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        #El Puesto requiere de Autorizacion
        cursor.execute(' insert into anuncio (idSolicitud, Num_Solicitantes, FechaPublicacion, FechaCierre, idcontacto, idMedioPublicidad) '
                       ' values (%s,%s,%s,%s,%s,%s)', ( aux_sol, aux_solicitantes, aux_fep, aux_fec, aux_con, aux_med ))
        conn.commit()
        cursor.execute(' update solicitud set idEstatus_Solicitud=3 where idSolicitud=%s', (aux_sol))
        conn.commit()
        cursor.execute(
            ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            ' from solicitud a, area b, puesto c, estatus_solicitud d '
            ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
            ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (aux_sol))

        dato = cursor.fetchone()
        cursor.execute(
            ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
            ' from anuncio a, contacto b, mediopublicidad c '
            ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s', (aux_sol))
        datos = cursor.fetchall()

        cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
        datos1 = cursor.fetchall()
        cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
        datos2 = cursor.fetchall()
        conn.close()
        return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)

@app.route('/bo_publicacion/<string:id>')
def bo_publicacion(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select idSolicitud from anuncio where idanuncio = {0}'.format(id))
    aux_sol=cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute(' delete from anuncio where idanuncio = {0}'.format(id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (aux_sol[0]))

    dato = cursor.fetchone()
    cursor.execute(
        ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        ' from anuncio a, contacto b, mediopublicidad c '
        ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s', (aux_sol[0]))
    datos = cursor.fetchall()

    cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
    datos1 = cursor.fetchall()
    cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)


##Candidato
@app.route('/candidato')
def candidato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select Curp, Nombre from candidato order by Nombre')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_candidato.html", candidatos = datos)

@app.route('/agrega_candidato', methods=['POST'])
def agrega_candidato():
    if request.method == 'POST':
        aux_cur =request.form['curp']
        aux_rfc = request.form['rfc']
        aux_nom = request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']
        aux_sex = request.form['sexo']
        aux_eci = request.form['edociv']
        aux_nac = request.form['nacionalidad']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from candidato where Curp = %s', (aux_cur))
        candidatos = cursor.fetchone()
        if (candidatos[0] != 0):
            error = "El Candidato ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/candidato")
        else:
            cursor.execute('insert into candidato (Curp, RFC, Nombre, nacionalidad, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil)'
                           ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(aux_cur, aux_rfc, aux_nom, aux_nac, aux_dom, aux_tel, aux_cor, aux_sex, aux_eda, aux_nss, aux_eci))
            conn.commit()

            cursor.execute('select Curp, RFC, Nombre, nacionalidad, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                           ' from candidato where Curp=%s',(aux_cur))
            datos=cursor.fetchall()

            cursor.execute('select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from candidato a, habilidad b, candidato_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(aux_cur))
            datos1=cursor.fetchall()

            cursor.execute('select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel from candidato a, idioma b, candidato_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(aux_cur))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_cur))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()

            
            conn.close()
            return render_template("edi_candidato.html", carrera_can=datos8,candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/nvo_candidato')
def nvo_candidato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idEstadoCivil, Descripcion from estadocivil order by Descripcion')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("candidato.html", ecivil=datos5)

@app.route('/modifica_candidato/<string:Curp>', methods=['POST'])
def modifica_candidato(Curp):
    if request.method == 'POST':
        aux_cur = request.form['curp']
        aux_rfc = request.form['rfc']
        aux_nom = request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']
        aux_sex = request.form['sexo']
        aux_eci = request.form['edociv']
        aux_nac = request.form['nacionalidad']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE candidato
            SET Curp=%s, RFC=%s, Nombre=%s, Domicilio=%s, Telefono=%s, E_Mail=%s, Sexo=%s, Edad=%s, NSS=%s, idEstadoCivil=%s, nacionalidad=%s
            WHERE Curp=%s
        """,(aux_cur,aux_rfc,aux_nom,aux_dom,aux_tel,aux_cor,aux_sex,aux_eda,aux_nss,aux_eci,aux_nac, Curp))
        conn.commit()
        conn.close()
        return redirect(url_for('candidato'))

@app.route('/ed_candidato/<string:Curp>')
def ed_candidato(Curp):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute(' select Curp, RFC, Nombre,nacionalidad,Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato.html", sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/agrega_hab_can/<string:Curp>', methods=['POST'])
def agrega_hab_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['can']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from candidato_has_habilidad where idHabilidad = %s and Curp=%s',(aux_hab,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "Esta habilidad ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/candidato")
        else:
            cursor.execute('insert into candidato_has_habilidad (Curp, idHabilidad, Experiencia) '
                           'values (%s,%s,%s)',(aux_can,aux_hab,aux_exp))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                           ' from candidato where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from candidato a, habilidad b, candidato_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from candidato a, idioma b, candidato_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_candidato.html", carrera_can=datos8,candidatos=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/agrega_idio_can/<string:Curp>', methods=['POST'])
def agrega_idio_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['cani']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from candidato_has_idioma where idIdioma = %s and Curp=%s',(aux_idi,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "El idioma ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/candidato")
        else:
            cursor.execute('insert into candidato_has_idioma (Curp, idIdioma, Nivel) '
                           'values (%s,%s,%s)',(aux_can,aux_idi,aux_niv))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                           ' from candidato where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from candidato a, habilidad b, candidato_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from candidato a, idioma b, candidato_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_candidato.html", carrera_can=datos8,candidatos=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/agrega_aca_can/<string:Curp>', methods=['POST'])
def agrega_aca_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['cana']
        aux_nivel = request.form['nivel']
        aux_carr = request.form['carrera']
        aux_ins = request.form['insti']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from candidato_has_nivelacademico where idNivelAcademico = %s and idCarrera=%s and Curp=%s',(aux_nivel,aux_carr,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "El Nivel Academico ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/candidato")
        else:
            cursor.execute('insert into candidato_has_nivelacademico (Curp, idNivelAcademico,idCarrera, Institucion) '
                           'values (%s,%s,%s,%s)',(aux_can,aux_nivel,aux_carr,aux_ins))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                           ' from candidato where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from candidato a, habilidad b, candidato_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from candidato a, idioma b, candidato_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_candidato.html", carrera_can=datos8,candidatos=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_hab_can/<string:idC>/<string:idH>')
def bo_hab_can(idC,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_habilidad where Curp =%s and idHabilidad=%s',(idC,idH))
    conn.commit()
    cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil from candidato where Curp=%s',(idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from candidato a, habilidad b, candidato_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from candidato a, idioma b, candidato_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8=cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("edi_candidato.html", carrera_can=datos8,candidatos=datos, can_habs=datos1, can_idis=datos2, can_acas=datos6,
                           habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_idi_can/<string:idC>/<string:idI>')
def bo_idi_can(idC,idI):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_idioma where Curp =%s and idIdioma=%s',(idC,idI))
    conn.commit()
    cursor.execute(
        ' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil from candidato where Curp=%s',
        (idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from candidato a, habilidad b, candidato_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from candidato a, idioma b, candidato_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()

    return render_template("edi_candidato.html", carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,
                           can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_aca_can/<string:idC>/<string:idA>/<string:idCA>')
def bo_aca_can(idC,idA,idCA):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_nivelacademico where Curp =%s and idNivelAcademico=%s and idCarrera=%s', (idC, idA,idCA))
    conn.commit()
    cursor.execute(
        ' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil from candidato where Curp=%s',(idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from candidato a, habilidad b, candidato_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from candidato a, idioma b, candidato_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()

    return render_template("edi_candidato.html", carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,
                           can_acas=datos6,
                           habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)


@app.route('/bo_candidato/<string:Curp>')
def bo_candidato(Curp):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from resultadocandidato where Curp = %s', (Curp))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El candidato tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/candidato")
    else:
        cursor.execute('delete from candidato_has_idioma where Curp = %s',(Curp))
        conn.commit()
        cursor.execute('delete from candidato_has_habilidad where Curp = %s',(Curp))
        conn.commit()
        cursor.execute('delete from candidato where Curp = %s',(Curp))
        conn.commit()
        conn.close()
        return redirect(url_for('candidato'))


##Perfil
@app.route('/perfil')
def perfil():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idPerfil, Descripcion from perfil_admo order by Descripcion')
    datos=cursor.fetchall()
    conn.close()
    return render_template("perfil.html", perfiles=datos)

@app.route('/nvo_perfil')
def nvo_perfil():
    return render_template("agrega_perfil.html")

@app.route('/agrega_perfil', methods=['POST'])
def agrega_perfil():
    if request.method == 'POST':
        aux_des = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('insert into perfil_admo (Descripcion) values (%s)',(aux_des))
        conn.commit()

        cursor.execute('select idPerfil, Descripcion from perfil_admo where idPerfil=(select max(idPerfil) from perfil_admo)')
        datos = cursor.fetchall()

        cursor.execute('select a.idPerfil, b.idProceso, b.Descripcion, c.idPerfil, c.idProceso, c.idPermiso, d.id_permiso, d.Descripcion '
                       ' from perfil_admo a, proceso b,perfil_has_proceso c, permisos d '
                       ' where a.idPerfil=c.idPerfil and b.idProceso=c.idProceso and d.id_permiso=c.idPermiso and c.idPerfil=(select max(idPerfil) from perfil_admo)')
        datos1=cursor.fetchall()

        cursor.execute('select idProceso, Descripcion from proceso order by Descripcion')
        datos2 = cursor.fetchall()

        cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
        datos3 = cursor.fetchall()
        conn.close()
        return render_template("edi_perfil.html", perfiles = datos, per_proc=datos1, procesos=datos2, permisos=datos3 )

@app.route('/modifica_perfil/<string:id>', methods=['POST'])
def modifica_perfil(id):
    if request.method == 'POST':
        aux_des =request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update perfil_admo set Descripcion=%s where idPerfil=%s', (aux_des, id))
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))

@app.route('/ed_perfil/<string:id>')
def ed_perfil(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idPerfil, Descripcion from perfil_admo where idPerfil=%s', (id))
    datos = cursor.fetchall()

    cursor.execute(
        'select a.idPerfil, b.idProceso, b.Descripcion, c.idPerfil, c.idProceso, c.idPermiso, d.id_permiso, d.Descripcion '
        ' from perfil_admo a, proceso b,perfil_has_proceso c, permisos d '
        ' where a.idPerfil=c.idPerfil and b.idProceso=c.idProceso and d.id_permiso=c.idPermiso and c.idPerfil=%s',(id))
    datos1 = cursor.fetchall()

    cursor.execute('select idProceso, Descripcion from proceso order by Descripcion')
    datos2 = cursor.fetchall()

    cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("edi_perfil.html", perfiles=datos, per_proc=datos1, procesos=datos2, permisos=datos3)

@app.route('/bo_perfil/<string:id>')
def bo_perfil(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from perfil_has_proceso where idPerfil = {0}'.format(id))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "El Perfil tiene dependientes, no puede ser borrado."
        return render_template("error.html", des_error=error, paginaant="/perfil")
    else:
        cursor.execute('delete from perfil_admo where idPerfil = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))

@app.route('/agrega_proceso_perfil', methods=['POST'])
def agrega_proceso_perfil():
    if request.method == 'POST':
        aux_per=request.form['per']
        aux_pro = request.form['proceso']
        aux_perm = request.form['permiso']
        conn = pymysql.connect(host='localhost', user='root', passwd='',db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('insert into perfil_has_proceso (idPerfil, idProceso, idPermiso) values (%s,%s,%s)',(aux_per,aux_pro,aux_perm))
        conn.commit()

        cursor.execute('select idPerfil, Descripcion from perfil_admo where idPerfil=%s',(aux_per))
        datos = cursor.fetchall()

        cursor.execute('select a.idPerfil, b.idProceso, b.Descripcion, c.idPerfil, c.idProceso, c.idPermiso, d.id_permiso, d.Descripcion '
                       ' from perfil_admo a, proceso b,perfil_has_proceso c, permisos d '
                       ' where a.idPerfil=c.idPerfil and b.idProceso=c.idProceso and d.id_permiso=c.idPermiso and c.idPerfil=%s',(aux_per))
        datos1=cursor.fetchall()

        cursor.execute('select idProceso, Descripcion from proceso order by Descripcion')
        datos2 = cursor.fetchall()

        cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
        datos3 = cursor.fetchall()
        conn.close()
        return render_template("edi_perfil.html", perfiles=datos, per_proc=datos1, procesos=datos2, permisos=datos3 )


@app.route('/bo_proceso_perfil/<string:idP>/<string:idPr>/<string:idPe>')
def bo_proceso_perfil(idP,idPr,idPe):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from perfil_has_proceso where idPerfil =%s and idProceso=%s and idPermiso=%s',(idP,idPr,idPe))
    conn.commit()

    cursor.execute('select idPerfil, Descripcion from perfil_admo where idPerfil=%s', (idP))
    datos = cursor.fetchall()

    cursor.execute(
        'select a.idPerfil, b.idProceso, b.Descripcion, c.idPerfil, c.idProceso, c.idPermiso, d.id_permiso, d.Descripcion '
        ' from perfil_admo a, proceso b,perfil_has_proceso c, permisos d '
        ' where a.idPerfil=c.idPerfil and b.idProceso=c.idProceso and d.id_permiso=c.idPermiso and c.idPerfil=%s',
        (idP))
    datos1 = cursor.fetchall()

    cursor.execute('select idProceso, Descripcion from proceso order by Descripcion')
    datos2 = cursor.fetchall()

    cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("edi_perfil.html", perfiles=datos, per_proc=datos1, procesos=datos2, permisos=datos3)


##Usuario
@app.route('/usuario')
def usuario():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idUsuario, Usuario, Nombre, Password, Perfil from usuario order by Nombre')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_usuario.html", usuarios=datos)

@app.route('/nvo_usuario')
def nvo_usuario():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idPerfil, Descripcion from perfil_admo order by Descripcion')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("agrega_usuario.html", pers=datos2)

@app.route('/agrega_usuario', methods=['POST'])
def agrega_usuario():
    if request.method == 'POST':
        aux_usuario = request.form['Usuario']
        aux_pass = request.form['Password']
        aux_nom = request.form['Nombre']
        aux_perfil = request.form ['per']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('insert into usuario (Usuario, Password, Nombre, Perfil) '
                       'values (%s,%s,%s,%s)', (aux_usuario, aux_pass, aux_nom, aux_perfil))
        conn.commit()

        cursor.execute('select idUsuario, Usuario, Password, Nombre, Perfil '
                       'from usuario where idUsuario=(select max(idUsuario) from usuario)')
        datos = cursor.fetchall()

        cursor.execute('select a.idUsuario, a.Perfil, b.Descripcion '
                       ' from usuario a, perfil_admo b '
                       ' where a.Perfil=b.idPerfil and b.idPerfil=(select max(idPerfil) from perfil_admo)')
        datos1=cursor.fetchall()

        cursor.execute('select idPerfil, Descripcion from perfil_admo order by Descripcion')
        datos2 = cursor.fetchall()
        conn.close()
        return redirect(url_for('usuario'))

@app.route('/agrega_per_usu/<string:id>', methods=['POST'])
def agrega_per_usu(id):
    if request.method == 'POST':
        aux_perfil = request.form['per']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update usuario set Perfil=%s'
                       'where idUsuario=%s', (aux_perfil, id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuario'))


@app.route('/bo_usuario/<string:id>')
def  bo_usuario(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from usuario where idUsuario={0}'.format(id))
    conn.commit()
    conn.close()
    return redirect(url_for('usuario'))

@app.route('/modifica_usuario/<string:id>', methods=['POST'])
def modifica_usuario(id):
    if request.method == 'POST':
        aux_usuario = request.form['Usuario']
        aux_pass = request.form['Password']
        aux_nom = request.form['Nombre']
        aux_perfil = request.form['per']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update usuario set Usuario=%s, Password=%s, Nombre=%s, Perfil=%s'
                       'where idUsuario=%s', (aux_usuario, aux_pass, aux_nom, aux_perfil,id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuario'))

@app.route('/ed_usuario/<string:id>')
def ed_usuario(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idUsuario, Usuario, Password, Nombre, Perfil from usuario where idUsuario=%s', (id))
    datos = cursor.fetchall()
    cursor.execute('select a.idUsuario, a.Perfil, b.Descripcion, b.idPerfil from usuario a, perfil_admo b where a.Perfil=b.idPerfil and a.idUsuario=%s', (id))
    datos1=cursor.fetchall()
    cursor.execute('select idPerfil, Descripcion from perfil_admo order by Descripcion')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("edi_usuario.html", usuarios = datos, usu_per=datos1, pers=datos2 )


#------------------------Selecciona Candidato--------------------------------#

@app.route('/agr_sel_candidato')
def agr_sel_candidato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos=cursor.fetchall()

    return render_template("tabla_sel_candidato.html", solicitudes=datos)

@app.route('/termina_sol_can/<string:id>')
def termina_sol_can(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('update solicitud set idEstatus_Solicitud=5 where idSolicitud=%s',(id))
    conn.commit()
    conn.close()
    return redirect(url_for('agr_sel_candidato'))


@app.route('/sel_candidato/<string:id>')
def sel_candidato(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))

    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
    'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
    'where b.curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera order by Nombre')
    datos=cursor.fetchall()

    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()

    return render_template("tabla_agr_sel_candidato.html",sol=dato_sol, candidatos=datos, can_seleccionados=datos1, solicitud=id)

@app.route('/ins_candidato/<string:ca>/<string:so>/<string:ans>')
def ins_candidato(ca,so,ans):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from resultadocandidato where idSolicitud=%s and Curp=%s',(so,ca))
    solicitudes=cursor.fetchone()
    if (solicitudes[0] != 0):
        error = "No puede eleccionar a un candidato mas de dos veces."
        return render_template("error.html", des_error=error, paginaant="/agr_sel_candidato")
    else:
        cursor.execute('insert into resultadocandidato (idSolicitud,Curp,Calificacion_Medica, Calificacion, validacion, estatus, Validar_ref, EstatusProceso) values (%s,%s,%s,%s,%s,%s,%s,1)',(so,ca,ans,ans, ans,ans, ans))
        conn.commit()
        cursor.execute(
            ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            ' from solicitud a, area b, puesto c, estatus_solicitud d '
            ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
            ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (so))

        dato_sol = cursor.fetchone()
        cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
        'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
        'where b.curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera order by Nombre')
        datos=cursor.fetchall()

        cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion '
        'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
        'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
        'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (so))
        datos1=cursor.fetchall()

        return render_template("tabla_agr_sel_candidato.html",sol=dato_sol, candidatos=datos, can_seleccionados=datos1, solicitud=so)


@app.route('/bo_sol_candidato/<string:ca>/<string:so>')
def bo_sol_candidato(ca,so):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from resultadocandidato where idSolicitud=%s and Curp=%s',(so, ca))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (so))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
    'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
    'where b.curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera order by Nombre')
    datos=cursor.fetchall()

    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (so))
    datos1=cursor.fetchall()

    return render_template("tabla_agr_sel_candidato.html",sol=dato_sol, candidatos=datos, can_seleccionados=datos1, solicitud=so)

@app.route('/ed_candidato2/<string:Curp>/<string:id>')
def ed_candidato2(Curp,id):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato2.html", sexo=sexos,carrera_can=datos8,solicitud=id, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/crea_pub2/<string:id>')
def crea_pub2(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (id))

    dato = cursor.fetchone()
    cursor.execute(
        ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        ' from anuncio a, contacto b, mediopublicidad c '
        ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',(id))
    datos = cursor.fetchall()

    cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
    datos1 = cursor.fetchall()
    cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("crea_publicacion2.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)
#----------Fin Selecciona Candidato------------------#


#------------------------Calificacion Psicologica--------------------------------#

@app.route('/agr_cal_psicologica')
def agr_cal_psicologica():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos=cursor.fetchall()
    return render_template("tabla_calf_psicologica.html", solicitudes=datos)


@app.route('/nvo_calf_psicologica/<string:ca>/<string:so>')
def nvo_calf_psicologica(ca,so):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (so))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
                   'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
                   'where b.Curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and'
                   '(SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s)',
                   (so))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Personalidad, a.Coeficiente_Intelectual, a.Calificacion, a.idSolicitud, a.Califica_el_Perfil '
                   'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
                   'where b.Curp = a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
                   'and e.idCarrera = c.idCarrera and a.Curp=%s and a.idSolicitud=%s order by Nombre',(ca,so))
    datos1 = cursor.fetchall()
    return render_template("calificacion_psicologica.html",candidatos=datos, can_seleccionados=datos1, sol=dato_sol, idSolicitud=id)

@app.route('/cal_sel_candidato/<string:id>')
def cal_sel_candidato(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
                   'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
                   'where b.Curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and'
                   '(SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s)',(id))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Personalidad, a.Coeficiente_Intelectual, a.Calificacion, a.idSolicitud, a.Califica_el_Perfil '
                   'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
                   'where b.Curp = a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
                   'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre',(id))
    datos1 = cursor.fetchall()
    return render_template("tabla_calf_psico_candidatos.html",candidatos=datos, can_seleccionados=datos1, sol=dato_sol, idSolicitud=id)

@app.route('/agrega_calf_psicologica/<string:so>/<string:ca>', methods=["POST"])
def agrega_calf_psicologica(so,ca):
    if request.method == 'POST':
        aux_per = request.form['analisis']
        aux_cal = request.form['apto']
        aux_coe = request.form['coeint']
        aux_cal_p = request.form['cal_p']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update resultadocandidato set Personalidad = %s, Coeficiente_Intelectual = %s, Calificacion = %s, Califica_el_Perfil = %s, EstatusProceso=2  '
                       'where resultadocandidato.idSolicitud = %s and resultadocandidato.Curp = %s', (aux_per,aux_coe, aux_cal, aux_cal_p, so, ca))
        conn.commit()
        conn.close()
        return redirect(url_for('cal_sel_candidato',id=so))
#------------------------Fin Calificacion Psicologica--------------------------------#



#------------------------Calificacion Medica----------------------------------------#
@app.route('/agr_cal_medica')
def agr_cal_medica():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos = cursor.fetchall()
    return render_template("tabla_calf_medica2.html", can_seleccionados=datos)


@app.route('/nvo_calf_medica/<string:id>')
def nvo_calf_medica(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))

    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
    'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
    'where b.curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera order by Nombre')
    datos=cursor.fetchall()

    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Calificacion_Medica '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()


    return render_template("tabla_calf_candidato_medica.html",sol=dato_sol, candidatos=datos, can_seleccionados=datos1, solicitud=id)

@app.route('/cal_med/<string:Curp>/<string:ap>/<string:id>')
def cal_med(Curp,ap,id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('update resultadocandidato set Calificacion_Medica=%s, EstatusProceso=3 where Curp=%s and idSolicitud=%s',(ap,Curp,id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
    cursor.execute(
        'select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Calificacion_Medica '
        'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
        'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
        'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1 = cursor.fetchall()
    conn.close()
    return render_template("tabla_calf_candidato_medica.html", can_seleccionados=datos1, sol=dato_sol, solicitud=id)

#------------------------Fin Calificacion Medica--------------------------------#



#------------------------Calificacion Tecnica-----------------------------------#
@app.route('/agr_sel_candidato2')
def agr_sel_candidato2():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos=cursor.fetchall()

    return render_template("tabla_calf_tecnica.html", solicitudes=datos)

@app.route('/sel_candidato2/<string:id>')
def sel_candidato2(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))

    dato_sol = cursor.fetchone()

    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.validacion '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()

    return render_template("tabla_agr_calf_tecnica.html",sol=dato_sol, can_seleccionados=datos1, solicitud=id)


@app.route('/bo_sol_candidato2/<string:ca>/<string:so>')
def bo_sol_candidato2(ca,so):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from resultadocandidato where idSolicitud=%s and Curp=%s',(so, ca))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (so))
    dato_sol = cursor.fetchone()

    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()

    return render_template("tabla_agr_calf_tecnica.html",sol=dato_sol, can_seleccionados=datos1, solicitud=so)

@app.route('/ed_candidato3/<string:Curp>/<string:id>/<string:ca>/')
def ed_candidato3(Curp,ca,id):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        cursor.execute('update resultadocandidato set validacion=%s where Curp=%s and idSolicitud=%s', (ca, Curp, id))
        conn.commit()



        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()


        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion, d.valida'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()


        conn.close()
        return render_template("edi_candidato3.html",sol=id ,sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)


@app.route('/cal_hab_cdto/<string:Curp>/<string:idH>/<string:co>/<string:id>')
def cal_hab_cdto(Curp,idH,co,id):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update candidato_has_habilidad set valida=%s where Curp=%s and idHabilidad=%s',(co,Curp,idH))
        conn.commit()

        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion, d.valida'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato3.html",sol=id ,sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/cal_idio_cdto/<string:Curp>/<string:idI>/<string:ca>/<string:id>')
def cal_idio_cdto(Curp,idI,ca,id):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update candidato_has_idioma set valida=%s where Curp=%s and idIdioma=%s',(ca,Curp,idI))
        conn.commit()

        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion, d.valida'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato3.html",sol=id,sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/cal_aca_cdto/<string:Curp>/<string:idA>/<string:co>/<string:id>')
def cal_aca_cdto(Curp,idA,co,id):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update candidato_has_nivelacademico set valida=%s where Curp=%s and idNivelAcademico=%s',(co,Curp,idA))
        conn.commit()

        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion, d.valida'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()

        conn.close()
        return render_template("edi_candidato3.html",sol=id,sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/cal_aca_cdto/<string:Curp>/<string:idA>/<string:ca>')
def cal_val_cdto(Curp,idA,ca):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('update resultadocandidato set validacion=%s where Curp=%s and idNivelAcademico=%s',(ca,Curp,idA))
        conn.commit()

        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion, d.valida'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()



        conn.close()
        return render_template("edi_candidato3.html", sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

#----------Fin Calificacion Tecnica ------------------#

#----------Validacion de referencias ------------------#
@app.route('/agr_valida_referencia')
def agr_valida_referencia():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos=cursor.fetchall()

    return render_template("validacion_referencias.html", solicitudes=datos)

@app.route('/cal_sel_candidato2/<string:id>')
def cal_sel_candidato2(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.validacion '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()
    conn.close()
    return render_template("tabla_validacion_referecias.html",can_seleccionados=datos1, sol=dato_sol, solicitud=id)

@app.route('/cal_val_ref/<string:Curp>/<string:ca>/<string:id>')
def cal_val_ref(Curp,ca,id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('update resultadocandidato set Validar_ref=%s where Curp=%s and idSolicitud=%s',(ca,Curp,id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
    cursor.execute(
        'select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Validar_ref '
        'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
        'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
        'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1 = cursor.fetchall()
    conn.close()
    return render_template("tabla_validacion_referecias.html", can_seleccionados=datos1, sol=dato_sol, solicitud=id)

#---------------- NUEVO MÓDULO DE CONTRATACIÓN ------------------#

#------------------------ Selecciona Candidato a contratar --------------------------------#


@app.route('/agr_candidato_contratacion')
def agr_candidato_contratacion():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, '
        'a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud '
        'and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4)')
    datos=cursor.fetchall()
    return render_template("mue_candidato_contratacion.html", solicitudes=datos)


@app.route('/sel_candidato_contratacion/<string:id>')
def sel_candidato_contratacion(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion,a.idsolicitud, a.validacion ,a.estatus ,a.Calificacion, a.Calificacion_Medica,a.Validar_ref '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()
    conn.close()
    return render_template("sel_can_cont.html",can_seleccionados=datos1, sol=dato_sol, solicitud=id)


@app.route('/muestra_calf_psicologica/<string:ca>/<string:so>')
def muestra_calf_psicologica(ca,so):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=3 or a.idEstatus_Solicitud=4) and idSolicitud=%s', (so))
    dato_sol = cursor.fetchone()
    cursor.execute('select a.Curp, a.Nombre, b.idNivelAcademico, b.idCarrera, c.Descripcion, d.Descripcion '
                   'from candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d '
                   'where b.Curp = a.Curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and'
                   '(SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s)',
                   (so))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion, a.Personalidad, a.Coeficiente_Intelectual, a.Calificacion, a.idSolicitud, a.Califica_el_Perfil '
                   'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
                   'where b.Curp = a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
                   'and e.idCarrera = c.idCarrera and a.Curp=%s and a.idSolicitud=%s order by Nombre',(ca,so))
    datos1 = cursor.fetchall()
    return render_template("mue_cal_psicologica.html",candidatos=datos, can_seleccionados=datos1, sol=dato_sol, idSolicitud=id)


@app.route('/mue_per_candidato/<string:Curp>')
def mue_per_candidato(Curp):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil'
                       ' from candidato where Curp=%s',(Curp))
        datos=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia, c.valida'
                       ' from candidato a, habilidad b, candidato_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel, c.valida'
                       ' from candidato a, idioma b, candidato_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                       ' from candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from candidato where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()
        conn.close()
        return render_template("mue_per_candidato.html", sexo=sexos,carrera_can=datos8, candidatos=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/contrata_candidato/<string:id>/<string:curp>/<string:estado>')
def contrata_candidato(id,curp,estado):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute("update resultadocandidato set estatus=%s where idsolicitud=%s and curp=%s ",(estado,id,curp))
    conn.commit()
    
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and idSolicitud=%s', (id))
    dato_sol = cursor.fetchone()
   
    cursor.execute('select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.Descripcion, e.Descripcion,a.idsolicitud,a.validacion ,a.estatus ,a.Calificacion, a.Calificacion_Medica,a.Validar_ref  '
    'from resultadocandidato a, candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e '
    'where b.curp= a.Curp and c.Curp = b.Curp and d.idNivelAcademico = c.idNivelAcademico '
    'and e.idCarrera = c.idCarrera and a.idSolicitud=%s order by Nombre', (id))
    datos1=cursor.fetchall()
    conn.close()
    return render_template("sel_can_cont.html",can_seleccionados=datos1, sol=dato_sol, solicitud=id)

#-----Captura de Datos de empleado-------#

@app.route('/empleado')
def empleado():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select Curp, Nombre from empleado order by Nombre')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_empleado.html", empleados = datos)

@app.route('/nvo_empleado')
def nvo_empleado():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select idEstadoCivil, Descripcion from estadocivil order by Descripcion')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("empleado.html", ecivil=datos5)

@app.route('/agrega_empleado', methods=['POST'])
def agrega_empleado():
    if request.method == 'POST':
        aux_cur = request.form['curp']
        aux_rfc = request.form['rfc']
        aux_nom = request.form['nombre']
        aux_nac = request.form['nacionalidad']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']
        aux_sex = request.form['sexo']
        aux_eci = request.form['edociv']        
        aux_nomc = request.form['nomcoy']
        aux_nomcaux = request.form['nomcaux']
        aux_telaux= request.form['telaux']
        aux_numinfonavit =request.form['numinfonavit']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from empleado where Curp = %s', (aux_cur))
        candidatos = cursor.fetchone()
        if (candidatos[0] != 0):
            error = "El Empleado ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/empleado")
        else:
            cursor.execute('insert into empleado (Curp, RFC, Nombre, nacionalidad, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit )'
                           ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(aux_cur, aux_rfc, aux_nom, aux_nac, aux_dom, aux_tel, aux_cor, aux_sex, aux_eda, aux_nss, aux_eci,aux_nomc,aux_telaux,aux_nomcaux,aux_numinfonavit))
            conn.commit()

            cursor.execute('select Curp, Nombre, RFC, Domicilio, nacionalidad , Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil,Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                           ' from empleado where Curp=%s',(aux_cur))
            datos=cursor.fetchall()

            cursor.execute('select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from empleado a, habilidad b, empleado_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(aux_cur))
            datos1=cursor.fetchall()

            cursor.execute('select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel from empleado a, idioma b, empleado_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(aux_cur))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_cur))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()

            conn.close()
            return render_template("edi_empleado.html", carrera_can=datos8,empleados=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)



@app.route('/bo_empleado/<string:Curp>')
def bo_empleado(Curp):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from empleado_has_idioma where Curp = %s',(Curp))
    conn.commit()
    cursor.execute('delete from empleado_has_habilidad where Curp = %s',(Curp))
    conn.commit()
    cursor.execute('delete from empleado where Curp = %s',(Curp))
    conn.commit()
    conn.close()
    return redirect(url_for('empleado'))

@app.route('/curp_empleado')
def curp_empleado():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select Curp, Nombre from candidato order by Nombre')
    datos=cursor.fetchall()
    conn.close()
    return render_template("curp_empleado.html", empleados = datos)



@app.route('/import_empleado/<string:val>', methods=['POST'])
def import_empleado(val):
    if request.method == 'POST':
        aux_cur = request.form['curp']
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from empleado where Curp = %s', (aux_cur))
    candidatos=cursor.fetchone()
    cursor.execute('select count(*) from candidato where Curp = %s', (aux_cur))
    noexist=cursor.fetchone()
    
    if (noexist [0] == 0 ):
        error = "No hay nadie asignado con esta CURP."
        return render_template("error.html", des_error=error, paginaant="/empleado")
    else:
        cursor.execute('select estatus from resultadocandidato where Curp = %s', (aux_cur))
        contratado = cursor.fetchone()
        if (contratado [0] == "No"):
            error = "El Empleado no ha sido contratado."
            return render_template("error.html", des_error=error, paginaant="/empleado")
        else:
            if (candidatos [0] != 0):
                error = "El Empleado ya se encuentra agregado."
                return render_template("error.html", des_error=error, paginaant="/empleado")
            else:
                cursor.execute('INSERT INTO `empleado`(`Curp`, `RFC`, `Nombre`, `Domicilio`, `Telefono`, `E_mail`, `Sexo`, `Edad`, `NSS`, `idEstadoCivil`)'
                       'SELECT `Curp`,`RFC`,`Nombre`,`Domicilio`,`Telefono`,`E_Mail`,`Sexo`,`Edad`,`NSS`,`idEstadoCivil`'
                       'FROM candidato where CURP=%s',(aux_cur)
                       )
                conn.commit()
                
                

                cursor.execute('INSERT INTO `empleado_has_nivelacademico`(`Curp`, `idNivelAcademico`, `idCarrera`, `Institucion`, `valida`)'
                                'Select `Curp`, `idNivelAcademico`, `idCarrera`, `Institucion`, `valida`'
                                'from candidato_has_nivelacademico where CURP=%s',(aux_cur)
                                )
                conn.commit()

                cursor.execute('INSERT INTO `empleado_has_habilidad`(`Curp`,`idHabilidad`, `Experiencia`, `valida`)'
                                'SELECT `Curp`,`idHabilidad`, `Experiencia`, `valida`'
                                'FROM candidato_has_habilidad where CURP=%s',(aux_cur))
                conn.commit()

                cursor.execute(
                    'INSERT INTO `empleado_has_idioma`(`Curp`, `idIdioma`, `NIvel`, `valida`)'
                    'SELECT `Curp`, `idIdioma`, `NIvel`, `valida`'
                    'FROM candidato_has_idioma where CURP=%s',(aux_cur))

                conn.commit()

                conn.close()

    return redirect(url_for('empleado'))


@app.route('/ed_empleado/<string:Curp>')
def ed_empleado(Curp):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute(' select Curp, RFC, Nombre, Domicilio, nacionalidad, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                       ' from empleado where Curp=%s',(Curp))
        datos=cursor.fetchall()


        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                       ' from empleado a, habilidad b, empleado_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                       ' from empleado a, idioma b, empleado_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                       ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()

        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from empleado where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()

        conn.close()
        return render_template("ed_empleado.html" ,sexo=sexos,carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)



@app.route('/modifica_empleado/<string:Curp>', methods=['POST'])
def modifica_empleado(Curp):
    if request.method == 'POST':
        aux_cur = request.form['curp']
        aux_rfc = request.form['rfc']
        aux_nom = request.form['nombre']
        aux_nac = request.form['nacionalidad']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_sex = request.form['sexo']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']

        aux_eci = request.form['edociv']

        aux_nomc = request.form['nomcoy']
        aux_nomcaux = request.form['nomcaux']
        aux_telaux= request.form['telaux']
        aux_numinfonavit =request.form['numinfonavit']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()

        cursor.execute(
                'update empleado '
                'set Curp=%s, RFC=%s, Nombre=%s, Nacionalidad=%s, Domicilio=%s, Telefono=%s, E_Mail=%s, Sexo=%s, Edad=%s, NSS=%s, idEstadoCivil=%s,Conyuje_Concubino=%s,tel_emergencia=%s, nombre_emergencia=%s, no_infonavit=%s '
                'where Curp=%s'
        ,(aux_cur,aux_rfc,aux_nom,aux_nac,aux_dom,aux_tel,aux_cor,aux_sex,aux_eda,aux_nss,aux_eci,aux_nomc,aux_telaux,aux_nomcaux,aux_numinfonavit,Curp))
        conn.commit()
        conn.close()
        return redirect(url_for('empleado')) 

@app.route('/agrega_emp_hab_can/<string:Curp>', methods=['POST'])
def agrega_emp_hab_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['can']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from empleado_has_habilidad where idHabilidad = %s and Curp=%s',(aux_hab,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "Esta habilidad ya se encuentra agregada."
            return render_template("error.html", des_error=error, paginaant="/empleado")
        else:
            cursor.execute('insert into empleado_has_habilidad (Curp, idHabilidad, Experiencia) '
                           'values (%s,%s,%s)',(aux_can,aux_hab,aux_exp))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                           ' from empleado where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from empleado a, habilidad b, empleado_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from empleado a, idioma b, empleado_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_empleado.html", carrera_can=datos8,empleados=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/agrega_emp_idio_can/<string:Curp>', methods=['POST'])
def agrega_emp_idio_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['cani']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from empleado_has_idioma where idIdioma = %s and Curp=%s',(aux_idi,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "El idioma ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/empleado")
        else:
            cursor.execute('insert into empleado_has_idioma (Curp, idIdioma, Nivel) '
                           'values (%s,%s,%s)',(aux_can,aux_idi,aux_niv))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                           ' from empleado where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from empleado a, habilidad b, empleado_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from empleado a, idioma b, empleado_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_empleado.html", carrera_can=datos8,empleados=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/agrega_emp_aca_can/<string:Curp>', methods=['POST'])
def agrega_emp_aca_can(Curp):
    if request.method == 'POST':
        aux_can = request.form['cana']
        aux_nivel = request.form['nivel']
        aux_carr = request.form['carrera']
        aux_ins = request.form['insti']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
        cursor = conn.cursor()
        cursor.execute('select count(*) from empleado_has_nivelacademico where idNivelAcademico = %s and idCarrera=%s and Curp=%s',(aux_nivel,aux_carr,aux_can))
        existe = cursor.fetchone()
        if (existe[0] != 0):
            error = "El Nivel Academico ya se encuentra agregado."
            return render_template("error.html", des_error=error, paginaant="/empleado")
        else:
            cursor.execute('insert into empleado_has_nivelacademico (Curp, idNivelAcademico,idCarrera, Institucion) '
                           'values (%s,%s,%s,%s)',(aux_can,aux_nivel,aux_carr,aux_ins))
            conn.commit()
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                           ' from empleado where Curp=%s', (aux_can))
            datos = cursor.fetchall()
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                           ' from empleado a, habilidad b, empleado_has_habilidad c'
                           ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_can))
            datos1 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                           ' from empleado a, idioma b, empleado_has_idioma c'
                           ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_can))
            datos2 = cursor.fetchall()

            cursor.execute(
                ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                (aux_can))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()
            conn.close()
            return render_template("edi_empleado.html", carrera_can=datos8,empleados=datos, can_habs=datos1,
                can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4,nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_emp_hab_can/<string:idC>/<string:idH>')
def bo_emp_hab_can(idC,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from empleado_has_habilidad where Curp =%s and idHabilidad=%s',(idC,idH))
    conn.commit()
    cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit from empleado where Curp=%s',(idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from empleado a, habilidad b, empleado_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from empleado a, idioma b, empleado_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8=cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("edi_empleado.html", carrera_can=datos8,empleados=datos, can_habs=datos1, can_idis=datos2, can_acas=datos6,
                           habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_emp_idi_can/<string:idC>/<string:idI>')
def bo_emp_idi_can(idC,idI):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from empleado_has_idioma where Curp =%s and idIdioma=%s',(idC,idI))
    conn.commit()
    cursor.execute(
        ' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit from empleado where Curp=%s',
        (idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from empleado a, habilidad b, empleado_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from empleado a, idioma b, empleado_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()

    return render_template("edi_empleado.html", carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,
                           can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/bo_emp_aca_can/<string:idC>/<string:idA>/<string:idCA>')
def bo_emp_aca_can(idC,idA,idCA):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('delete from empleado_has_nivelacademico where Curp =%s and idNivelAcademico=%s and idCarrera=%s', (idC, idA,idCA))
    conn.commit()
    cursor.execute(
        ' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit from empleado where Curp=%s',(idC))
    datos = cursor.fetchall()
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                   ' from empleado a, habilidad b, empleado_has_habilidad c'
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (idC))
    datos1 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                   ' from empleado a, idioma b, empleado_has_idioma c'
                   ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (idC))
    datos2 = cursor.fetchall()

    cursor.execute(
        ' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
        ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
        (idC))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()
    conn.close()

    return render_template("edi_empleado.html", carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,
                           can_acas=datos6,
                           habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)







##Contrato temporal
@app.route('/contrato')
def contrato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute(' select Curp, Nombre, ContratoTemporal_val from empleado order by Nombre')
    datos=cursor.fetchall()
    conn.close()
    return render_template("tabla_contrato.html", empleados = datos)

@app.route('/ed_contrato/<string:Curp>')
def ed_contrato(Curp):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('select count(*) from contrato where Curp = %s',(Curp))
    existe = cursor.fetchone()
    if (existe[0] == 0):
        error = "Este empleado aun no tiene contrato."
        return render_template("error.html", des_error=error, paginaant="/contrato")

    else:
        cursor.execute(' select Curp, RFC, Nombre,nacionalidad,Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                       ' from empleado where Curp=%s',(Curp))
        datos=cursor.fetchall()


        cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                       ' from empleado a, habilidad b, empleado_has_habilidad c'
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
        datos1=cursor.fetchall()

        cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                       ' from empleado a, idioma b, empleado_has_idioma c'
                       ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
        datos2 = cursor.fetchall()

        cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                       ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
        datos6 = cursor.fetchall()


        cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()

        cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()

        cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(' select Curp,Sexo from empleado where Curp=%s',(Curp))
        sexos = cursor.fetchall()

        cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
        datos8=cursor.fetchall()

        cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
        datos5 = cursor.fetchall()

        cursor.execute('  SELECT a.idContrato, a.Curp, a.idPuesto,b.Descripcion, a.idArea, c.AreaNombre ,a.Salario,a.dias_de_pago , a.fecha_inicio, a.fecha_fin, a.idJornada, e.jornombre , a.horas_semana, e.Descripcion, a.horario'
                        ' FROM contrato a, puesto b, area c , jornada e'
                        ' where a.idPuesto=b.idPuesto and a.idArea= c.idArea and a.idJornada= e.IdJornada and a.curp=%s',(Curp))
        datos9=cursor.fetchall()

        conn.close()
        return render_template("ed_contrato.html" ,datoscontrato=datos9,sexo=sexos,carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)


@app.route('/nvo_contrato/<string:Curp>')
def nvo_contrato(Curp):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()  
    cursor.execute('select count(*) from contrato where Curp = %s',(Curp))
    existecontrato = cursor.fetchone()
    if (existecontrato[0]!= 0 ):
        error = "Este empleado ya tiene contrato."
        return render_template("error.html", des_error=error, paginaant="/contrato")

    else:
        cursor.execute('select count(*) from resultadocandidato where Curp = %s',(Curp))
        existe = cursor.fetchone()
        if (existe[0] == 0):
            cursor.execute(' select Curp, RFC, Nombre,nacionalidad, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                        ' from empleado where Curp=%s',(Curp))
            datos=cursor.fetchall()
            
            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                        ' from empleado a, habilidad b, empleado_has_habilidad c'
                        ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
            datos1=cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                        ' from empleado a, idioma b, empleado_has_idioma c'
                        ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
            datos2 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                        ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
            datos6 = cursor.fetchall()

            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute(' select Curp,Sexo from empleado where Curp=%s',(Curp))
            sexos = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()

            cursor.execute('select idArea, AreaNombre, AreaDescripcion from area ')
            datos9 = cursor.fetchall()

            cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion from puesto '
                        'order by Descripcion')
            datos10 = cursor.fetchall()        

            cursor = mysql.connection.cursor()
            query = "select * from jornada"
            cursor.execute(query)
            jornada = cursor.fetchall()
            message = ''  

            cursor.execute('SELECT idTurno, Tipo FROM turno')
            datos12=cursor.fetchall()

            conn.close()
            return render_template("nvo_contrato2.html" , jornada=jornada, message=message,turnos=datos12,sexo=sexos,carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5, areas=datos9, puestos=datos10)
        else:
            cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
                        ' from empleado where Curp=%s',(Curp))
            datos=cursor.fetchall()


            cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
                        ' from empleado a, habilidad b, empleado_has_habilidad c'
                        ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
            datos1=cursor.fetchall()

            cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
                        ' from empleado a, idioma b, empleado_has_idioma c'
                        ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
            datos2 = cursor.fetchall()

            cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
                        ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
                        ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
            datos6 = cursor.fetchall()


            cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
            datos3 = cursor.fetchall()

            cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
            datos4 = cursor.fetchall()

            cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
            datos7 = cursor.fetchall()

            cursor.execute(' select Curp,Sexo from empleado where Curp=%s',(Curp))
            sexos = cursor.fetchall()

            cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
            datos8=cursor.fetchall()

            cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
            datos5 = cursor.fetchall()

            cursor.execute('select a.idsolicitud, b.idarea,c.areanombre, b.idpuesto, d.descripcion, d.SalarioMensual'
                        ' from resultadocandidato a, solicitud b, area c, puesto d '
                        'where b.idsolicitud=a.idsolicitud and c.idarea=b.idarea and d.idpuesto=b.idpuesto and a.curp=%s' , (Curp))
            datos9=cursor.fetchall()

            cursor.execute('SELECT idTurno, Tipo FROM turno')
            datos10=cursor.fetchall()

            cursor = mysql.connection.cursor()
            query = "select * from jornada"
            cursor.execute(query)
            jornada = cursor.fetchall()
            message = ''  

            conn.close()
        return render_template("nvo_contrato.html", impor=datos9,turnos=datos10,jornada=jornada,message=message, sexo=sexos,carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2,can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5)

@app.route('/nvo_contrato/state/<get_state>')
def statebycountry(get_state):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM jordesc WHERE IdJornada = %s", [get_state])
    state = cur.fetchall()  
    stateArray = []
    for row in state:
        stateObj = {
                'iddesc': row['iddesc'],
                'name': row['name']}
        stateArray.append(stateObj)
    return jsonify({'statecountry' : stateArray})

   

@app.route('/modifica_contrato/<string:Curp>')
def modifica_contrato(Curp):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    
    cursor.execute(' select Curp, RFC, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil, Conyuje_Concubino,tel_emergencia, nombre_emergencia, no_infonavit'
            ' from empleado where Curp=%s',(Curp))
    datos=cursor.fetchall()
            
    cursor.execute(' select a.Curp, b.idHabilidad, b.Descripcion, c.Curp, c.idHabilidad, c.Experiencia'
            ' from empleado a, habilidad b, empleado_has_habilidad c'
            ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(Curp))
    datos1=cursor.fetchall()

    cursor.execute(' select a.Curp, b.idIdioma, b.Lenguaje, c.Curp, c.idIdioma, c.Nivel'
            ' from empleado a, idioma b, empleado_has_idioma c'
            ' where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(Curp))
    datos2 = cursor.fetchall()

    cursor.execute(' select a.Curp, b.idNivelAcademico, b.Descripcion, c.idCarrera, c.Descripcion, d.Curp, d.idNivelAcademico, d.idCarrera, d.Institucion'
            ' from empleado a, nivelacademico b, carrera c, empleado_has_nivelacademico d'
            ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(Curp))
    datos6 = cursor.fetchall()

    cursor.execute(' select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()

    cursor.execute(' select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()

    cursor.execute(' select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(' select Curp,Sexo from empleado where Curp=%s',(Curp))
    sexos = cursor.fetchall()

    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos8=cursor.fetchall()

    cursor.execute(' select idEstadoCivil, Descripcion from estadocivil')
    datos5 = cursor.fetchall()

    cursor.execute('select idArea, AreaNombre, AreaDescripcion from area ')
    datos9 = cursor.fetchall()

    cursor.execute('select idPuesto, Descripcion, SalarioMensual, Beneficios, Bonos, Aprobacion from puesto '
                   'order by Descripcion')
    datos10 = cursor.fetchall()        

    cursor.execute('  SELECT a.idContrato, a.Curp, a.idPuesto,b.Descripcion, a.idArea, c.AreaNombre ,a.Salario,a.dias_de_pago , a.fecha_inicio, a.fecha_fin, a.idJornada, a.horas_semana, a.horario '
                   '  FROM contrato a, puesto b, area c '
                   '  where a.idPuesto=b.idPuesto and a.idArea= c.idArea and a.curp=%s',(Curp))
    datos13=cursor.fetchall()    
    
    cursor = mysql.connection.cursor()
    query = "select * from jornada"
    cursor.execute(query)
    jornada = cursor.fetchall()
    message = '' 
    

    conn.close()
    return render_template("modifica_contrato.html", message=message, jornada=jornada, sexo=sexos, carrera_can=datos8, empleados=datos, can_habs=datos1, can_idis=datos2, can_acas=datos6, habs=datos3, idiomas=datos4, nivel_academico=datos7, ecivil=datos5, areas=datos9, puestos=datos10, datoscontrato=datos13)


@app.route('/modifica_contrato/state/<get_state>')
def statebycountrymod_contrato(get_state):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM jordesc WHERE IdJornada = %s", [get_state])
    state = cur.fetchall()  
    stateArray = []
    for row in state:
        stateObj = {
                'iddesc': row['iddesc'],
                'name': row['name']}
        stateArray.append(stateObj)
    return jsonify({'statecountry' : stateArray})



@app.route('/agr_nvo_contrato/<string:val>', methods=['GET', 'POST'])
def agr_nvo_contrato(val):
    if request.method == 'POST':
        aux_curp = request.form['curp']
        aux_puesto= request.form['idpuesto']
        aux_area= request.form['id_area']
        aux_salario=request.form['salario']
        aux_diapaga = request.form['diapaga']
        aux_dateini = request.form['fecha_inicio']
        aux_dateend = request.form['fecha_fin']
        aux_jor = request.form['country']
        aux_hsemana= request.form['state']
        aux_horario = request.form['dias']
        aux_diafirma=request.form['fecha_inicio']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(
                "INSERT INTO contrato (Curp, idPuesto, idArea, fecha_inicio, fecha_fin, idJornada, horas_semana, horario,Salario,dias_de_pago,fecha_firma) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        ,(aux_curp,aux_puesto,aux_area,aux_dateini,aux_dateend,aux_jor,aux_hsemana,aux_horario,aux_salario,aux_diapaga,aux_diafirma))
        mysql.connection.commit()

        cur.execute('UPDATE `empleado` SET `ContratoTemporal_Val` = %s'
                    'WHERE  Curp = %s',(val,aux_curp)

        )
        mysql.connection.commit()
        cur.close()

       
        return redirect(url_for('contrato'))
        
@app.route('/editar_contrato/<string:id>', methods=['POST'])
def editar_contrato(id):
    if request.method == 'POST':
        aux_curp = request.form['curp']
        aux_puesto= request.form['idpuesto']
        aux_area= request.form['id_area']
        aux_salario=request.form['salario']
        aux_diapaga = request.form['diapaga']
        aux_dateini = request.form['fecha_inicio']
        aux_dateend = request.form['fecha_fin']
        aux_jor = request.form['country']
        aux_hsemana= request.form['state']
        aux_horario = request.form['dias']
        aux_diafirma=request.form['fecha_inicio']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute( 'Update contrato set Curp=%s, idPuesto=%s, idArea=%s, fecha_inicio=%s, fecha_fin=%s, idJornada=%s, horas_semana=%s, horario=%s, Salario= %s, dias_de_pago=%s, fecha_firma = %s where idContrato=%s'
                                            ,(aux_curp,aux_puesto,aux_area,aux_dateini,aux_dateend,aux_jor,aux_hsemana,aux_horario,aux_salario,aux_diapaga,aux_diafirma,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('contrato'))

@app.route('/bo_contrato/<string:Curp>/<string:val>/<string:id>')
def bo_contrato(Curp,val,id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='r_humanos')
    cursor = conn.cursor()
    cursor.execute('UPDATE `empleado` SET `ContratoTemporal_Val` = %s'
            'WHERE  Curp = %s',(val,Curp))
    conn.commit()

    cursor.execute(' delete from contrato where Curp = %s',(Curp))
    conn.commit()
    conn.close()
    return redirect(url_for('contrato'))










if __name__ == "__main__":
    app.run(debug=True, port=5000)