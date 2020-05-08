##### フォームを作る

画面に用意するものになるので、templates の index.html を修正する。
form という URL の書き出しを行う。この form は後ほど urpatterns に追加する。
CSRF 対策タグもつける。これでフォーム送信時に、このトークンも一緒に受け渡され、チェックが行われる。

**_CSRF(クロスサイトリクエストフォージェリ)とは？_**

```
オンラインサービスを利用するユーザーがログイン状態を保持したまま悪意ある第三者の作成したURLなどをクリックした場合など、本人が意図しない形で、情報・リクエストを送信されてしまうことを意味する。ユーザー側は何が起きたのか気づくことなく。後から被害にあったことに気が付く。
```

**トークンとは？**

```
トークンとは、プログラミングにおいて、ソースコード上の文字列を、それ以上分けることのできない最小単位に分けたもののことを指します。ソースコードの内容を解析する時に、そこに記述されている文字を分割したとき、意味を持つ最小単位までに分割されたもので、例えば変数名や演算子などがそれに当たり、トークンを使用する場面は、例えばプログラミング言語から機械語に翻訳する場合。ソースコード上の変数名や関数名、その他演算子等の記号等を、それぞれ意味をもった最小単位のトークンにまで分解した後、それらの意味を1つずつ解析し、翻訳していく。
```

**セキュリティトークン**
セキュリティトークンとは「ワンタイムスパスワード」を生成する機械やソフトウェアのこと。ワンタイムパスワードは一度だけ使う「使い捨てのパスワード」

一旦不要な second は消す。
index.html

```
{% load static %}
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>{{title}}</title>
        <link rel="stylesheet" type="text/css"
        href="{% static 'app1/css/style.css' %}"/>
    </head>
    <body>
        <h1>{{title}}</h1>　　　
        <p>{{msg}}</p>
        <form action= "{% url 'form' %}" method = "post"> <!--ここのフォーム使うとformのURLに飛びます-->
            {% csrf_token %} <!--CSRF対策-->
            <label for = "msg">ここに入力：</label> <!--入力項目ラベル-->
            <input id = "msg" type="text" name ="msg"> <!--入力フォーム-->
            <input type="submit" value="入力"> <!--ボタン-->
        </form>
    </body>
</html>
```

html を変更したので、それを制御する、views.py の変更を行う。
form 関数を作る。html の input 部分に書いてある通り、ここで送信された msg to
nadukerareta
text を受け取るために、POST メソッドを利用し送信された値を取り出す。

\*一旦不要な second は消す。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    params = {
        'title':'Hello World',
        'msg':'名前を入力してください',
    }
    return render(request,'app1/index.html', params)


def form(request):
    msg = request.POST['msg']
    params = {
        'title':'Hello World',
        'msg':'hello '+msg+'!',
    }
    return render(request,'app1/index.html', params)
```

新しい関数を定義したので、この関数が呼び出せるように URL を準備する。url.py に追加する。ここで追加することで html のタグをつけるようになる。

urls.py

```
from django.urls import path
from . import views

urlpatterns = [
    path("",　views.aisatsu,　name=　"aisatsu"),
    path("form",views.form,　name="form"),
]
```

python3 manage.py runserver 　で　http://127.0.0.1:8000/app1/　にアクセスして確認する。

```
Hello Worrld ver1
名前を入力してください

ここに入力
```

入力後

```
Hello World
hello tsu! <!-- ここの表示が変わる -->

ここに入力
```

###### 今後の対策として

入力した名前がクリアになってしまうので、DB 登録とのチェック機能などができないと汎用性が無い。なので django に用意されている Form クラスを使用する。

app1 フォルダ配下に forms.py を作成する。
テキスト(char)と整数(int)の入力フィールドを用意、label で名前をつける。

app1/forms.py

```
from django import forms

class Aisatsuform(forms.Form):
    name = forms.CharField(label="name")
    area = forms.CharField(label="area")
    age = forms.IntegerField(label="age")
```

このフォームを利用できるような制御にするために、views.py を修正する。
パラメタの中に form を作りインスタンスを入れる。
request.method で、リクエストが POST かどうかをチェックして、そうだったら POST 用の処理を実施する。GET なら、ページだけを返す。
※POST とか GET:HTTP メソッド。フォームを使うなら POST を利用。他にもいくつかメソッドがあるが、メソッドを見れば、どんなことが行われているかわかるようになっている。

views.py

```
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AisatsuForm

def aisatsu(request):
    params = {
        'title':'Hello World',
        'msg':'ちゃんと挨拶したいので情報の登録をしてください',
        'form': AisatsuForm(),
    }
    if (request.method=='POST'):
        params['msg'] = 'こんにちは!'+request.POST['name']+'さん!<br>'+request.POST['area']+'にお住まいで<br>年齢は'+request.POST['age']+'歳なんですね!<br>よろしくお願いします。'
        params['form']= AisatsuForm(request.POST)
    return render(request,'app1/index.html', params)
```

冒頭で aisatsuform のインスタンスを form に代入しもし POST リクエストだったら、もう一度 POST の内容でインスタンスを作り上書きを行っている。同様に msg も書き換えを行い、POST された情報を表示させるようにしている。ここでは<br>などの html タグが埋め込まれているので、index.html で表示させている時、知らせなくてはならない。以下のようにする。

画面表示を直すため index.html を修正する。
フォームは置き換える。
{{form}}のところをテーブル(as_table)にしたり、リスト(as_ul)にすることもできる。何も指定しないと横一列にフィールドが設置される。※table にする場合タグが必要。

index.html

```
{% load static %}
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>{{title}}</title>
        <link rel="stylesheet" type="text/css"
        href="{% static 'app1/css/style.css' %}"/>
    </head>
    <body>
        <h1>{{title}}</h1>　　　
        <p>{{msg|safe}}</p><!--ここでviews.pyのhtmlを有効化-->
        <form action= "{% url 'aisatsu' %}" method = "post">
            {% csrf_token %}
            {{form.as_ul}} <!--ここ-->
            <input type="submit" value="入力">
        </form>
    </body>
</html>
```

views.py を変えている(form 関数をなくした)ので url をのとに直す。

http://127.0.0.1:8000/にアクセスしてみる。

```
Hello World
ちゃんと挨拶したいので情報の登録をしてください

name:
area:
age:
```
入力後・・・・
```
Hello World
こんにちは!翼さん!
kanagawaにお住まいで
年齢は30歳なんですね!
よろしくお願いします。

name: 翼
area: kanagawa
age: 30
```
