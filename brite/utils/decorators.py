from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models.user import User


def admin_required(fn):
    """
    Decorator function that checks if the current user has an 'admin' role.

    Parameters:
    - fn: The function to be decorated.

    Returns:
    - The decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user or user.role != "admin":
            return {"message": "Admin role required!"}, 403
        return fn(*args, **kwargs)

    return wrapper
