import simplejson
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from stacks.www.models import Following

def error_json(message=None, code=None):
    """Generates a standard 'error' response."""
    d = {u'status': 'error'}
    if message:
        d[u'message'] = message
    if code:
        d[u'code'] = code
    return HttpResponse(simplejson.dumps(d), mimetype='application/json')

def ok_json(message=None):
    """Generates a standard 'ok' response."""
    d = {u'status': 'ok'}
    if message:
        d['message'] = message
    return HttpResponse(simplejson.dumps(d), mimetype='application/json')

@login_required
def follow(request):
    followed_user_id = request.POST.get('followed_user')
    if not followed_user_id:
        return error_json("You need to tell me who to follow.")
    else:
        try:
            followed_user = User.objects.get(id=followed_user_id)
        except User.DoesNotExist:
            return error_json("That user doesn't exist.")

        request.user.following.create(followed_user=followed_user)
        return ok_json("Now following %s" % followed_user.username)

@login_required
def unfollow(request):
    followed_user_id = request.POST.get('followed_user')
    if not followed_user_id:
        return error_json("You need to tell me who to follow.")
    else:
        try:
            followed_user = User.objects.get(id=followed_user_id)
        except User.DoesNotExist:
            return error_json("That user doesn't exist.")

        try:
            f = request.user.following.get(followed_user=followed_user)
            f.delete()
        except Following.DoesNotExist:
            return error_json("Ease up, you're not following that user anyway.")

        return ok_json("Unfollowed %s" % followed_user.username)
