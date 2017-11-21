# このソフトウェアについて

sys.modules[key]にclassインスタンスを代入して複数回それをimportしてもインスタンス初期化されないことを確認した。

2回importしたら1回目の属性設定が消えるのでは？という懸念があったが、同一モジュールは1回しかimportされず問題なかった。

## 前回

* https://github.com/ytyaru/Python.Const.201709132215

# 実行

```sh
$ python 0.py
```

# 問題

Pythonでreadonlyな定数を作りたい。

# 解法

## 1. __setattr__で再代入禁止する

const.py
```python
class _const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if name in self.__dict__.keys(): raise self.ConstError('readonly。再代入禁止。')
        self.__dict__[name]=value
```

1. objectクラスの`__setattr__`メソッドを継承する（属性を設定するときに実行される）
1. `__setattr__`で属性名が既存ならエラーにする

`_const`クラスのインスタンス属性に2度目の代入をしようとすると例外発生する。

```python
inst = _const()
inst.attr = 'a'
inst.attr = 'a' # ConstError
```

以下の問題が残るが、以降で解決する。

* インスタンスを生成せねばならないのが面倒
* 全体で1つだけにしたい


## 2. moduleにclassインスタンスを代入する

const.py
```python
class _const: ...
import sys
sys.modules[__name__]=_const()
```

`sys.modules[__name__]=_const()`で、`const.py`モジュールに`_const`クラスのインスタンスを代入している。

0.py
```python
import const
print(const, type(const)) #<const._const object at 0xb712932c> <class 'const._const'>
```

`$ python 0.py`で実行すると、上記の通り、モジュールにclassインスタンスが代入される。

もしconstがモジュールなら、以下のように表示されていたはずである。

```
<module 'const' from '/.../const.py'> <class 'module'>
```

### [sys.modules](https://docs.python.jp/3/library/sys.html#sys.modules)

`sys.modules`の操作は[Python文書](https://docs.python.jp/3/library/sys.html#sys.modules)によると、真っ当ではないらしい。でも今回のようなトリック操作ができる。

> 既に読み込まれているモジュールとモジュール名がマップされている辞書です。これを使用してモジュールの強制再読み込みやその他のトリック操作が行えます。ただし、この辞書の置き換えは想定された操作ではなく、必要不可欠なアイテムを削除することで Python が異常終了してしまうかもしれません。

## 3. classインスタンスの属性を動的生成する

```python
import const
const.attr = 'value'
const.attr = 'value'
```

2の通り、constはモジュールではなく、`const._const`クラスのインスタンスである。

1の通り、2度めの代入で例外が発生する。

これにてreadonlyな定数の実装が可能となる。間違って既存の名前で代入しようとするとエラーになる。

ただ、新規生成(定義)は1つのファイル内でやらないと名前重複が探しづらくなる。別々のファイルで定義すると、どのファイルで定義しているか見つけられなくなる。

# 今回の本題

以下の疑問が生じたので試した。結果、問題なかった。

## 2回importしたら1回目の属性設定が消えるのでは？

2回importしたら2回`sys.modules[__name__]=_const()`が実行されてしまうのではないか？

`_const()`によりインスタンスは新しいものが生成され、`=`式で代入され、これまでの`_const`インスタンスとそれに代入していた属性は消えてしまうのでは？

const.py
```python
print('***** import start const.py ****')
...
import sys
sys.modules[__name__]=_const()
print('***** import end const.py ****')
```

0.py
```python
import const
...
import const
```

* `***** import start const.py ****`は1回しか表示されなかった

0.py
```python
import const
const.test = "Test"

import const
const.test = "Test"
```

* 2回目のimport文のあとで、その前に作った属性に代入すると例外が発生した

### 同一mouduleは1回しかimportされない

思い通りに動作している。上記の結果から「同一moduleは1回しか`import`されない」ということなのか？

`import`文の回数だけ実行されるのでは？

以下の検証でも1回のみだった。

* main.py
* const.py
* sub.py

main.py
```python
import sub
import const
print(const, type(const))
import const
```
sub.py
```python
import const
```
const.py
```python
print('CONST!')
```

* 同一module内で2回、同一moduleをimportする
* 異なるmoduleをまたいで同一moduleをimportする

実行しても、`CONST!`の表示は1回だけだった。

```sh
$ python main.py
CONST!
```

「同一mouduleは1回しかimportされない」ということだろう。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [pyenv](https://github.com/pylangstudy/201705/blob/master/27/Python%E5%AD%A6%E7%BF%92%E7%92%B0%E5%A2%83%E3%82%92%E7%94%A8%E6%84%8F%E3%81%99%E3%82%8B.md) 1.0.10
    * Python 3.6.1

# ライセンス

* https://sites.google.com/site/michinobumaeda/programming/pythonconst

Library|License|Copyright
-------|-------|---------
http://code.activestate.com/recipes/65207/|[PSF](https://ja.osdn.net/projects/opensource/wiki/licenses%2FPython_Software_Foundation_License)|Copyright (c) 2001 Python Software Foundation; All Rights Reserved
