from appio import App

from .routes import api_routes


def create_app():
    app = App()
    app.routes = api_routes
    return app
