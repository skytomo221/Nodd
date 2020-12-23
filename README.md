# Nodd

![image](https://user-images.githubusercontent.com/18415838/102994566-a6a6e880-4562-11eb-9a7b-fcd873ff54f3.png)

Nodd（ノッド）はDiscordメンバーのニックネームにナンバーを振ります。
主に日本言語製作共同研究会で使われています。

## 主な機能

- `.getnum` ナンバリングを取得します。
- `.help` ヘルプを表示します。
- `.neko` にゃーんと返事します。
- `.nick` ニックネームを変更します。
- `.setnum` ナンバリングを設定します。

## セットアップ

1. [ここ](https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8#10-bot%E3%81%AB%E6%A9%9F%E8%83%BD%E3%82%92%E8%BF%BD%E5%8A%A0)を参考にHerokuにデプロイしてください。
2. Config Varsは以下の通りに設定してください。

|KEY|VALUE|
|:-:|:-:|
|DISCORD_NODD_BOT_TOKEN|ボットのアクセストークン|
|DISCORD_NODD_GUILD_ID|ボットを運用するサーバID|
