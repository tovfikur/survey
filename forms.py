from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField, TelField # can be accessed under the wtforms.fields.html5 namespace

class LoginForm(FlaskForm):
    name = StringField('Name:', id='name')
    phone = TelField('Phone Number:', id='name')
    damage = StringField('Name:', id='name')
    thana = StringField('Name:', id='name')
    address = StringField('Name:', id='name')
    zilla = StringField('Name:', id='name')
    details = StringField('Name:', id='name')
    proof = StringField('Name:', id='name')