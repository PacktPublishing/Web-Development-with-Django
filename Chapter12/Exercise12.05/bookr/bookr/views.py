from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    return render(request, 'profile.html',
            {'user': user, 'permissions': permissions})

