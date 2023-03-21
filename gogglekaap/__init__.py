from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
    
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    
    app.config['SECRET_KEY'] = 'secretkey' #session 암호화ㅏ
    app.config['SESSION_COOKIE_NAME'] = 'gogglekaap'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3307/gogglekaap?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT '] = 1
    
    '''db init'''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    '''route init'''
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)



    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html')
    
    # '''routing practice'''
    # from flask import jsonify, redirect, url_for
    # from markupsafe import escape
    
    # @app.route('/test/name/<name>')
    # def name(name):
    #     return f'name is {name},{escape(type(name))}'    
    
    # @app.route('/test/id/<int:id>')
    # def id(id):
    #     return 'id : %d' %id
    
    # @app.route('/test/path/<path:subpath>')
    # def path(subpath):
    #     return subpath
    
    # @app.route('/test/json')
    # def json():
    #     return jsonify({'name':'hi'})
    
    # @app.route('/test/urlfor/<path:subpath>')
    # def urlfor(subpath):
    #     return redirect(url_for('path',subpath=subpath))
    
    # '''method request'''
    # from flask import request
    
    # def on_json_loading_failed_return_dict(e):
    #     return {}
    
    # @app.route('/test/method/<id>', methods = ['POST', 'GET'])
    
    # def method_test(id):
    #     request.on_json_loading_failed = on_json_loading_failed_return_dict
    #     return jsonify({
    #         "requset.arg" : request.args,
    #         "request.form" : request.form,
    #         "request.json" : request.json,
    #         "request.method" : request.method 
    #     })
    
    return app