from django.forms import ModelForm, models
from wtforms import BooleanField, HiddenField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from . models import *

class CreateRoomForm(ModelForm):
    # room_name = StringField('Room name', validators=[DataRequired()])
    # password = PasswordField('Password')
    # public = SelectField('Public', coerce=lambda x: x == 'Yes',
    #                      choices=[('No'), ('Yes')])
    # guest_limit = SelectField('Guest limit', coerce=int,
    #                           choices=[(0, 'None'), (2, '2'), (3, '3'),
    #                                    (5, '5'), (10, '10')])
    # submit = SubmitField('Create')
    class Meta:
        model = Room
        exclude = ['slug','created','active']
    


class JoinRoomForm(ModelForm):
    class Meta:
        model = Client
        exclude = ['uuid','room_id','seen']
