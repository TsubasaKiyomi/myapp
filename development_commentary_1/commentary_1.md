#### django とは

- python の web フレームワークのこと。
- フレームワークは、開発するための機能や仕組みが準備されている物。
- アプリ設計には MVC モデルと MTV モデルがある。
- django は MTV モデルの考えが用いられている。

##### プロジェクトを立ち上げる。

作業するディレクトリを作成する今回はデスクトップに準備した。
ターミナルにコマンドを入力

```
cd Desktop
```

さらに django を立ち上げる

```
django-admin startproject myapp
*djangoをadominで立ち上げる。startprojectでファイルが全て用意される。myappはフォルダ名なので好きに変更できる。
```

```
myapp　
├── manage.py　#(ざっくり)機能に関するファイル　　　　　　　　　　　　　　　　　　　
└── myapp #このプロジェクトで使うファイルがまとめらているフォルダ
    ├── __init__.py #初期化処理を行うファイル
    ├── settings.py #設定情報を記述するファイル
    ├── urls.py #URLを管理するファイル
    └── wsgi.py　#メインプログラムのファイル
```

サーバーが起動するか確認する。myapp のディレクトリで以下のコマンドを入力する。

```
python3 manage.py runserver
```

出力結果

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

May 06, 2020 - 23:50:04
Django version 3.0.5, using settings 'myapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[06/May/2020 23:50:08] "GET / HTTP/1.1" 200 16351
```

ブラウザにアクセスできる。 http://127.0.0.1:8000/

＊ターミナルで cntrl+C でサーバーを停止できる。

###### MVC のアーキテクチャ(設計)について

| MVC        | 説明                                | MTV      |
| ---------- | ----------------------------------- | -------- |
| Model      | アプリと DB（データベース）を繋ぐ物 | Model    |
| View       | 画面表示/ページ作り                 | Template |
| Controller | コントロールする物                  | View     |

流れ
リクエストされると coutroller が model を呼び出し DB から必要なデータを受け取り、さらに View を呼び出し、ページを作りレスポンスする。

リクエスト=>coutroller が model を呼び出し=>DB データを受け取り/View を呼び出し=>ページをレスポンス

例え
会員番号を入力したら、自分の情報が DB に呼び出され、マイページ表示される。

###### アプリを作成

立ち上げたプロジェクトには MVC の仕組みがないので導入していく。

```
python3 manage.py startapp app1
```

app1 のフォルダが作成され sqlite のファイルもできた。

```
myapp
├── app1
│   ├── __init__.py #初期化処理を行うもの
│   ├── admin.py #管理者ツールのためのもの
│   ├── apps.py　#アプリの処理
│   ├── migrations #DBに関する機能がまとまったファイル
│   │   └── __init__.py
│   ├── models.py　#modelに関するもの
│   ├── tests.py　#テストに関するもの
│   └── views.py　#表示に関するもの
├── db.sqlite3
├── manage.py
└── myapp
    ├── __init__.py
    ├── __pycache__ #キャッシュなので無視
    │   ├── __init__.cpython-36.pyc
    │   ├── settings.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── wsgi.cpython-36.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

アプリ自体はいくつでも増やせる。
例え
顧客管理アプリ・商品管理アプリ・受注アプリなど・・・・

###### アプリの作動確認

表示に関することは View なので View.py の内容を変更する。
本来はテンプレートを変更するが、とりあえず View で完結させる。
HttpResponse を使うことが大切。

- aisatsu という関数を作り「**HttpResponse で情報(helloworld)を返し表示する**」という処理を書く。
  views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    return HttpResponse("Hello World")
```

view.py にコードを入力したので表示の準備はできた。
次は表示させるために URL を準備する。

- 特定のアドレスにアクセスしたら、aisatsu 関数が実行されるようにしなければならない。
  URL は urls.py の「urlpattern」にまとめられている。

urls.py

```
from django.urls import path
from django.contrib import admin
# app1フォルダのview.pyを呼び出せるようにimportしapp1を名付ける。
import app1.views as app1

urlpatterns = [
    path('admin/', admin.site.urls),
    #urlpatterns にapp1というurlを作成しaisatsu関数の処理を呼び出し。
    path('app1/', app1.aisatsu),
]
```

動いているか確認する。

```
python3 manage.py runserver
```

出力結果

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

May 07, 2020 - 00:23:19
Django version 3.0.5, using settings 'myapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

ブラウザで 127.0.0.1:8000/app1/にアクセスすると「Hello World」が表示される。

###### 改善をする

現在 app1 の処理実行を、myapp の url.py で処理している。
**_app1 の処理を増やすと、url.py に修正を加える必要があり、アプリを増やすと、それだけ複雑な管理が必要となる。_**

アプリ内のアプリ URL の管理を完結できるように改善する。

app1 フォルダの中に url.py を作成する
name という引数を使用し、url に名前をつける。name は次の投稿で使用する。
app1/urls.py

```
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path("",views.aisatsu,name="aisatsu")　#空のテキストを指定
]
```

myapp の urls.py を変更する。
**include 関数は、引数のモジュールを読み込むためのもの。**
app1 フォルダの urls.py を読み込み、app1 の URL を割り当てる。

myapp/urls.py

```
from django.urls import path,include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls')),     #ここが肝！
]
```

これで今後アプリの URL の割り当ては myapp ではなく app1 内の urls.py でできるようになった。

##### クエリパラメータ

###### クエリパラメータとは？

- 「クエリパラメータ」は様々な情報を Web サーバーに伝えるために URL に付け加える情報のこと。
- クエリ文字列（URL パラメーター）とは、サーバーに情報を送るために URL の末尾につけ足す文字列（変数）のこと。

クエリパラメタとは

```
https://www.amazon.co.jp/ref=br_msw_pdt-2　?　_encoding=UTF8&smid=A3BXOMJQF0Y34H&...
```

この「?」以降に続く、「=」で結ばれたもののことです。

分かりやすくするため app1 内の views.py を書き換える。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    name = request.GET['name']
    return HttpResponse('My name is '+ name +'.')
```

これでブラウザで
http://127.0.0.1:8000/app1/**?name=Tsubasa**
と app1/?name=名前
を入力すると・・・

```
My name is Tsubasa.
```

と表示される。

reqest は HttpRequest というクライアントのアクセス管理する class のインスタンスで、GET というメソッドを持っている。クエリパラメータに記入されたものはここに保管される。

###### クエリパラメータが無い場合

もし、クエリパラメータがなかった場合に備える。
if 文で、リクエストの中にクエリパラメータがあるかないかで処理を分岐させる。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    if 'name' in request.GET:
        name = request.GET['name']
        result = 'My name is '+ name +'.'
    else:
        result = 'please enter your name at url bar!'
    return HttpResponse(result)
```

- リクエスト：クライアント**からの**アクセスを管理
- レスポンス：クライアント**への**アクセスを管理
