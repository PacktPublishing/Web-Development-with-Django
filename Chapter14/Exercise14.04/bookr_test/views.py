from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def greeting_view(request):
    """Greet the user."""
    return HttpResponse("Hey there, welcome to Bookr! Your one stop place to review books.")


@login_required
def greeting_view_user(request):
    """Greeting view for the user."""
    user = request.user
    return HttpResponse("Welcome to Bookr! {username}".format(username=user))
