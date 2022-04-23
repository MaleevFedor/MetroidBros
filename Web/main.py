import os
from datetime import timedelta

from flask import Flask, render_template, make_response, redirect, session,\
    send_file, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.user_class import User
from forms import LoginForm, RegisterForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    days=31
)
app.config['DOWNLOAD_GAME_PATH'] = f'{os.getcwd()}\Download\Game\DinoMight.zip'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfJ75IeAAAAADHld1mi9lW-uCMBkZT0PTNnsLx9'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfJ75IeAAAAANTfinH4snDS7flzeoAmP963clPI'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/login_users")


# Game-stats functions
@app.route('/stats', methods=['POST'])
def update_stats():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter((User.email == request.json['user']) | (User.login == request.json['user'])).first()
    user.kills += request.json['kills']
    user.deaths += request.json['deaths']
    user.wins += request.json['wins']
    user.hp_healed += request.json['hp']
    user.loses += request.json['loses']
    user.shots += request.json['shots']
    user.hits += request.json['hits']
    db_sess.commit()
    return 'ok'


@app.route('/game_login', methods=['POST'])
def game_login():
    if db_check_password(request.json['login'], request.json['password']):
        return 'ok'
    return 'not ok'


def db_check_password(login, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == login).first()
    if user and user.check_password(password):
        return True


# Site functions
@login_manager.user_loader
def load_user(user):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user)


@app.route('/')
def welcome_page():
    if current_user.is_authenticated:
        return redirect('/mainpage')
    return render_template('welcome.html')


@app.route('/mainpage', methods=['GET', 'POST'])
@login_required
def main_page():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    return render_template('mainpage.html', form=form)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.email.data) | (User.login == form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/mainpage")
        return render_template('login.html',
                               message="Incorrect login or password", form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/download')
@login_required
def download_game():
    redirect('/mainpage')
    return send_file(app.config['DOWNLOAD_GAME_PATH'])


@app.route("/session_test")
@login_required
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html',
                                   form=form, message="Passwords are not the same",)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first() or \
                db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('registration.html',
                                   form=form, message="User already exists",)
        if form.about.data == '':
            form.about.data = 'No information'
        user = User(
            login=form.login.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', form=form)


@app.route('/profile/<username>')
@login_required
def search_profile(username):
    db_sess = db_session.create_session()
    if current_user.login == username or current_user.email == username:
        return redirect('/my_profile')
    found_user = db_sess.query(User).filter((User.email == username) | (User.login == username)).first()
    if found_user:
        return found_user.login
    else:
        return 'No such user'


@app.route('/my_profile')
@login_required
def my_profile():
    return 'here is your profile'


@app.route('/rating', methods=['GET', 'POST'])
@login_required
def show_rating():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    db_sess = db_session.create_session()
    user_list = []
    for user in db_sess.query(User).all():
        user_list.append(user)
    user_list = sorted(user_list, key=lambda user: user.wins + user.loses)
    user_list = sorted(user_list, key=lambda user: user.elo, reverse=True)
    context = {}
    context['users'] = []
    for i, user in enumerate(user_list):
        if i == 100:
            break
        context['users'].append({'world_ranking': i + 1, 'nickname': user.login,
                                 'matches_played': user.wins + user.loses, 'rank': f'({user.elo})'})
    return render_template('rating.html', context=context, form=form)


@app.route('/achievements')
@login_required
def show_achiv():
    return 'here will be achievements'


@app.route('/history')
@login_required
def show_history():
    return 'here will be your recent matches'


@app.route('/tournaments')
@login_required
def show_tournaments():
    return 'here maybe will be tournaments list'


@app.errorhandler(401)
def custom_401(error):
    return redirect('/')


@app.errorhandler(404)
def custom_404(error):
    return redirect('/mainpage')


if __name__ == '__main__':
    app.run("127.0.0.1", 80)
