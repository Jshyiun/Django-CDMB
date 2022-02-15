## 这是一个Django项目
## 使用技术栈：Django4.0 + Python3.9 + AdminLTE3.2 + MySQL8.0

## 简单的使用方法：


创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py文件为settings.py
运行migrate命令，创建数据库和数据表 （Django默认使用SQLite3数据库）
运行python manage.py runserver启动服务器


路由设置：


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('precious/', include('precious.urls')),
]

## /precious/urls.py
from django.urls import path
from precious import views


app_name = 'precious'

urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('detail/<int:asset_id>/', views.detail, name='detail'),
    path('', views.dashboard),
]