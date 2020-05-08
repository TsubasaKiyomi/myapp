# from django.conf.urls import url
# from django.urls import path
# from . import views

# urlpatterns = [
#     # 空のテキストを指定
#     path("", views.aisatsu, name="aisatsu")
# ]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.aisatsu, name="aisatsu"),
    path("second", views.secondaisatsu, name="secondaisatsu"),
]
