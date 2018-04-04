# CentOS上にPENGUINが動作する環境を構築しよう
PENGUIN(11月祭事務局制作のWebアプリケーション)を情報環境機構所有のCentOS7.4仮想マシン上で走らせるための環境を構築する方法をここでは記載します。このDocumentationの目的は「情報環境機構の方への情報共有」と「後輩への引き継ぎ」を兼ねていますので、特に情報環境機構の方にとってはややくどい説明となっておりますことをご了承ください。

```local$```から始まるコマンドラインはローカルで、```remote$```から始まるコマンドラインはサーバーサイドで作業することを意味します。また、ローカルマシンはUbuntu16.04 LTSです。

# 1.LAMP構成を作りましょう
LAMP構成は次の4要素からなります。
|||
| --- | --- |
| **P**ython3.6.4 (Django2.0.3) | PENGUINはDjangoというPythonベースのWebフレームワークで動いています。|
| **M**ariaDB10.2.13 | データベースを扱います。CentOS7からMySQLに代わって標準になりました。 |
| **A**pache HTTP Server2.4.6 | webサーバー。ネット上に何か上げる際は必須です。 |
| **L**inux (CentOS7.4.1708) | 情報環境機構の方にインストールしていただきました。 |

ということでこのLAMP構成を完成させることが目標です。

# 2.Linuxの初期設定
情報環境機構の方は読み飛ばしていただいても構いません。

##  1. ssh秘密鍵と公開鍵のペアを作る
```
local$ ssh-keygen -t rsa

Generating public/private rsa key pair.
Enter file in which to save the key (/home/$USER/.ssh/id_rsa):
```
(以下```$USER```は自分のlocalのユーザー名に置き換えてください。)

## 2. 秘密鍵と公開鍵のペアを置く場所と鍵の名前を決める
```
Enter file in which to save the key (/home/$USER/.ssh/id_rsa):/home/$USER/.ssh/penguin_rsa
```
ここでは```pegnuin_rsa```という名前にしておきました。```_rsa```で終わるファイル名にしないとエラーを吐いてしまいます。

さて、正しいファイル名を入力すると次にパスコードの入力を求められます。
```
Enter passphrase (empty for no passphrase):
```
これはサーバーにログインする際に必要になりますから、慎重に設定してください。また、何があっても **他の人には絶対にバラさないでください！！！** 2回入力を求められ、合致していれば指定された場所に鍵が保存されるはずです。
* パスコード入力画面では何かを入力しても画面の変化がありません（「***」も表示されません）。

## 3. 情報環境機構に公開鍵と希望ユーザー名を送信する
成功すると指定した場所に```penguin_rsa```と```penguin_rsa.pub```が保存されます。このうち```penguin_rsa.pub```とサーバーにログインする際のユーザー名（ここでは```user```とします）を情報環境機構にメール等で送信してください。
* 鍵を作る際に設定したパスコードや```penguin_rsa```など、上記の2つ以外のものを送信しないでください！**これらは自分以外の誰にも漏洩してはいけません**！！
    * 若林はここでパスコードを漏洩させてしまいました。本当に気をつけましょう。パスコードを漏洩させた場合は```ssh-keygen -p```で再設定し、```penguin-rsa```を誤って送信してしまった場合はもう一度鍵ペアを作り直してください。

## 4. サーバーにログインする
しばらくしたら情報環境機構がログイン可能な状態にしてくれます。次のコマンドを打ってログインしましょう。

```
local$ user@(IPアドレス) -i (秘密鍵penguin_rsaのパス)
```

これを入力するとパスコードを聞かれることがあるのでその際は設定したものを入力してください。
初回ログインの際は警告が出てきますが、```yes```と入力すればOKです（Aliasを設定すると便利です。やりかたはググって調べてください）。

## 5. サーバー側のパスワードを設定しよう
情報環境機構が初期パスワードを設定してくれていますので、まずは情報環境機構が指定した方法で手に入れてください。手に入れたらサーバー側で次のコマンドを打ちましょう。

```
remote$ passwd
```
あとは古いパスワード（先程手に入れたパスワード）→新しいパスワード→新しいパスワード（再入力）の順番で入力すればOKです。記号を必ず1つ含むなど、かなり複雑なパスワードにしないとエラーが返ってくるようです。

これでLAMP構成の「L」が完成しました。お疲れ様でした。

# 3. Apacheを立てる
ApacheとはWebサーバーの一つであり、簡単に言えばインターネットの大海原に何かを上げる際に必須となるものです。

## 1. Apacheをインストールする
```
remote$ sudo yum install -y httpd httpd-devel
```
* ```sudo```はアプリをインストールするときなど、ちょっと「アブナイ」操作を行う際に頭につけるコマンドです。```You need to be root to perform this command.```みたいなことを言われた際は```sudo```を頭につけて実行するとうまく行くことがあります。たまに```sudo```を実行するとサーバー上でログインしているユーザー（ここでは```user```）のパスワードを聞かれるので入力してあげましょう。

いろいろ画面上にうわーって出てきた後```Complete!```と出てきたら終了です。

## 2. 80番ポートを開放する
```
remote$ sudo firewall-cmd --add-port=80/tcp --zone=public --permanent
success
remote$ sudo firewall-cmd --reload
success
```

* 簡単に言うと「ブラウザからアクセスできるようにする」作業です。

## 3. Apacheを起動する
```
remote$ sudo systemctl enable httpd
remote$ sudo systemctl start httpd
```
WebブラウザにサーバーのIPアドレスを入力するとこんな画面が表示されます。

![i1](i1.png)

この画面が表示されたら成功です。以上でLAMP構成の「LA」が完成しました。お疲れ様でした。

# 4. MariaDBをインストールする
MariaDBはほとんどMySQLと同じで、データベースを扱う際に必要となるものです。

## 1. インストールする
```
remote$ sudo yum install -y mariadb mariadb-server
remote$ sudo systemctl enable mariadb
remote$ sudo systemctl start mariadb
```
特に迷うことはないかと。

## 2. 文字化け対策をする
```
remote$ sudo cp -p /usr/share/mysql/my-small.cnf /etc/my.cnf.d/server.cnf
remote$ sudo vim /etc/my.cnf.d/server.cnf
```

ここで```vim```というコマンドが出てきました。これはテキストエディターなのですが、非常に癖があります。**テキストを打てる状態にするために```i```キーを押してください**。そして、次の文を挿入してください。

```
[client]
......
default-character-set = utf8 #new!

[mysqld]
......
character-set-server = utf8 #new!
```

**入力し終えたら```Esc```→```:wq```→```Enter```の順番でキーを打ってください**。
（詳しいVimの使い方はググってください。Vimを極めるとコーディングスピードが上がるそうです）

## 3. MariaDBの設定を行う
まずは次のコマンドを入力してください。
```
remote$ mysql_secure_installation
```

するとダイアログに従ってMariaDBを設定することができます。
```
Enter current password for root (enter for none):
```
ここは何も入力せずにEnterを押してください。
```
Set root password? [Y/n] Yと入力
New password: (適当に設定し入力)
Re-enter new password: (上と同じものを入力)
```
ここではデータベースに関する最も強い権限を持つユーザーのパスワードを設定します。絶対にバレないようにしましょう。

```
Remove anonymous users? [Y/n] Yと入力
Disallow root login remotely? [Y/n] Yと入力
Remove test database and access to it? [Y/n] Yと入力
Reload privilege tables now? [Y/n] Yと入力
```
すべて```Y```で問題ないでしょう。```Thanks for using MariaDB!```と表示されたらOKです。
```root```ユーザーとしてSQL文を書きたい際は```mysql -u root -p```と入力してrootのパスワードを入力してください。

これでMariaDBのインストールが完了しました。この後Djangoアプリとデータベースを接続する作業がありますが、とりあえずデータベースの構築を一旦休止し、次にPythonがサーバー上で動く環境を作りましょう。

# 5. Pythonをサーバー上で動かす
## 1. pyenvを用いてpython3をインストール
CentOSに```python```と入力するとpython2.7.5が起動してしまいます。最新のDjangoはPython3上じゃないと動いてくれないので、pythonの異なるバージョンを併存させることができるpyenvを導入します。

```
remote$ sudo yum install -y git
remote$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
remote$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
remote$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
remote$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
remote$ source ~/.bash_profile
```

```pyenv -v```と入力してインストールされていることを確認してください。

次にpython3を入れていきます。
```
remote$ sudo yum install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel gcc
```

インストールできるpythonのバージョンを確認しましょう。
```
remote$ pyenv install -l
Available versions:
...
  3.6.3
  3.6.4
  3.7.0b2
  3.7-dev
  3.8-dev
  activepython-2.7.14
 ......
  ```
ということで今回は現時点での最新版python3.6.4をインストールすることにしましょう。
```
remote$ pyenv install 3.6.4
remote$ pyenv global 3.6.4
```

最後に```python --version```と入力してバージョンを確認してください。```Python 3.6.4```と表示されたらOKです。

## 2. virtualenvでPENGUIN用の仮想環境を組もう
PENGUINを動かすに当たってpipとかでいろいろインストールするので仮想環境を作りましょう。
```
remote$ cd [project dir] #ここでは/home/zuyaとする
remote$ python -m venv [new virtualenv name] #ここではdjvenvとする
```
これで```/home/user```上に仮想環境ディレクトリ```djvenv```ができます。この後いつでも好きなタイミングで仮想環境```djvenv```の有効化・無効化が可能になります。

|操作|コマンド|変化|
| --- | --- | --- |
| 環境突入 | ```source ~/djvenv/bin/activate```  | 左に```(djvenv)```と表示される|
| 環境脱出 | ```deactivate``` | 左の```(djvenv)```が消える|

## 3. djangoを仮想環境djvenvにインストールしよう
まず仮想環境を有効化しましょう。
```
remote$ source ~/djvenv/bin/activate
```
次にdjangoをインストールし、プロジェクト```penguin```を立ち上げます。
```
remote$ pip install django
remote$ django-admin startproject penguin
```
ここで設定を少しいじりましょう。
```
remote$ cd penguin
remote$ vim penguin/settings.py
```
変更点は以下のとおりです。
|変数名|変更前|変更後|説明|
| --- | --- | --- | --- |
| ALLOWED_HOSTS | [] | ['*'] | すべてのホストからのアクセスを許可 |
| LANGUAGE_CODE | 'en-us' | 'ja' | 色々日本語化 |
| TIME_ZONE | 'UTC' | 'Asia/Tokyo' | タイムゾーンを日本にする |
| USE_TZ | True | False | なぜかこうしないとタイムゾーンが日本にならない |

## 4. テストサーバーを立てて確認しよう

では8000番ポートを開放してテストサーバーを立てます。
```
remote$ sudo firewall-cmd --add-port=8000/tcp --zone=public
remote$ python manage.py runserver 0.0.0.0:8000
```
ブラウザで```(IPアドレス):8000```と入力してこのような画面が表示されたらOKです。
![i2](i2.png)

確認できたら```Ctrl+C```でテストサーバーを閉じて8080ポートを閉じましょう。
```
remote$ sudo firewall-cmd --remove-port=8000/tcp --zone=public
```

## 5. Apache上でpythonが動くようにしよう
Apache上でpythonを動かすためにはmod_wsgiというモジュールが必要になります。そのためにはなぜかpythonの再コンパイルを要求されるのでそれを先に行います。よくわからなかったらとりあえず書いてあるとおりにコマンドを打てばOKです。

```
remote$ CFLAGS="-fPIC" pyenv install 3.6.4
pyenv: /home/zuya/.pyenv/versions/3.6.4 already exists
continue with installation? (y/N) yと入力
remote$ pip install mod_wsgi
```

次に設定をいじります。
```
remote$ sudo vim /etc/httpd/conf.modules.d/mod_wsgi.conf

(vimで次の文を追記して保存。mod_wsgiの場所は頑張って探して各自置換すること）
LoadModule wsgi_module /home/zuya/djvenv/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so
```

```
remote$ sudo vim /etc/httpd/conf.d/django.conf

(vimで次の文を追記して保存。mod_wsgiの場所は頑張って探して各自置換すること）
WSGIPythonHome /home/zuya/djvenv
WSGIScriptAlias / /home/zuya/penguin/penguin/wsgi.py
WSGIPythonPath /home/zuya/penguin

<Directory /home/zuya/penguin/penguin>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

```
remote$ sudo vim /etc/sysconfig/httpd

(以下追加して保存)
LD_PRELOAD=/usr/lib64/libutil.so
LD_LIBRARY_PATH=/home/zuya/djvenv/lib

export LD_PRELOAD
export LD_LIBRARY_PATH
```

```
remote$ sudo chmod 755 /home/zuya
```

最後に一度apacheを再起動します。
``` 
remote$ sudo systemctl restart httpd
```

webブラウザにIPアドレスを入力するとこのような画面が表示されます。
![i3](i3.png)

これでapacheとpythonを接続することに成功しました。お疲れ様でした。
* このDocumentationは若林がたくさんハマった結果なんとか得られた最適解とは限らない解です。予想外のエラーが出た際は```sudo vim /var/log/httpd/error_log```で出力されるlogを読むなどして対処してください。

# 6. MariaDBをdjangoに接続する
## 1. PENGUINが扱うデータベースの作成
まずpythonがデータベースを扱うために必要なものをインストールします。
```
remote$ pip install PyMySQL
```
次にMariaDBにログインしてPENGUIN用のDBなどを作ります。
```
remote$ mysql -u root -p
Enter password: (DBのrootのパスワードを入力)
> CREATE DATABASE IF NOT EXISTS (データベース名) DEFAULT CHARACTER SET utf8;
> GRANT ALL ON (データベース名).* to (ユーザー名)@localhost identified by '(パスワード)';
```
ここではデータベース名を```penguin_db```、ユーザーを```penguin```とします。
* rootの他にpenguin_db専用のユーザーを作成しました。PENGUIN専用のデータベースをrootがいじるのは非常に危険だからです。

## 2. settings.pyの最適化（DB対応/設定分離)
```
remote$ vim penguin/settings.py

(vimで編集します。まずSECRET_KEYをファイル外に記録してから削除してください。)
(次にDATABASEの設定も削除して次のように書き換えます。)

from socket import gethostname
from os import environ

HOSTNAME = gethostname()

if (ローカルPCのホスト名) in HOSTNAME:
        from . import settings_local

        SECRET_KEY = settings_local.SECRET_KEY
        DEBUG = settings_local.DEBUG
        DATABASES = {
                'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                 }
        }


else:                    
        import pymysql    
        from . import settings_server

        pymysql.install_as_MySQLdb()

        SECRET_KEY = settings_server.SECRET_KEY
        DEBUG = settings.server.DEBUG
        DATABASES = {'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'penguin_db',
                'USER': 'penguin',
                'PASSWORD': settings_server.DB_PASSWORD,
                'HOST':'',
                'OPTIONS': {
			    	'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
			    },
            }
        }
```

次にこのようなファイルを作成します。
```
remote$ vim penguin/settings_local.py

SECRET_KEY = '(先程記録したSECRET_KEYを記入)'
DEBUG = True
```

```
remote$ vim penguin/settings_server.py

SECRET_KEY = '(先程記録したSECRET_KEYを記入)'
DEBUG = False
DB_PASSWORD = '(DBのユーザーpenguinのパスワードを記入)
```
これら2つのファイルは漏洩したら困るので例えばgit管理する際に.gitignoreに含めるなど、慎重に取り扱ってください。

次のコマンドを実行してエラーを吐かなければ成功です。
```
remote$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  No migrations to apply.
```

# 7. 静的ファイルの配信
「静的ファイル」とはcssファイルなどを指します。これをdjangoが読めるようにします。
```
remote$ sudo vim /etc/httpd/conf/httpd.conf
(以下追加)
Alias /static/ /home/zuya/penguin/static/

<Directory /home/zuya/penguin/static>
        Require all granted
</Directory>

Alias /media/ /home/zuya/penguin/media/

<Directory /home/zuya/penguin/media>
        Require all granted
</Directory>
```

```
remote$ sudo vim /home/zuya/penguin/penguin/settings.py
（以下追加)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

```
remote$ python manage.py collectstatic
```

以上で環境構築は完了です。お疲れ様でした。