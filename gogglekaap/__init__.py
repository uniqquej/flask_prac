from flask import Flask, g
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)
    csrf.init_app(app)
    
    '''flask configs'''
    from .configs import ProductionConfig, DevelopmentConfig
    
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
    
    app.config.from_object(config)
    
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
    
    '''RestX init'''
    from gogglekaap.apis import blueprint as api
    app.register_blueprint(api)
    
    '''Request Hook'''
    @app.before_request 
    def before_request():
        g.db = db.session # 매 요청 전에 db를 물려주는 역할
    
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close() # 모든 요청 후 db를 닫아주는 역할
    
    
    
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html')
    
    return app