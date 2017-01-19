from game import db


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cicid = db.Column(db.Text)
    lead = db.Column(db.Text)
    lxc = db.Column(db.Text)
    status = db.Column(db.Text)

    __tablename__ = 'agent_cic'


class AgentData(db.Model):
    type = db.Column(db.Text)
    lob = db.Column(db.Text)
    position = db.Column(db.Text)
    id = db.Column(db.Integer, db.ForeignKey(Agent.id), primary_key=True)

    fk_agentdi = db.relationship('Agent', backref='position')

    __tablename__ = 'dbo_position'
    __table_args_ = (
        db.PrimaryKeyConstraint('agentdi')
    )
    __table_args__ = {'schema': 'game'}


class Game(db.Model):
    gamename = db.Column(db.Text)
    gamedescription = db.Column(db.Text)
    gameid = db.Column(db.Text, unique=True, primary_key=True)
    status = db.Column(db.String)

    __tablename__ = 'gamedir'
    __table_args_ = (
        db.PrimaryKeyConstraint('gameid'),
    )
    __table_args__ = {'schema': 'game'}


class Metric(db.Model):
    metricname = db.Column(db.Text)
    type = db.Column(db.Text)
    metric_id = db.Column(db.Text, unique=True)
    metricid = db.Column(db.Integer, primary_key=True)
    fromdb = db.Column(db.String)
    fk_gamename = db.Column(db.Text, db.ForeignKey(Game.gameid))

    games = db.relationship('Game', backref='metrics')

    __tablename__ = 'metrics'
    __table_args_ = (
        db.PrimaryKeyConstraint('fk_gamename', 'metric_id'),
    )
    __table_args__ = {'schema': 'game'}



class Action(db.Model):
    actionname = db.Column(db.Text)
    actionid = db.Column(db.Integer, unique=True, primary_key=True)
    actiondescription = db.Column(db.Text)
    actiondo = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    fk_belongs = db.Column(db.Text, db.ForeignKey(Metric.metricid))

    belongs = db.relationship('Metric', backref='actions')

    __tablename__ = 'actions'
    __table_args_ = (
        db.PrimaryKeyConstraint('fk_belongs', 'actionid')
    )
    __table_args__ = {'schema': 'game'}



class Leaderboard(db.Model):
    boardname = db.Column(db.Text)
    boardid = db.Column(db.Integer, primary_key=True)
    boarddescription = db.Column(db.Text)
    scope = db.Column(db.Text)  #
    userscope = db.Column(db.Text)
    peridiocity = db.Column(db.Integer)
    requirement = db.Column(db.Text)
    userselection = db.Column(db.Text)
    measureboard = db.Column(db.Integer, db.ForeignKey(Game.gameid))
    participants = db.Column(db.Integer)

    fk_measureboard = db.relationship('Game', backref='boards')

    __tablename__ = 'leaderboard'
    __table_args_ = (
        db.PrimaryKeyConstraint('measureboard', 'boardid')
    )
    __table_args__ = {'schema': 'game'}


class BoardParticipant(db.Model):
    board = db.Column(db.Integer, db.ForeignKey(Leaderboard.boardid))
    agent = db.Column(db.Integer, db.ForeignKey(Agent.id))
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Float)

    fk_boardparticipants = db.relationship('Leaderboard', backref='participating')
    fk_agentsinboard = db.relationship('Agent', backref='inboard')

    __tablename__ = 'boardparticipant'
    __table_args_ = (
        db.PrimaryKeyConstraint('agent', 'board')
    )
    __table_args__ = {'schema': 'game'}



class GameRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, server_default=db.func.now())
    board = db.Column(db.Integer, db.ForeignKey(BoardParticipant.id))
    metricid = db.Column(db.Integer, db.ForeignKey(Metric.metricid))

    fk_recordboard = db.relationship('BoardParticipant', backref='records')

    __tablename__ = 'gamerecords'
    __table_args__ = {'schema': 'game'}


class Coins(db.Model):
    agent = db.Column(db.Integer, db.ForeignKey(Agent.id), primary_key=True)
    amount = db.Column(db.Integer)
    points = db.Column(db.Integer)

    fk_agentpoints = db.relationship('Agent', backref='coins')
    __tablename__ = 'temp_coins'
    __table_args__ = {'schema': 'game'}


