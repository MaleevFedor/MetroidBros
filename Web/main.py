import os
from datetime import timedelta

from flask import Flask, render_template, make_response, redirect, session, \
    send_file, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.user_class import User
from Rating import ranked_emblems, check_rating, number_of_predators
from data.match_class import Match
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
    user = db_sess.query(User).filter(
        (User.email == request.json['user']) | (User.login == request.json['user'])).first()
    user.kills += request.json['kills']
    user.deaths += request.json['deaths']
    user.wins += request.json['wins']
    user.hp_healed += request.json['hp']
    user.loses += request.json['loses']
    user.shots += request.json['shots']
    user.hits += request.json['hits']
    user.saws_deaths += request.json['saws_deaths']
    db_sess.commit()
    return 'ok'


@app.route('/change_elo', methods=['POST'])
def update_elo():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        (User.email == request.json['user']) | (User.login == request.json['user'])).first()
    user.elo += request.json['elo']
    user.marksman = request.json['marksman']
    user.comeback = request.json['comeback']
    user.heal_500 = request.json['heal_500']
    user.perfect = request.json['perfect']
    db_sess.commit()
    return 'ok'



@app.route('/stats_match', methods=['POST'])
def update_match_stats():
    db_sess = db_session.create_session()
    match = Match(
            player_name=request.json['player_name'],
            kills=request.json['kills'],
            deaths=request.json['deaths'],
            hp_healed=request.json['hp'],
            saws_deaths=request.json['saws_deaths'],
            shots=request.json['shots'],
            hits=request.json['hits'],
            elo=request.json['elo'],
            results=request.json['result'],
            enemy_name=request.json['enemy_name']
        )

    user = db_sess.query(User).filter(
        (User.email == request.json['player_name']) | (User.login == request.json['player_name'])).first()
    user.elo += request.json['elo']
    if match.hits == match.shots and match.elo > 0:
        user.marksman = True
    if match.hp_healed >= 500:
        user.heal_500 = True
    if match.results == 'LLVVV':
        user.comeback = True
    if match.shots > 0:
        if match.hits / match.shots * 100 < 25:
            user.bullseye = True
    user.perfect = request.json['perfect']
    db_sess.add(match)
    db_sess.commit()
    return 'ok'


@app.route('/game_login', methods=['POST'])
def game_login():
    if db_check_password(request.json['login'], request.json['password']):
        return 'ok'
    return 'not ok'


@app.route('/player_elo', methods=['POST'])
def get_elo():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        (User.email == request.json['name']) | (User.login == request.json['name'])).first()
    return str(user.elo)


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
    return render_template('mainpage.html', form=form, Title='DinoStats')


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
    send_file(app.config['DOWNLOAD_GAME_PATH'])
    return redirect('/mainpage')


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
                                   form=form, message="Passwords are not the same")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first() or \
                db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('registration.html',
                                   form=form, message="User already exists")
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


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def search_profile(username):
    your_profile = False
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    db_sess = db_session.create_session()
    if current_user.login == username or current_user.email == username:
        your_profile = True
    found_user = db_sess.query(User).filter((User.email == username) | (User.login == username)).first()
    if found_user:
        db_sess = db_session.create_session()
        user_list = []
        for user in db_sess.query(User).filter(User.banned != True):
            user_list.append(user)
        user_list = sorted(user_list, key=lambda user: user.wins + user.loses)
        user_list = sorted(user_list, key=lambda user: user.elo, reverse=True)
        if_pred = number_of_predators + 100
        for user in user_list[0:number_of_predators + 1]:
            if found_user.login == user.login:
                if_pred = 1
        rank = check_rating(found_user.elo, if_pred)
        username = found_user.login
        achiv = dict()
        return render_template('profile.html', form=form, current_user=your_profile,
                               username=username, rank=rank, achiv=achiv,
                               )
    else:
        return 'No such user'


@app.route('/my_profile')
@login_required
def my_profile():
    return redirect(f'/profile/{current_user.login}')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    return render_template('profile.html', form=form)


@app.route('/rating', methods=['GET', 'POST'])
@login_required
def show_rating():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    db_sess = db_session.create_session()
    user_list = []
    for user in db_sess.query(User).filter(User.banned != True):
        user_list.append(user)
    user_list = sorted(user_list, key=lambda user: user.wins + user.loses)
    user_list = sorted(user_list, key=lambda user: user.elo, reverse=True)
    data = dict()
    data['users'] = []
    for i, user in enumerate(user_list):
        if i == 100:
            break
        rank = check_rating(user.elo, i)
        data['users'].append({'world_ranking': i + 1,
                              'nickname': user.login,
                              'matches_played': user.wins + user.loses,
                              'rank': f'{rank}({user.elo})',
                              'path': url_for('static', filename=f'img/Emblems/Ranked/{ranked_emblems[rank]}'),
                              'me': user.login == current_user.login})
    return render_template('rating.html', Title='rating', data=data, form=form)


@app.route('/achievements')
@login_required
def show_achiv():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    return render_template('achivments.html', form=form, Title='achievements')


@app.route('/history', methods=['GET', 'POST'])
@login_required
def show_history():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/profile/{form.search.data}')
    db_sess = db_session.create_session()
    match_list = []
    for match in db_sess.query(Match).filter(Match.player_name == current_user.login):
        match_list.append(match)
    match_list = reversed(match_list)
    data = dict()
    data['matches'] = []
    for match in match_list:
        if match.shots <= 0:
            accuracy = '-'
        else:
            accuracy = str(round(match.hits / match.shots * 100)) + '%'
        if match.deaths <= 0:
            match.deaths = 1
        kd = round(match.kills / match.deaths, 2)
        data['matches'].append({
            'id': match.id,
            'date': str(match.match_date).split('.')[0],
            'enemy': match.enemy_name,
            'result': match.results,
            'kd': kd,
            'accuracy': accuracy,
            'elo': match.elo})
    return render_template('history.html', Title='history', data=data, form=form)


@app.route('/help')
@login_required
def give_help():
    return 'i also need it'


@app.errorhandler(401)
def custom_401(error):
    return redirect('/')


@app.errorhandler(404)
def custom_404(error):
    return redirect('/mainpage')


if __name__ == '__main__':
    app.run("127.0.0.1", 80)
