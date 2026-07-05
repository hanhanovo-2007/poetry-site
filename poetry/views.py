import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Poem, Comment


def api_response(data=None, code=0, message="success", status=200):
    return JsonResponse({"code": code, "message": message, "data": data}, status=status)


def error_response(message, status=400):
    return api_response(None, -1, message, status)


def get_user_from_request(request):
    if not request.user.is_authenticated:
        return None
    profile = getattr(request.user, "profile", None)
    return {
        "id": request.user.id,
        "username": request.user.username,
        "nickname": profile.nickname if profile else request.user.username,
        "email": request.user.email,
    }


def poem_to_dict(poem, request=None):
    author = poem.author
    profile = getattr(author, "profile", None)
    comments_count = poem.comments.count()
    result = {
        "id": poem.id,
        "title": poem.title,
        "content": poem.content,
        "author": {
            "id": author.id,
            "username": author.username,
            "nickname": profile.nickname if profile else author.username,
        },
        "likes": poem.likes,
        "views": poem.views,
        "comments_count": comments_count,
        "created_at": poem.created_at.strftime("%Y-%m-%d %H:%M"),
        "updated_at": poem.updated_at.strftime("%Y-%m-%d %H:%M"),
    }
    if poem.image and request:
        result["image"] = request.build_absolute_uri(poem.image.url)
    return result


def comment_to_dict(comment):
    author = comment.author
    profile = getattr(author, "profile", None)
    return {
        "id": comment.id,
        "poem_id": comment.poem_id,
        "author": {
            "id": author.id,
            "username": author.username,
            "nickname": profile.nickname if profile else author.username,
        },
        "text": comment.text,
        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def list_create_poems(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        poems = Poem.objects.all()
        if search:
            poems = poems.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
                | Q(author__username__icontains=search)
            )
        author_id = request.GET.get("author")
        if author_id:
            poems = poems.filter(author_id=author_id)
        data = [poem_to_dict(p, request) for p in poems]
        return api_response(data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return error_response("请先登录", 401)

        # 支持 JSON 和 multipart/form-data 两种提交方式
        if request.content_type and "multipart/form-data" in request.content_type:
            title = request.POST.get("title", "").strip()
            content = request.POST.get("content", "").strip()
            image_file = request.FILES.get("image", None)
        else:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return error_response("请求数据格式错误")
            title = body.get("title", "").strip()
            content = body.get("content", "").strip()
            image_file = None

        if not title:
            return error_response("请输入诗词标题")
        if not content:
            return error_response("请输入诗词正文")

        poem = Poem.objects.create(
            title=title,
            content=content,
            author=request.user,
        )
        if image_file:
            poem.image = image_file
            poem.save(update_fields=["image"])

        return api_response(poem_to_dict(poem, request), message="作品发表成功", status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def poem_detail(request, poem_id):
    try:
        poem = Poem.objects.get(id=poem_id)
    except Poem.DoesNotExist:
        return error_response("作品不存在", 404)

    if request.method == "GET":
        poem.views += 1
        poem.save(update_fields=["views"])
        data = poem_to_dict(poem, request)
        comments = poem.comments.all()
        data["comments"] = [comment_to_dict(c) for c in comments]
        return api_response(data)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return error_response("请先登录", 401)
        if poem.author != request.user:
            return error_response("无权修改此作品", 403)
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("请求数据格式错误")
        if "title" in body:
            title = body["title"].strip()
            if title:
                poem.title = title
        if "content" in body:
            poem.content = body["content"].strip()
        poem.save()
        return api_response(poem_to_dict(poem, request), message="作品已更新")

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return error_response("请先登录", 401)
        if poem.author != request.user:
            return error_response("无权删除此作品", 403)
        poem.delete()
        return api_response(None, message="作品已删除")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def list_create_comments(request, poem_id):
    try:
        poem = Poem.objects.get(id=poem_id)
    except Poem.DoesNotExist:
        return error_response("作品不存在", 404)

    if request.method == "GET":
        comments = poem.comments.all()
        data = [comment_to_dict(c) for c in comments]
        return api_response(data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return error_response("请先登录", 401)
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("请求数据格式错误")
        text = body.get("text", "").strip()
        if not text:
            return error_response("评论内容不能为空")
        comment = Comment.objects.create(
            poem=poem,
            author=request.user,
            text=text,
        )
        return api_response(comment_to_dict(comment), message="评论发表成功", status=201)


@csrf_exempt
@require_http_methods(["POST"])
def like_poem(request, poem_id):
    try:
        poem = Poem.objects.get(id=poem_id)
    except Poem.DoesNotExist:
        return error_response("作品不存在", 404)
    poem.likes += 1
    poem.save(update_fields=["likes"])
    return api_response({"likes": poem.likes}, message="点赞成功")

