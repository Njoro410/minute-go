from crypt import methods
from unicodedata import category
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from app.forms import UpdateProfile
from app.models import Pitches, User, Comments
from . import db,photos


views = Blueprint('views', __name__)


@views.route('/')
def index():

    return render_template('index.html')


@views.route('/pitches', methods=['GET', 'POST'])
@login_required
def pitches():
    users = User.query.all()
    pitches = Pitches.get_pitches()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('pitch')
        category = request.form.get('catselect')

        new_pitch = Pitches(title=title, content=content,
                            user_id=current_user.id, categories_id=category)
        new_pitch.save_pitch()
    return render_template('pitches.html', users=users, user=current_user, pitches=pitches)


@views.route('/pitch/<int:id>')
def single_pitch(id):
    pitch = Pitches.query.get(id)

    return render_template('pitch.html', pitch=pitch, user=current_user)


@views.route('/pitch', methods=['GET', 'POST'])
def comments():
    comments = Comments.get_comment()
    if request.method == 'POST':
        comment = request.form.get('comment')

        new_comment = Comments(
            comment=comment, user_id=current_user.id, pitch_id=id)
        new_comment.save_comment()
    return render_template('pitch.html', comment=comments)


@views.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@views.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@views.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('views.profile',uname=uname))