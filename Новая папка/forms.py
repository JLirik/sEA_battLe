from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    cod = StringField('Введите код для скачивания:', validators=[DataRequired()])
    download = SubmitField('Скачать')