from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Credential
from app.main.forms import CredentialForm, EditProfileForm, EditCredentialForm, DeleteCredentialForm
from datetime import datetime
from dateutil import tz
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
        credential = Credential(username=form.username.data, password=form.password.data, comments=form.comments.data, owner=current_user)
        db.session.add(credential)
        db.session.commit()
        flash('Your credential is saved!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    credentials = current_user.get_credentials().paginate(
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
    credentials = user.credentials.order_by(Credential.established.desc()).paginate(
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

@bp.route('/edit_credential/<id>', methods=['GET', 'POST'])
@login_required
def edit_credential(id):
    credential = Credential.query.filter_by(id=id).first_or_404()
    form = EditCredentialForm(credential.username, credential.password, credential.comments)
    if form.validate_on_submit():
        credential.username = form.username.data
        credential.password = form.password.data
        credential.established = datetime.utcnow()
        db.session.commit()
        flash('You changes have been saved.')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = credential.established
        utc = utc.replace(tzinfo=from_zone)
        form.username.data = credential.username
        form.password.data = credential.password
        form.comments.data = credential.comments
        form.established.data = utc.astimezone(to_zone)
    return render_template('edit_credential.html', title='Edit Credential', form=form)

@bp.route('/delete_credential/<id>', methods=['GET', 'POST'])
@login_required
def delete_credential(id):
    credential = Credential.query.filter_by(id=id).first_or_404()
    form = DeleteCredentialForm()
    if form.validate_on_submit():
        db.session.delete(credential)
        db.session.commit()
        flash('You credential have been deleted.')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = credential.established
        utc = utc.replace(tzinfo=from_zone)
        form.username.data = credential.username
        form.password.data = credential.password
        form.comments.data = credential.comments
        form.established.data = utc.astimezone(to_zone)
    return render_template('delete_credential.html', title='Delete Credential', form=form)
