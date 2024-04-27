from functools import wraps

from flask import flash, jsonify, make_response, redirect, url_for
from flask_login import current_user


def admin_required(inner):
    """Decorator for pages that require an admin user."""
    # Use wraps to preserve the name/docstring of the function.
    @wraps(inner)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            # No authorization, return 401 Unauthorized.
            return make_response(jsonify(
                {'error': 'Unauthorized access'}), 401)
        if not current_user.is_admin:
            # Forbidden to this user, return 403 Forbidden.
            return make_response(jsonify(
                {'error': 'Access forbidden'}), 403)
        return inner(*args, **kwargs)
    return wrapped
