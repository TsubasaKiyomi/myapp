# from django.shortcuts import render
# from django.http import HttpResponse


# def aisatsu(request):
#     return HttpResponse("Hello World")
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse


# クエリパラメータがあるか無いか？をif文で分岐させる。
# def aisatsu(request):
#     if 'name' in request.GET:
#         name = request.GET['name']
#         result = 'My name is ' + name + '.'
#     else:
#         result = 'please enter your name at url bar!'
#     return HttpResponse(result)
def aisatsu(request):
    params = {
        'title': 'Hello Worrld ver1',
        'msg': 'こんにちは',
        'gopage': 'secondaisatsu',
    }
    return render(request, 'app1/index.html', params)


def secondaisatsu(request):
    params = {
        'title': 'Hello Worrld ver2',
        'msg': 'さようなら',
        'gopage': 'aisatsu',
    }
    return render(request, 'app1/index.html', params)
