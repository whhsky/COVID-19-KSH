import json
from django.http import HttpResponse
from rest_framework.views import APIView

# Create your views here.
from .ksh import xyqz, zgdt, yqbt, bg, gfx
from .models import Ssrd
from .serializer import ReDianSerializer


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error



# 全国疫情
class qgyq(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(xyqz()))

# 中国疫情地图
class Zgdt(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(zgdt()))

# 中国疫情地图
class Yqbt(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(yqbt()))

# 近期31省区市本土现有病例
class Bg(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bg()))


# 高风险地区
class gfx1(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(gfx('高风险')))
# 中风险地区
class zfx1(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(gfx('中风险')))
# 风险地区
class fxdq1(APIView):
    def get(self, request, *args, **kwargs):
        with open('demo/data/风险地区.json', 'r', encoding='utf-8') as f:
            data = f.read()
        return JsonResponse(json.loads(data))
# 中国疫情
class chinayq1(APIView):
    def get(self, request, *args, **kwargs):
        with open('demo/data/中国疫情.json', 'r', encoding='utf-8') as f:
            data = f.read()
        return JsonResponse(json.loads(data))
# 实时热点
class ssrd1(APIView):
    def get(self, request, *args, **kwargs):
        ssrd = Ssrd.objects.all()
        serializer = ReDianSerializer(ssrd, many=True)
        return JsonResponse(serializer.data)
# 主页
class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index.html", 'rb').read())