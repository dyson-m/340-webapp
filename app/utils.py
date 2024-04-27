from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(inner):
    """Decorator for pages that require an admin user."""
    # Use wraps to preserve the name/docstring of the function.
    @wraps(inner)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You must be logged in as an admin to access this page.')
            return redirect(url_for('login'))
        if not current_user.is_admin:
            flash('You must be an admin to access this page.')
            return redirect(url_for('index'))
        return inner(*args, **kwargs)
    return wrapped
