from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_ex.models import Trainer

'''
Forms
'''

class LoginForm(FlaskForm):
    #TODO: Trainer ID number
    username = StringField("TrainerID", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log me in, Rotom!")

class RegisterForm(FlaskForm):
    #TODO: Trainer ID number
    username = StringField('TrainerID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register me, Rotom!')

    def validate_username(self, username):
        user = Trainer.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class RegisterPokemonForm(FlaskForm):
    #TODO: SelectField for pokemon species, maybe rely on data mine from other websites?
    species = StringField("Pokemon Species", validators = [DataRequired()])
    nickname = StringField("Pokemon Nickname")
    level = StringField("Pokemon Level", validators = [DataRequired()])
    pokerus = BooleanField("Pokerus?")
    submit = SubmitField("Register Pokemon")

class AddTrainingSession(FlaskForm):
    #TODO: Convert session length to language in the SwSh game
    pokemon = SelectField("Pokemon Nickname", validators = [DataRequired()])
    ev = SelectField("EV to Train", validators = [DataRequired()],\
                     choices = [("hp", "HP"), ("att", "Attack"), ("spatt", "Special Attack"),\
                                ("def", "Defence"), ("spdef", "Special Defence"), ("spe", "Speed")])
    s_length = IntegerField("Length of Session in Hours", validators = [DataRequired()])
    submit = SubmitField("Add Session")
