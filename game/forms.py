from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length


class GameForm(Form):
    gamename = StringField('gamename', validators=[DataRequired()])
    gamedescription = TextAreaField('gamedescription')


class MetricForm(Form):
    metricname = StringField('metricname', validators=[DataRequired()])
    type = IntegerField('type', validators=[DataRequired()])
    fromdb = StringField('fromdb', validators=[DataRequired()])
    fk_gamename = StringField('fk_gamename')


class ActionForm(Form):
    actionname = StringField('actionname', validators=[DataRequired()])
    actiondescription = StringField('actiondescription', validators=[DataRequired()])
    fk_belongs = StringField('belongs')
    actiondo = IntegerField('actiondo', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[DataRequired()])
    gamename = StringField()


class LeaderForm(Form):
    boardname = StringField('boardname', )
    boarddescription = StringField('boarddescription')
    participants = StringField('for')
    scope = StringField('Scope')
    userscope = StringField('userscope')
    peridiocity = StringField('peridiocity')
    requirement = StringField('requirement')
    userselection = StringField('userselection')
    gamename = StringField()


class ParticipantForm(Form):
    agent = IntegerField('agent')
    board = IntegerField('board')


class UpdateForm(Form):
    board = IntegerField('board')
    agent = IntegerField('agent')
    metric = StringField('metric')
    points = IntegerField('points')
