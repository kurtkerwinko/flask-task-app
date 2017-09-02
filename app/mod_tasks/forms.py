from wtforms import Form, StringField, TextAreaField, validators

class TaskForm(Form):
  title       = StringField('Title', [validators.InputRequired(), validators.Length(max=80)])
  description = TextAreaField('Description', [validators.InputRequired()])
