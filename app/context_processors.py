import jwt
import time
from django.conf import settings as app_settings
from django.core.cache import cache


def get_centrifugo_data(user_id):
    ws_url = app_settings.CENTRIFUGO_WS_URL
    secret = app_settings.CENTRIFUGO_SECRET
    token = jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 10 * 60}, secret, algorithm="HS256")
    return {"centrifugo": {"token": token, "url": ws_url}}


def global_settings(request):
    best_members = cache.get("best_members")
    popular_tags = cache.get("popular_tags")
    return {"best_members": best_members, "popular_tags": popular_tags, **get_centrifugo_data(request.user.id)}
