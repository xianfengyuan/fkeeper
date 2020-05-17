from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Credential
from app.main.forms import CredentialForm, EditProfileForm
from datetime import datetime
from app.main import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CredentialForm()
    if form.validate_on_submit():
        credential = Credential(username=form.username.data, owner=current_user)
        db.session.add(credential)
        db.session.commit()
        flash('Your credential db is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    credentials = current_user.credentials().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('main.index', page=credentials.next_num) \
        if credentials.has_next else None
    prev_url = url_for('main.index', page=credentials.prev_num) \
        if credentials.has_prev else None
    return render_template('index.html', title='Home', form=form, credentials=credentials.items,
        next_url=next_url, prev_url=prev_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    credentials = user.credentials.order_by(Credential.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=credentials.next_num) \
        if credentials.has_next else None
    prev_url = url_for('main.user', username=user.username, page=credentials.prev_num) \
        if credentials.has_prev else None
    return render_template('user.html', user=user, credentials=credentials.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('You changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
