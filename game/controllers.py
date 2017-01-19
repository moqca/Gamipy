import json
from flask import render_template, redirect
from flask import request
from flask import url_for
from sqlalchemy import desc

from game import app, db
from models import Game, Metric, Action, Leaderboard, Agent, AgentData, BoardParticipant, GameRecords, Coins
from forms import GameForm, MetricForm, ActionForm, LeaderForm, ParticipantForm, UpdateForm

@app.errorhandler(404)
def not_found(error):
    return render_template('404.hmtl'), 404


@app.route('/')
@app.route('/index')
def index():
    games = Game.query.all()
    return render_template('show_all.html', games=games)


@app.route('/game/add', methods=['GET', 'POST'])
def game_add():
    game = Game()
    form = GameForm(request.form)

    if request.method == 'POST':
        game = Game(gamename=form.gamename.data,
                    gamedescription=form.gamedescription.data,
                    gameid=form.gamename.data.replace(" ", "_"),
                    status='Active')

        db.session.add(game)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_game.html', form=form)


@app.route('/game/<string:id>')
def view_game(id):
    game = Game.query.get(id)
    metricform = MetricForm(request.form, fk_gamename=game.gameid)
    return render_template('show_game.html', game=game, metricform=metricform)


@app.route('/game/<string:id>/config')
def config_game(id):
    game = Game.query.get(id)
    metricform = MetricForm(request.form, fk_gamename=game.gameid)

    return render_template('config_game.html', game=game, metricform=metricform)


@app.route('/game/metric/add', methods=['GET', 'POST'])
def metric_add():
    form = MetricForm(request.form)

    if request.method == 'POST':
        metric = Metric(metricname=form.metricname.data,
                        fk_gamename=form.fk_gamename.data,
                        type=1,
                        fromdb=form.fromdb.data,
                        metric_id=form.metricname.data.replace(' ', '_'))

        db.session.add(metric)
        db.session.commit()
    return redirect(url_for('view_game', id=form.fk_gamename.data))


@app.route('/delete/action/<int:id>', methods=['POST'])
def delete_action(id):
    action = Action.query.filter_by(actionid=id)
    action.delete()
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/game/action/add', methods=['GET', 'POST'])
def action_add():
    action = Action()
    form = ActionForm(request.form)
    do_dir = {'Add': 1, 'Substract': 2, 'Null': 3}
    actiondo = do_dir[request.form['actiondo']]
    if request.method == 'POST':
        action = Action(actionname=form.actionname.data,
                        fk_belongs=form.fk_belongs.data,
                        actiondescription=form.actiondescription.data,
                        actiondo=actiondo,
                        amount=form.amount.data,
                        )

        db.session.add(action)
        db.session.commit()
    return redirect(url_for('view_game', id=form.gamename.data))





@app.route('/slot/result', methods=['POST'])
def post_result():
    coin = int(request.form['money'])
    points = int(request.form['points'])
    agent = request.form['agent']

    coins = Coins.query.filter_by(agent=agent).first()

    coins.points += points
    coins.amount = coin

    db.session.commit()

    return redirect(url_for('apps_view'))


@app.route('/player/<int:id>')
def agent_view(id):
    agent = Agent.query.get(id)
    games = db.session.query(Leaderboard).filter(Leaderboard.boardid == BoardParticipant.board).filter(
        BoardParticipant.agent == id)

    return render_template('show_agent.html', agent=agent, games=games)
    pass


def debug():
    assert current_app.debug == False


@app.route('/game/board/<int:id>')
def board_view(id):
    board = Leaderboard.query.get(id)
    participating = db.session.query(Agent, BoardParticipant) \
        .filter(Agent.id == BoardParticipant.agent) \
        .filter(Agent.inboard.any(BoardParticipant.board == id)) \
        .order_by(desc(BoardParticipant.points))

    games = db.session.query(Game).filter(Game.gameid == Leaderboard.measureboard).filter(Leaderboard.boardid==id)

    agents = (Agent.query.filter(Agent.position.any(AgentData.lob == board.userselection))
              .filter_by(status='Activo')
              .filter(Agent.position.any(AgentData.type == 'Agent'))
              .filter(~Agent.inboard.any(BoardParticipant.board == 1))

              )

    return render_template('show_board.html', board=board, agents=agents,
                           participating=participating,
                           enumerate=enumerate,
                           game=games)
    pass


@app.route('/game/board/add/agent', methods=['POST'])
def board_add_agent():
    form = ParticipantForm(request.form)
    participant = BoardParticipant(agent=form.agent.data,
                                   board=form.board.data,
                                   points=0)

    db.session.add(participant)
    db.session.commit()

    return redirect(url_for('board_view', id=form.board.data))


@app.route('/game/board/add', methods=['POST'])
def board_add():
    form = LeaderForm(request.form)

    scopedir = {'Game': 1}
    scope = scopedir[form.scope.data]

    perioddir = {'Day': 1, 'Week': 2, 'Month': 3, 'Year': 4}
    period = perioddir[form.peridiocity.data]

    if request.method == 'POST':
        board = Leaderboard(boardname=form.boardname.data,
                            boarddescription=form.boarddescription.data,
                            measureboard=form.gamename.data,
                            scope=scope,
                            userscope=form.userscope.data,
                            peridiocity=period,
                            requirement=form.requirement.data,
                            userselection=form.userselection.data
                            )
        db.session.add(board)
        db.session.commit()

    return redirect(url_for('view_game', id=form.gamename.data))


@app.route('/board/update/agent', methods=['POST'])
def board_update_value():
    update = UpdateForm(request.form)

    new_record = GameRecords(board=update.board.data,
                             agent=update.agent.data,
                             metricid=update.metric.data,
                             amount=update.points.data)

    db.session.add(new_record)
    db.session.commit()


    return redirect(url_for('agent_view', id=update.agent.data))


@app.route('/apps')
def apps_view():
    agent = Agent.query.get(2978)
    return render_template('gamelist.html', agent=agent)

@app.route('/slot')
def play_slot():
    agent = 2978
    coins = Coins.query.filter_by(agent=agent).first()
    return render_template('index.html', coins=coins.amount, agent=coins.agent)


