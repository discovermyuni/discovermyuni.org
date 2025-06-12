from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _

LOGIN_REQUIRED_MESSAGE = _("You need to be logged in to view the dashboard.")


def login_required_message(
    message=LOGIN_REQUIRED_MESSAGE,
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url=None,
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, message)
            return actual_decorator(view_function)(request, *args, **kwargs)

        return wrapper

    if function:
        return decorator(function)
    return decorator
