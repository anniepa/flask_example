from flask_ex import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Trainer(UserMixin, db.Model):
    #TODO: maybe flesh out which game the Trainer is playing?
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    pw_hash = db.Column(db.String(128))

    def hash_pw(self, pw):
        self.pw_hash = generate_password_hash(pw)

    def comp_pw(self, pw):
        return check_password_hash(self.pw_hash, pw)
        
    def __repr__(self):
        return '<Trainer {}>'.format(self.username)   


class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pokemon = db.Column(db.String(140), db.ForeignKey('pokemon.nickname'))
    times_start = db.Column(db.DateTime)
    times_end = db.Column(db.DateTime)
    sess_length = db.Column(db.Integer)
    trainer = db.Column(db.String(64), db.ForeignKey('trainer.username'))

    def __repr__(self):
        return '<Session for {}>'.format(self.pokemon)

class Pokemon(db.Model):
    #TODO: Flesh out for specific stats, include base and IVs
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(140), index = True, unique = True)
    species = db.Column(db.String(64))
    level = db.Column(db.String(64))
    trainer = db.Column(db.String(64), db.ForeignKey('trainer.username'))
    ev_hp = db.Column(db.Integer)
    ev_attack = db.Column(db.Integer)
    ev_spattack = db.Column(db.Integer)
    ev_defence = db.Column(db.Integer)
    ev_spdefence = db.Column(db.Integer)
    ev_speed = db.Column(db.Integer)
    pokerus = db.Column(db.Boolean)
    in_session = db.Column(db.Boolean)
    
    def __repr__(self):
        return '<{0} : {1}>'.format(self.species, self.nickname)

@login.user_loader
def load_trainer(id):
    return Trainer.query.get(int(id))
