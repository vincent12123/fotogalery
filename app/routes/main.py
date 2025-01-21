from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)