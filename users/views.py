import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile


def api_response(data=None, code=0, message="success", status=200):
    return JsonResponse({"code": code, "message": message, "data": data}, status=status)


def error_response(message, status=400):
    return api_response(None, -1, message, status)


def get_profile_dict(user):
    profile = getattr(user, "profile", None)
    return {
        "id": user.id,
        "username": user.username,
        "nickname": profile.nickname if profile else user.username,
        "email": user.email,
        "bio": profile.bio if profile and profile.bio else "",
        "created_at": profile.created_at.strftime("%Y-%m-%d") if profile else "",
    }


@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return error_response("请求数据格式错误")

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    email = body.get("email", "").strip()
    nickname = body.get("nickname", "").strip() or username

    if not username or not password:
        return error_response("用户名和密码不能为空")
    if len(password) < 6:
        return error_response("密码至少6位")
    if User.objects.filter(username=username).exists():
        return error_response("用户名已被注册", 409)
    if email and User.objects.filter(email=email).exclude(email="").exists():
        return error_response("邮箱已被使用", 409)

    user = User.objects.create_user(username=username, password=password, email=email)
    Profile.objects.create(user=user, nickname=nickname, bio=body.get("bio", ""))
    login(request, user)
    return api_response(get_profile_dict(user), message="注册成功", status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return error_response("请求数据格式错误")

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        return error_response("请输入用户名和密码")

    user = authenticate(request, username=username, password=password)
    if user is None:
        return error_response("用户名或密码错误", 401)

    login(request, user)
    return api_response(get_profile_dict(user), message="登录成功")


@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    if not request.user.is_authenticated:
        return error_response("未登录", 401)
    logout(request)
    return api_response(None, message="已退出登录")


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def profile_detail(request):
    if not request.user.is_authenticated:
        return error_response("请先登录", 401)

    if request.method == "GET":
        return api_response(get_profile_dict(request.user))

    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("请求数据格式错误")

        profile, _ = Profile.objects.get_or_create(user=request.user)
        nickname = body.get("nickname", "").strip()
        if nickname:
            profile.nickname = nickname
        if "bio" in body:
            profile.bio = body.get("bio", "").strip()
        profile.save()

        email = body.get("email", "").strip()
        if email and email != request.user.email:
            request.user.email = email
        password = body.get("password", "").strip()
        if password:
            if len(password) >= 6:
                request.user.set_password(password)
            else:
                return error_response("密码至少6位")
        request.user.save()

        return api_response(get_profile_dict(request.user), message="资料已更新")
