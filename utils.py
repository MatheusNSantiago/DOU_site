from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class ComentarioForm(FlaskForm):
    conteudo = StringField(validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Enviar")
    
    
