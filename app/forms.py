from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment',validators=[Required()])
    submit = SubmitField('Submit')
