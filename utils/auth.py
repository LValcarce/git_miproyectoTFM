from flask import redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def configure_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == 'admin':
            return User(id='admin')
        return None

def add_logout_route(server):
    @server.route("/logout")
    def logout():
        logout_user()
        return redirect("/login")