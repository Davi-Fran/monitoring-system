from apps.accounts.models import User

def user_list():
    return User.objects.all()