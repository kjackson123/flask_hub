from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Length

class EnterIPForm(FlaskForm):
    ipaddress = StringField( validators=[DataRequired(),Length(min=2,max=20)])
    
    submit= SubmitField ( 'Connect to Device' )
    
    
 
#class ViewExistingIP(FlaskForm):
    