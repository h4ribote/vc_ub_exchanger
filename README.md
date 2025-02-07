# vc_ub_exchanger

## 何これ
VirtualCrypto、UnbelievaBoat間の送金するためのdiscordボットをパパッとセットアップできるやつ

## 使い方
- requirements.txt
```
pip install -r requirements.txt
```

- [VirtualCrypto](https://vcrypto.sumidora.com/me)と[UnbelievaBoat](https://unbelievaboat.com/applications)でidやらシークレットやらを取得

- config.pyに設定を記述
  - guild_id: ボットを動かすサーバーのid
  - vc_currency_unit: 入出金対象の通貨のUnit(通貨単位) UnbelievaBoatの通貨と1対1で交換する
  - admin_user_id: 管理者のユーザーidのリスト 現時点では`/withdraw_all`(所有する通貨をすべて引き出す)コマンドが使用可

- main.pyを実行
```
python main.py
```

## 注意書きみたいなやつ
virtualcryptoの[client.py 167行目](https://github.com/h4ribote/vc_ub_exchanger/blob/main/virtualcrypto/client.py#L167)がオリジナルのやつだとなんか動かなかったので勝手に書き換えてます  
元のほうのコードで動いたやつ、至急、メールくれや。  

## To do
- 寝る
