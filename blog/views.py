from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from functools import wraps
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
)

User = get_user_model()

def method_check(methods):
    """
    It checks request.method.
    Usage : @method_check(["GET", "POST"])
    """

    def return_check_method(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if args[0].method not in methods:
                return HttpResponseNotAllowed(methods)
            return func(*args, **kwargs)

        return inner

    return return_check_method


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
        User.objects.create_user(username, password)
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def signin(request):
    if request.method == "POST":
        req_data = json.loads(request.body.decode())
        username = req_data["username"]
        password = req_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=204)
        return HttpResponse(status=401)
    return HttpResponseNotAllowed(["POST"])

@method_check(["GET"])
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse(status=204)
    return HttpResponse(status=401)



@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])

def article_list(request):
    return HttpResponse("article_list")

def article(request, id=""):
    return HttpResponse("article")

def comment(request):
    return HttpResponse("commetn")

def comment_id(request, id=""):
    return HttpResponse("comment_id")
