from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(30), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitches', backref='user', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    pitches = db.relationship('Pitches', backref='categories', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Pitches(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(150))
    posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    # category = db.relationship('Categories', backref='user', lazy="dynamic")

    def __repr__(self):
        return f'User {self.content}'

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls):
        pitches = Pitches.query.all()
        return pitches


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def __repr__(self):
        return f'User {self.content}'

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    



