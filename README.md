# post_news_in_line

Line Notifyを使ってニュースを配信するAPI
・例としてあるローカル新聞のニュースを取得しています

## 準備
・アクセストークンを格納するiniファイルが必要です。

フォーマット例
```
[line-notify]
token={発行したtoken}
```

・下記のパッケージが必要です。
```
pip install beautifulsoup4
pip install schedule
```

・newsクラスを継承し、`track`メソッドをオーバーライドしてそれぞれのサイトを元にタグ情報を取得すると良いです。

・スケジューラーはschedule (https://schedule.readthedocs.io/en/stable/) を参考にするとlauncherのタイミングを変更できます。

## 起動

・上記でトークン用のiniファイルパスをパラメータに付け加えると完了

```
python ***.ini
```