# vc_ub_exchanger

## 何これ
VirtualCrypto、UnbelievaBoat間の送金するためのdiscordボットをパパッとセットアップできるやつ

## セットアップ
- requirements.txt
```
pip install -r requirements.txt
```

- [VirtualCrypto](https://vcrypto.sumidora.com/me)と[UnbelievaBoat](https://unbelievaboat.com/applications)でidやらシークレットやらを取得
  - VirtualCrypto  
    1: 「新規アプリケーション」を選択して新規アプリケーションを作成し、色々入力  
    2: Discord Botと紐つける  
    3: クライアントIDは`vc_client_id`に、クライアントシークレットは`vc_secret`にコピペ  
  - UnbelievaBoat  
    1: My Applications > New application  
    2: TOKENを`unbelievaboat_secret`にコピペ  

- config.pyに設定を記述
  - guild_id: ボットを動かすサーバーのid
  - vc_currency_unit: 入出金対象の通貨のUnit(通貨単位) UnbelievaBoatの通貨と1対1で交換する
  - admin_user_id: 管理者のユーザーidのリスト 現時点では`/withdraw_all`(所有する通貨をすべて引き出す)コマンドが使用可

- main.pyを実行
```
python main.py
```
- VirtualCryptoから対象のボットに通貨を補充
  - 交換比率が1対1のため、ユーザーがギャンブルで爆勝ちすると準備金が不足してVirtualCrypto側に移せない事態が発生する可能性があるので注意

## 注意書きみたいなやつ
virtualcryptoの[client.py 167行目](https://github.com/h4ribote/vc_ub_exchanger/blob/main/virtualcrypto/client.py#L167)がオリジナルのやつだとなんか動かなかったので勝手に書き換えてます  
元のほうのコードで動いたやつ、至急、メールくれや。  

## To do
- 寝る
