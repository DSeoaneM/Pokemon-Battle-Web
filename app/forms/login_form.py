from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TrainerLoginForm(FlaskForm):
    trainer_name = StringField("Trainer: ", validators=[
        DataRequired(message="Trainer's name is mandatory"),
        Length(min=3, max=15, message="Trainer's name length is invalid. It should be between 3 and 15 characters")
    ])
    submit = SubmitField("Submit")
