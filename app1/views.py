from django.shortcuts import render
from django.http import HttpResponse
from .forms import AisatsuForm


def aisatsu(request):
    params = {
        'title': 'Hello World',
        'msg': 'ちゃんと挨拶したいので情報の登録をしてください',
        'form': AisatsuForm(),
    }
    if (request.method == 'POST'):
        params['msg'] = 'こんにちは!' + request.POST['name'] + 'さん!<br>' + request.POST['area'] + \
            'にお住まいで<br>年齢は' + request.POST['age'] + '歳なんですね!<br>よろしくお願いします。'
        params['form'] = AisatsuForm(request.POST)
    return render(request, 'app1/index.html', params)
