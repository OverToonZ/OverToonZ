import time
from django.db.models import Q
from .models import User

def versioning(request):
    return {'time':int(time.time())}



def user_details(request):
    if request.user.is_authenticated:
        userdata = User.objects.filter(Q(email = request.user)|Q( username = request.user)).values()
        userinfo = {}
        for info in userdata:
            userinfo['username'] = info['username']
            userinfo['email'] = info['email']
            userinfo['favourite_anime'] = info['favourite_anime']
            userinfo['date_joined'] = info['date_joined']
            userinfo['last_login'] = info['last_login']
            userinfo['login_count'] = info['login_count']
            if info['is_superuser'] == True:
                userinfo['role'] = "Admin"
            else:
                userinfo['role'] = "User"
    else:
        userinfo = {}
        userinfo['username'] = "Mr. Anonymous"
        userinfo['email'] = "Not Available"
        userinfo['favourite_anime'] = "Not Available"
        userinfo['date_joined'] = "Not Available"
        userinfo['last_login'] = "Not Available"
        userinfo['login_count'] = 0
        userinfo['role'] = "Anonymous User"

    return {
        'userinfo': userinfo
    }