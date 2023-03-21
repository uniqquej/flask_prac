from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from gogglekaap.forms.auth_form import LoginForm, RegisterForm
from gogglekaap.models.users import User as UserModel
from werkzeug import security

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')

from dataclasses import dataclass

USERS = []

@dataclass
class User:
    '''
    class User:
        def __init__(self, user_id, username, password):
            self.user_id = user_id
            self.username = username
            self.password = password
    '''
    user_id: str
    username: str
    password: str

USERS.append(User('tester2','tester2',security.generate_password_hash('test1234')))
USERS.append(User('tester3','tester3',security.generate_password_hash('test1234')))
USERS.append(User('tester1','tester1',security.generate_password_hash('test1234')))

@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))

@bp.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        '''
        todo
        1. 유저 조회
        2. 유저가 이미 존재하는지 체크
        3. 패스워드 체크
        4. 로그인 유지(세션)
        '''
        user_id = form.data.get('user_id')
        password = form.data.get('password')
        
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            user = user[0]
            if not security.check_password_hash(user.password, password):
                flash('Password is not valid')
            else:
                session['user_id'] = user_id
                return redirect(url_for('base.index'))
        else:
            flash('User is not exists')
    else:
        #todo : error
        flash_form_errors(form)
    
    return render_template(f'{NAME}/login.html', form = form)

@bp.route('/register',  methods = ['GET','POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        '''
        todo
        1. 유저 조회
        2. 유저가 이미 존재하는지 체크
        3. 없으면 유저생성
        4. 로그인 유지
        '''
        user_id = form.data.get('user_id')
        username = form.data.get('username')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            flash('Already exists')
            return redirect(request.path) # register url로 다시 이동한다
        else:
            USERS.append(
                User(
                    user_id = user_id,
                    username = username,
                    password = security.generate_password_hash(password)
                )
            )
            session['user_id'] = user_id
            return redirect(url_for('auth.login'))
    else:
        #todo : error
        flash_form_errors(form)
    return render_template(f'{NAME}/register.html', form = form)
 
@bp.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for(f'{NAME}.login'))

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)