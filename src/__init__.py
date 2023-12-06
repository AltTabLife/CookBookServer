from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import landing_page
    app.register_blueprint(landing_page.bp)

    from . import RecipeSearch
    app.register_blueprint(RecipeSearch.bp)

    
    return app