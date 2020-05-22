from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Credential

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, orig_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.orig_username = orig_username

    def validate_username(self, username):
        if username.data != self.orig_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class CredentialForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class EditCredentialForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired(), Length(min=1, max=140)])
    established = DateTimeField(format='%b %d %Y, %I:%M:%S %p')
    submit = SubmitField('Submit')

    def __init__(self, orig_username, orig_password, orig_comments, *args, **kwargs):
        super(EditCredentialForm, self).__init__(*args, **kwargs)
        self.orig_username = orig_username
        self.orig_password = orig_password
        self.orig_comments = orig_comments

    def validate_comments(self, comments):
        if comments.data != self.orig_comments:
            credential = Credential.query.filter_by(comments=self.comments.data).first()
            if credential is not None:
                raise ValidationError('Please use different comments.')
