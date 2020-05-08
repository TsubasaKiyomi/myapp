###### 動作させるためのアプリ設定

- テンプレート作成の前に**必ず**しなければならないことが、**アプリケーションの設定**。
  「myapp プロジェクトの中の app1 というアプリ」ということを宣言しないと、**動作しない**。

seeting.py のファイル内の内容に'app1'を追記する。

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',#これを追加する
]
```

加えて言語の設定を変える。
seeting.py

```
LANGUAGE_CODE = 'ja-JP'

TIME_ZONE = 'Asia/Tokyo'
```

##### テンプレートを作成

- app1 ディレクトリの配下に templates フォルダを作成。さらにその配下に app1 フォルダを作成し、index.html を作成した。なぜ app1/index.html にしたのか？これは、今後アプリを複数このプロジェクトで作成した場合、app2,app3 と全部同じ index.html だと、どのアプリの html か分からなくなるので、区別できるようにした。

index.html

```
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>app1</title>
    </head>
    <body>
        <h1>Hello World</h1>
        <p>おはよう世界、おはよう世界、おはよう世界</p>
        <p>こんにちは世界、こんにちは世界、こんにちは世界</p>
        <p>こんばんは世界、こんばんは世界、こんばんは世界</p>
        <p>おやすみ世界、おやすみ世界、おやすみ世界</p>
    </body>
</html>
```

###### html ファイルにアクセスできるようにする

html を作成したので、この html ファイルにアクセスできるようにする。
app1/urls.py は、views.py の aisatsu 関数を呼び起こすようにしているので、aisatsu 関数が app1/index.ntml を参照するように書き直す。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    return render(request,'app1/index.html')#ここが肝！
```

**python3 manage.py runserver**コマンドで
http://127.0.0.1:8000/app1/　ブラウザに移動

templates フォルダからの相対パスを指定し、以下の出力結果になればちゃんとレンダリングされている。

出力結果

```
Hello World
おはよう世界、おはよう世界、おはよう世界

こんにちは世界、こんにちは世界、こんにちは世界

こんばんは世界、こんばんは世界、こんばんは世界

おやすみ世界、おやすみ世界、おやすみ世界
```

- **_render 関数は第一引数に HttpRequest クラスのインスタンス、第二引数に html ファイルを指定する。_**
- **_レンダリングとは、コードを書いてあることを読み込み、必要な物に置き換え、画面表示させること。_**

###### テンプレートの値を渡す

鐵 m プレートの値を渡せるようにする。DB から情報を呼び出して、画面上に表示させる時に大切になる。一旦 view.py に情報を入れる。

まずはテンプレートの index.html を修正する。
{{}}は変数や関数などを呼び出すためのもの。これを入れることで、レンダリングする際に変数を参照にする。

index.html

```
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>{{title}}</title> <!--ここが大事-->
    </head>
    <body>
        <h1>{{title}}</h1>　　　<!--ここが大事-->
        <p>{{msg}}世界</p>
        <p>{{msg}}世界</p>
        <p>{{msg}}世界</p>  　<!--ここが大事-->
    </body>
</html>
```

views.py に情報を与える。

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    params = {
        'title':'Hello Worrld',
        'msg':'こんにちは',
    }
    return render(request,'app1/index.html', params)
```

render の第三引数に params を指定した。
**python3 manage.py runserver**でブラウザに移行すると以下のような表示になる。

```
Hello Worrld
こんにちは世界

こんにちは世界

こんにちは世界
```

##### ページの遷移

ページは１つだけでなく何個も作れるが、html を毎回書き直すのは大変。なので index.html を流用しページを作成する。
html を以下のようにする。
アンカーリンクの追加し{%%}はテンプレートタグで今回は url タグを使用する。指定した名前の URL が書き出させる。ここで使われている名前は、urlpatterns で name 指定したものを利用できる。\*さらに gopage というのを views.py に用意する。

index.html

```
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>{{title}}</title>
    </head>
    <body>
        <h1>{{title}}</h1>　　　
        <p>{{msg}}世界</p>
        <p>{{msg}}世界</p>
        <p>{{msg}}世界</p>
        <p><a href="{% url gopage %}">{{gopage}}</a></p> <!--ここ-->
    </body>
</html>
```

- 遷移したことをわかりやすくするため、secondaisaisatsu のページ用情報を用意。さらに上記の gopage 用のパラメタを用意。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    params = {
        'title':'Hello World　ver1',
        'msg':'こんにちは',
        'gopage':'secondaisatsu',
    }
    return render(request,'app1/index.html', params)

def secondaisatsu(request):
    params = {
        'title':'Hello World ver2',
        'msg':'さようなら',
        'gopage':'aisatsu'
    }
    return render(request,'app1/index.html', params)
```

最後に secondaisatsuni にアクセスできるように URL を準備する。
second という URL を割り振り、secondaisatsu の処理をするようにした。

app1/urls.py

```
from django.urls import path
from . import views

urlpatterns = [
    path("",views.aisatsu,name="aisatsu"),
    path("second",views.secondaisatsu,name="secondaisatsu"),
]
```

ここまで編集するとページが２つできる。

```
Hello Worrld ver1
こんにちは世界

こんにちは世界

こんにちは世界

secondaisatsu
```

```
Hello Worrld ver2
さようなら世界

さようなら世界

さようなら世界

aisatsu
```

###### ページの装飾もできる

CSS や Javascript で装飾ができる。
今回の場合は、app1/templates/app1 に作成するのではなく。
static フォルダを用意する。

- app1 の配下(templates と同じ階層)に static フォルダを作り、その下に app1 フォルダを作る。さらにその下に css のフォルダを設置しその中に css ファイルを作る。

```
myapp
├── app1
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── admin.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   ├── urls.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-36.pyc
│   ├── models.py
│   ├── static   #これ
│   │   └── app1　　　＃これ
│   │       └── css　　　＃これ
│   │           └── style.css　＃これ
│   ├── templates
│   │   └── app1
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
└── myapp
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   ├── settings.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── wsgi.cpython-36.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

style.css ができたら適当にコードを入力する

```
body {
    color:blue;
    font-size:20pt;
}

h1 {
    color:red;
    font-size:32pt;
}

p {
    color:green;
    margin:10px;
}

a {
    color:yellow;
}
```

この css を読み込むように index.html を修正する。
**静的ファイル**を読み込む時は{% load static %}を利用する。
さらに
href="{% static'app1/css/style.css'%}"/>
と記述することで css ファイルを呼び出す。
javascript や jpeg などのイメージを呼び出す際も同じコードになる。

**python3 manage.py runserver**を起動しブラウザに移行すると
cssのコードが反映されている。