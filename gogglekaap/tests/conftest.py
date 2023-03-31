import sys
sys.path.append('.')

from gogglekaap.configs import TestingConfig
from gogglekaap import create_app, db
from gogglekaap.models.users import User as UserModel
from gogglekaap.models.memo import Memo as MemoModel
import pytest
import os, shutil


@pytest.fixture(scope='session')
def user_data():
    yield dict(
        user_id='tester',
        user_name='tester',
        password='tester'        
    )
    
@pytest.fixture(scope='session')
def memo_data():
    yield dict(
        title ='test memo',
        content = 'test content'
    )

@pytest.fixture(scope='session')
def app(user_data, memo_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all() # flask db upgrade처럼 동작
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.flush() #user.id를 받아올 수 있게 해줌
        memo_data['user_id'] = user.id
        db.session.add(MemoModel(**memo_data))
        db.session.commit()        
        yield app
        #불필요 db 정리
        path = os.path.join(
            app.static_folder,
            app.config['USER_STATIC_BASE_DIR'],
            user_data['user_id']
        )
        shutil.rmtree(path, True)
        db.drop_all()
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            'sqlite:///',
            ''
        )
        if os.path.isfile(db_path):
            os.remove(db_path)
    

@pytest.fixture(scope='session')
def client(app, user_data):
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = user_data.get('user_id')
        yield client