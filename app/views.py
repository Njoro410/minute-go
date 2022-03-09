from crypt import methods
from nis import cat
from unicodedata import category
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from app.forms import CommentForm, UpdateProfile
from app.models import Categories, Pitches, User, Comments
from . import db, photos


views = Blueprint('views', __name__)


@views.route('/')
def index():

    return render_template('index.html')


@views.route('/pitches', methods=['GET', 'POST'])
@login_required
def pitches():
    pitches = Pitches.get_pitches()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('pitch')
        category = request.form.get('catselect')

        new_pitch = Pitches(title=title, content=content,
                            user_id=current_user.id, categories_id=category,likes = 0, dislikes = 0)
        new_pitch.save_pitch()
        return redirect(request.referrer)

    return render_template('pitches.html', user=current_user, pitches=pitches)


@views.route('/pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def single_pitch(id):
    pitch = Pitches.query.get(id)
    coms = Comments.get_comments(id)

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.content.data

        new_comment = Comments(
            comment=comment, user_id=current_user.id, pitch_id=id)

        new_comment.save_comment()
        return redirect(request.referrer)

    return render_template('pitch.html', user=current_user, pitch=pitch, comment_form=comment_form, comments=coms)


@views.route('/user/<uname>/<id>')
def profile(uname,id):
    user = User.query.filter_by(username=uname).first()
    pitch = Pitches.query.filter_by(user_id=id).all()


    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user,pitches = pitch)


@views.route('/user/<uname>/<id>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname,id):
    user = User.query.filter_by(username=uname,id=id).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username,id=user.id))

    return render_template('profile/update.html', form=form)


@views.route('/user/<uname>/<id>/update/pic', methods=['POST'])
@login_required
def update_pic(uname,id):
    user = User.query.filter_by(username=uname,id=id).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('views.profile', uname=uname, id=id))


@views.route('/category/<id>')
@login_required
def category(id):
    pitch = Pitches.query.filter_by(categories_id=id).all()
    cat = Categories.query.filter_by(id=id).first()
    
    return render_template('category.html', pitches=pitch, category=cat)
