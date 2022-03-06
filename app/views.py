from crypt import methods
from unicodedata import category
from flask import Blueprint,render_template,abort,request
from flask_login import login_required, current_user
from app.models import Pitches, User
from . import db


views = Blueprint('views',__name__)

@views.route('/')
def index():

    return render_template('index.html')

@views.route('/pitches',methods = ['GET','POST'])
@login_required
def pitches():
    users = User.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('pitch')
        category = request.form.get('catselect')

        new_pitch = Pitches(title = title,content = content,user_id = current_user.id,categories_id = category)
        new_pitch.save_pitch()
    return render_template('pitches.html',users=users, user = current_user)
        

    