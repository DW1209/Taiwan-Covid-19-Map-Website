from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] =  '77a0d7c45b07a91a0a7c486b703fd192'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app