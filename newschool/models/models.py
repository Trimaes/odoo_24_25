# -*- coding: utf-8 -*-

from odoo import models, fields, api

#PARA GENERAR CONTRASEÑAS ALEATORIAS
import secrets

#VALIDATION ERRORS
from odoo.exceptions import ValidationError

#  -----USO DE loggs: ----------------------------
# | odoo -u newschool -d proves --log-level=debug |
#  -----------------------------------------------
import logging
_logger = logging.getLogger(__name__)

#EXPRESIONES REGULARES
import re

#  ---------------------------------------------------------------------------------------------
# |                                        COMENTARIOS                                          |
# |                                                                                             |
#  ---------------------------------------------------------------------------------------------


class student(models.Model):
    #HERENCIA DE CLASE -> ya no se necesita: _description, name. Sólo hay que dejar los fields que NO existan ya en res.partner
    _name = 'res.partner' #------------ IMPORTANTE
    _inherit = 'res.partner' #---------------------------------- SE NECESITA PARA QUE FUNCIONE LA HERENCIA
    #_description = 'newschool.student' #------------ IMPORTANTE
    
    # ----- ACTIONS -----
    def open_student(self):
        for s in self:
            action = self.env.ref('newschool.action_student_modal').read()[0]
            action['res_id'] = s.id
            # Mostrar acciones de tipo WINDOW:
            return action
            # --> return {
                # Mostrar action tipo URL:
            # -->     "type" : "ir.actions.act_url",
            # -->     "url" : "http://odoo.com",
                # El targer puede ser self o new
            # -->     "target" : "self",
            # --> }
            
    # ----- print en CRON -----
    @api.model
    def cron(self):
        print(self._name)
        
    # ----- SERVER ACTION -----
    @api.model
    # Si se usa records = self.browse(self._context.get('active_ids')) no incluir records como parámetro
    def server_action_students(self,records):
        #records = self.browse(self._context.get('active_ids'))
        for r in records:
            print(r)
    
    #  ---------------------------------------------------------------------------------------------    
    # | string -> da un nombre al field, si no se define se coge el nombre de la variable           |
    # | Se aconseja poner el atributo string y help aunque no es estrictamente necesario            |
    # | ES IMPORTANTTE SIEMPRE TENER UN FIELD CON EL NOMBRE -> name                                 |
    #  ---------------------------------------------------------------------------------------------
    
    #name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    level = fields.Selection([('1','1'),('2','2')])
    
    birth_year = fields.Integer()
    description = fields.Text()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    state = fields.Selection([('1','Enrolled'),('2','Student'),('3','Ex-student')], default='1')
    
    #  ----- IMAGES ------------------------------------------------------------------------------------------------
    # |                                                                                                             |
    # | photo = fields.Binary() -> RECOMENTBLE USAR: fields.Image()                                                 |
    # | SE NECESITA UN WIDGET IMAGE EN LA VISTA PARA VISUALIZAR LA FOTO                                             |       
    # |                                                                                                             |
    # |----- IMAGEN DEFAULT ----------------------------------------------------------------------------------------|
    # |                                                                                                             |
    # | ---> def _get_default_image(self):                                                                          |
    # | --->     return self.env.ref('id_modelo').photo -> Ej ID: newschool.student12345678C                        |
    # |                                                                                                             |
    # | ---> photo = fields.Image(default=_get_default_image, max_width=200, max_height=200)                        |
    # |                                                                                                             |
    # |----- IMAGEN DEFAULT DESDE UNA IMAGEN GUARDADA EN EL DIRECTORIO STATIC --------------------------------------|
    # |                                                                                                             |
    # | 1- Crear el directorio static en la carpeta del modulo.                                                     |
    # | 2- Dentro de static crear el dicectorio src y dentro de src dejar el archivo .jpg                           |
    # |                                                                                                             |
    # | ---> def _get_default_image(self):                                                                          |
    # | --->     with open(modules.get_module_resource('newschool','static/src','imagen.jpg'),'rb') as f:           |
    # | --->        img = f.read()                                                                                  |
    # | --->        return base64.b64encode(imagen)                                                                 |
    # |                                                                                                             |
    # |----- IMAGEN DEFAULT ONCHANGE DESDE UNA IMAGEN GUARDADA EN EL DIRECTORIO STATIC -----------------------------|
    # |                                                                                                             |
    # | ---> tipo = fields.Selection([('1','Tipo1'),('2','Tipo2'),('3','Tipo3')])                                   |
    # |                                                                                                             |
    # |      @api.onchange('tipo')                                                                                  |
    # | ---> def _get_default_image(self):                                                                          |
    # | --->     nombre_img = str(self.tipo) + '.jpg'                                                               |
    # | --->     with open(modules.get_module_resource('newschool','static/src',nombre_img),'rb') as f:             |
    # | --->        img = f.read()                                                                                  |
    # | --->        self.photo = base64.b64encode(img)                                                              |
    # |                                                                                                             |
    # -------------------------------------------------------------------------------------------------------------
    
    photo = fields.Image(max_width=200, max_height=200)

    #  ----- FIELDS RELACIONALES -----------------------------------------------------------------------------
    # |                                                                                                       |
    # | Many2One se debe especificar el nombre de la clase a la que se hace referencia (classroom)            |
    # | ondelete -> 'set null', 'restrict', 'cascade' / SI NO SE INCLUYE ondelete POR DEFECTO ES 'set null'   |
    # | classroom = fields.Many2one('newschool.classroom')                                                    |
    # |                                                                                                       |
    #  -------------------------------------------------------------------------------------------------------
    #  ----- FILTROS - domain ---------------------------------------------------------------------------------------------------------------------
    # |                                                                                                                                            |
    # | domain -> tupla -> 1rCampo: Nombre del field 'remoto'(el de classoom), 2oCampo: Operador, 3rcampo: Field de la clase actual(el de student) |
    # | domain="[('level','=',level)]"                                                                                                             |
    # | EL DOMAIN TABIÉN PUEDE ESTAR EN LA VISTA                                                                                                   |
    # |                                                                                                                                            |
    #  --------------------------------------------------------------------------------------------------------------------------------------------
    classroom = fields.Many2one(comodel_name='newschool.classroom', ondelete='set null', help = 'La clase a la que va el alumno')
    
    #  ---------------------------------------------------------------------------------------------------------------------------------------------
    # | Obtener la lista de profesores del estudiante sin crear una nueva relación, aprovechando la relación que                                    |    
    # | No se guarda en la BBDD sólo en le modelo                                                                                                   |
    # | ya existe entre la classroom y teacher (para evitar la redundancia en la BBDD)                                                              |
    # | En el related se especifica el modelo y el atributo (que contiene la relación) al que se refiere -> classroom.teachers                      |
    # | IMPORTANTE -> El field de destino del related ha de ser igual al tipo de field desde el que se invoca Many2many a un Many2Many por ejemplo  |
    #  ---------------------------------------------------------------------------------------------------------------------------------------------
    teachers = fields.Many2many(comodel_name='newschool.teacher', related='classroom.teachers', readonly=True)
    
    #----- CONSTRAINTS -----
    dni = fields.Char(string='DNI')
    
    @api.constrains('dni')
    def _chec_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z',re.I)
        for s in self:
            if regex.match(s.dni):
                _logger.info('El dni hace match')
            else:
                raise ValidationError('El DNI no es válido')
    
    #CONSTRAINTS SQL ---> 1rParámetro: Nombre que asignamos a la constraint, 2oParámetro: Constraint sql y attr, 3rParámetro: Mensaje
    _sql_constraints = [('dni_unique', 'unique(dni)', 'Este DNI ya existe')]
    
    #  ----- ONCHANGE --------------------------------------------------------------------------------------
    # |                                                                                                     |
    # | {'warning' : {'title':'Bad birth year','message':'The student is too young','type':'notification'}} |
    # | - Los campos que son computed y tienen un depends ya tienen un onchange implícito.                  |
    # |                                                                                                     |
    #  -----------------------------------------------------------------------------------------------------
    @api.onchange('birth_year')
    def _onchange_year(self):
        if self.birth_year >2030:
            self.birth_year = 2000
            return {'warning' : {'title':'Bad birth year','message':'The student is too young'}}
        
    @api.onchange('level')
    def _onchange_level(self):
        return {
            'domain' : {'classroom' : [('level','=',self.level)]}
            }
        
    
    #----- BUTTON Functions -----
    def regenerate_password(self):
        for s in self:
            password = secrets.token_urlsafe(12)
            s.write({'password':password})
                 
    #  ----- FIELDS DEFAULT -------------------------------------------
    # | Default 'computado'                                            |
    # | No necesita for                                                |
    # |                                                                |
    # | --->def _get_password(self):                                   |
    # | --->    print('\033[35m',self,'\033[0m')                       | 
    # | --->    password = secrets.token_urlsafe(12)                   | 
    # | --->    _logger.warning('\033[35m'+str(password)+'\033[0m')    | 
    # | --->    return password                                        | 
    # |                                                                | 
    # | --->password = fields.Char(default=_get_password)              | 
    #  ----------------------------------------------------------------
    
    enrollment_date = fields.Datetime(default= lambda self: fields.Datetime.now())
    
    #Con lambda:
    password = fields.Char(default=lambda s: secrets.token_urlsafe(12))
    
    #  ----- FIELDS COMPUTE ------------------------------------------------------------------------
    # |                                                                                             |
    # | Para que la función sea privada el nombre de esta debe empezar con barra baja '_'           |
    # | EJEMPLO CON PASSWORD                                                                        |
    # |                                                                                             |
    # | CODE --------> password = fields.Char(compute='_get_password', store = True)                |
    # |                                                                                             |
    # | self es un recordset que hay que recorrer mediante el for, obteniendo cada singleton        |
    # | print como opcion de 'debugging' 35m -> púrpura (ANSI) ---->  print('\033[35m',x,'\033[0m') |
    # | _logger.debug _logger.info _logger.warning                                                  |
    # | s -> singleton de student                                                                   |
    # |                                                                                             |
    # | CODE --------> @api.depends('name')                                                         |
    # |                                                                                             |
    # | CODE --------> def _get_password(self):                                                     |
    # | CODE -------->     #print(self)                                                             |
    # | CODE -------->     for s in self:                                                           |
    # | CODE -------->         #print('\033[35m',s,'\033[0m')                                       |
    # | CODE -------->         s.password = secrets.token_urlsafe(12)                               |
    # | CODE -------->         _logger.debug('\033[35m'+str(s)+'\033[0m')                           |
    #  ---------------------------------------------------------------------------------------------
    
class classroom(models.Model):
    _name = 'newschool.classroom'
    _description = 'Las clases'
    
    courses = fields.Many2one(comodel_name="newschool.course", inverse_name="classrooms")
    
    name = fields.Char()
    level = fields.Selection([('1','1'),('2','2')])
    
    # ----------------------------------------------------------------------------------------------------
    #| One2Many se declara como un field pero no se guarda en la base de datos, es una consulta a la BBDD |
    #| Se debe indicar el modelo o clase (comodel_name) a la que se hace referencia                       |
    #| y la clave ajena (inverse_name) (field que hace referencia -> 'classroom' de la clase student)     |
    # ----------------------------------------------------------------------------------------------------
    students = fields.One2many(comodel_name='res.partner', inverse_name='classroom')
    
    #  -----------------------------------------------------------------------------------------------------
    # | Indicar el modelo con el que se relaciona                                                           |
    # | relation -> nombre de la tabla intermedia                                                           |
    # | column1 -> nombre de la columna que hace referencia al modelo actual (classroom) dentro de la tabla |
    #  -----------------------------------------------------------------------------------------------------
    teachers = fields.Many2many(comodel_name='newschool.teacher',
                                relation='teachers_classroom',
                                column1='clssoom_id',
                                column2='teacher_id')

    teachers_last_year = fields.Many2many(comodel_name='newschool.teacher',
                                relation='teachers_classroom_last_year',
                                column1='clssoom_id',
                                column2='teacher_id')
    
    #  ----- FIELDS COMPUTE RELACIONALES ----------------------------------------------------------
    # | Sólo se pueden hacer compute relacionales los Many2one y los Many2any                      |
    # | ---> delegate = fields.Many2one(comodel_name='newschool.student', compute='_get_delegate') |
    #  --------------------------------------------------------------------------------------------
    all_teachers = fields.Many2many('newschool.teacher', compute='_get_teachers')
    
    #  ---------------------------------------------
    # | s -> singleton de classroom                 | 
    # | ---> def _get_delegate(self):               |
    # | --->     for s in self:                     |
    # | --->         s.delegate = s.students[0].id  |
    #  ---------------------------------------------
    def _get_teachers(self):
        for s in self:
            s.all_teachers = s.teachers + s.teachers_last_year
    
class teacher(models.Model):
    _name = 'newschool.teacher'
    _description = 'Los profesores'
    
    name = fields.Char()
    topic = fields.Char()
    phone = fields.Char()
    
    #  ----- FIELDS RELACIONALES -----------------
    # | Indicar el modelo con el que se relaciona |
    #  -------------------------------------------
    classrooms = fields.Many2many(comodel_name='newschool.classroom',
                                  relation='teachers_classroom',
                                  column2='clssoom_id',
                                  column1='teacher_id')
    
    classrooms_last_year = fields.Many2many(comodel_name='newschool.classroom',
                                            relation='teachers_classroom_last_year',
                                            column2='clssoom_id',
                                            column1='teacher_id')
    
class seminar(models.Model):
    _name = "newschool.seminar"
    _description = "Los seminarios"
    
    name = fields.Char()
    date_start = fields.Datetime()
    date_finish = fields.Datetime()
    hours = fields.Integer()
    classroom = fields.Many2one(comodel_name='newschool.classroom', ondelete='set null', help = 'La clase')
    
class course(models.Model):
    _name = "newschool.course"
    name = fields.Char()
    
    classrooms = fields.One2many(comodel_name="newschool.classroom", inverse_name="courses")
    students = fields.Many2many('res.partner')
    enrolled_students = fields.Many2many('res.partner', compute='_get_enrolled')
    
    def _get_enrolled(self):
        for c in self:
            c.enrolled_students = c.students.filtered(lambda s: len(s.classroom) == 1)
    
class course_wizard(models.TransientModel):
    _name="newschool.course_wizard"
    
    name = fields.Char()
    classrooms = fields.Many2many(comodel_name="newschool.classroom")
    students = fields.Many2many('res.partner')
    