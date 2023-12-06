from flask import Blueprint, render_template


bp = Blueprint('landing_page', __name__)

@bp.route('/')
def landing_page():
    return render_template('landing_page.html')

