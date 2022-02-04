"""keshihua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('xyqz/', views.qgyq.as_view(), name='xyqz'), # 中国累计新增/确诊折线图
    path('zgdt/', views.Zgdt.as_view(), name='Zgdt'), # 中国地图
    path('yqbt/', views.Yqbt.as_view(), name='yqbt'), # 饼图
    path('bg/', views.Bg.as_view(), name='bg'), # 近期31省区市本土现有病例
    path('gfx/', views.gfx1.as_view(), name='gfx'), # 高风险
    path('zfx/', views.zfx1.as_view(), name='zfx'), # 中风险
    path('fxdq/', views.fxdq1.as_view(), name='fxdq'), # 中风险
    path('chinayq/', views.chinayq1.as_view(), name='chinayq'), # 更新时间
    path('ssrd/', views.ssrd1.as_view(), name='ssrd'), # 实时热点
]
