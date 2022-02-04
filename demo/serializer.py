from rest_framework import serializers
# -*- coding:utf-8 -*-
from demo.models import Ssrd
import datetime
# 时间转换
def time_diff(timestamp):
    onlineTime = datetime.datetime.fromtimestamp(timestamp)
    localTime = datetime.datetime.now()
    result = localTime - onlineTime
    hours = int(result.seconds / 3600)
    minutes = int(result.seconds % 3600 / 60)
    seconds = result.seconds % 3600 % 60
    if result.days > 0:
        x = f'{result.days}天前'
    elif hours > 0:
        x = f'{hours}小时前'
    elif minutes > 0:
        x = f'{minutes}分钟前'
    else:
        x = f'{seconds}秒前'
    return x

# 热门资讯
class ReDianSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()


    class Meta:
        model = Ssrd
        fields = "__all__"

    def get_time_ago(self, obj):
        time_ago = time_diff(int(obj.eventtime))
        return time_ago