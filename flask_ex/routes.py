from flask import render_template, flash, redirect, url_for, request
from flask_ex import app, db
from flask_ex.fill_ins import LoginForm, RegisterForm, RegisterPokemonForm, AddTrainingSession
from flask_login import login_required, current_user, login_user, logout_user
from flask_ex.models import Trainer, Pokemon, Session
from werkzeug.urls import url_parse
from datetime import datetime, timedelta

@app.route('/')
@app.route('/index')
def index():
    #TODO: make this screen more interesting,
    ##add links to competitive forums or recommend pokemon to train
    return render_template("home.html")

@app.route('/trainer/<trainername>')
@login_required
def trainer(trainername):
    #TODO: convert url to /trainer/<id> when you implement trainer numbers
    #TODO: animate a count down for session
    if current_user.is_authenticated and current_user.username == trainername:
        user = Trainer.query.filter_by(username = trainername).first_or_404()
        pokemon = Pokemon.query.filter_by(trainer = user.username).all()
        sessions = Session.query.filter_by(trainer = user.username).all()
        return render_template("trainer.html",trainer = user ,pokemon = pokemon, sessions = sessions)
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('trainer', trainername = current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = Trainer.query.filter_by(username=form.username.data).first()
        if user is None or not user.comp_pw(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('trainer', trainername = user.username)
        return redirect(next_page)
    return render_template("login.html", title = "Trainer Login", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register_trainer', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = Trainer(username=form.username.data)
        user.hash_pw(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered pokemon trainer!')
        return redirect(url_for('login'))
    return render_template('register_trainer.html', title='Register', form=form)

@app.route('/trainer/<trainername>/register_pokemon', methods = ['GET','POST'])
@login_required
def register_pokemon(trainername):
    #TODO: compensate for fleshed out pokemon model
    user = Trainer.query.filter_by(username = trainername).first_or_404()
    form = RegisterPokemonForm()
    if form.validate_on_submit():
        '''
        TODO: Make this cleaner
        Order of attributes: 
        id, nickname, species, level, trainer
        ev_hp, ev_attack, ev_spattack
        ev_defecne, ev_spdefence, ev_speed
        pokerus, in_session
        '''
        poke = Pokemon(trainer = trainername, \
                       nickname = form.nickname.data, \
                       species = form.species.data, \
                       level = form.level.data, \
                       ev_hp = 0,\
                       ev_attack = 0,\
                       ev_spattack = 0,\
                       ev_defence = 0,\
                       ev_spdefence = 0,\
                       ev_speed = 0,\
                       pokerus = form.pokerus.data,\
                       in_session = False)
        db.session.add(poke)
        db.session.commit()
        return redirect(url_for('trainer', trainername = trainername))
    return render_template('registerpoke.html', title = "Register Pokemon", form = form)

@app.route('/trainer/<trainername>/<pokenickname>')
@login_required
def pokemon(trainername, pokenickname):
    #TODO: Add pokemon details to this page, calculate stats and EV/IV changes
    if current_user.is_authenticated and current_user.username == trainername:
        poke = Pokemon.query.filter_by(nickname = pokenickname, trainer = trainername).first_or_404()
        return render_template("pokemon.html", pokemon = poke)
    return redirect(url_for('login'))

@app.route('/trainer/<trainername>/add_session', methods = ['GET', 'POST'])
@login_required
def add_session(trainername):
    #TODO: make it so that pokemon currently in a session cannot be chosen
    form = AddTrainingSession()
    pokemon = Pokemon.query.filter_by(trainer = trainername).all()
    form.pokemon.choices = [(p.nickname, p.nickname) for p in pokemon]
    if form.validate_on_submit():
        new_session = Session(pokemon = form.pokemon.data,\
                          times_start = datetime.now(),\
                              times_end = datetime.now() + timedelta(hours = form.s_length.data),\
                          sess_length = form.s_length.data,\
                          trainer = trainername)
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('trainer', trainername = trainername))
    return render_template("add_session.html", title = "Add Training Session", form = form)
