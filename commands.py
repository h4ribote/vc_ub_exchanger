import config
import unbelievaboat
import virtualcrypto
import json
from discord import Embed, Colour

vcscopes = [virtualcrypto.Scope.Pay, virtualcrypto.Scope.Claim]
vcclient = virtualcrypto.VirtualCryptoClient(client_id=config.vc_client_id,client_secret=config.vc_secret,scopes=vcscopes)

def embed_Error(title:str,description:str):
    embed = Embed()
    embed.colour = Colour.from_rgb(234,56,118)
    embed.title = title
    embed.description = description
    return embed

def embed_Success(title:str,description:str):
    embed = Embed()
    embed.colour = Colour.from_rgb(56,234,65)
    embed.title = title
    embed.description = description
    return embed

def embed_Yellow(title:str,description:str):
    embed = Embed()
    embed.colour = Colour.from_rgb(255,223,88)
    embed.title = title
    embed.description = description
    return embed

def bot_help():
    embed = Embed()
    embed.colour = Colour.from_rgb(88,185,255)
    embed.title = "各種コマンド"
    embed.add_field(name="deposit [入金数量]",value="指定された数量をUnbelievaBoatに入金するための請求をVirtualCryptoで発行します",inline=False)
    embed.add_field(name="confirm [VirtualCryptoの請求id]",value="`/deposit`で発行された請求を支払ったあとに該当idを入力し実行することで入金処理が行われます",inline=False)
    embed.add_field(name="withdraw",value="UnbelievaBoatから指定された数量を出金します\n(出金したい残高は銀行に移してください)",inline=False)
    embed.add_field(name="withdrawable",value="現時点で出金が可能な最大数量を表示します",inline=False)
    return embed

def withdrawable():
    available_currency = vcclient.get_currency_by_unit(config.vc_currency_unit)
    withdrawable_bal = 0
    for bal in vcclient.get_balances():
        if bal.currency.unit == available_currency.unit:
            withdrawable_bal = bal.amount
            break
    embed = Embed()
    embed.colour = Colour.from_rgb(88,185,255)
    embed.add_field(name="出金可能残高",value=f"{withdrawable_bal} {available_currency.unit}",inline=False)
    embed.add_field(name="対応通貨",value=f"`{available_currency.name}` ({available_currency.unit})",inline=False)
    return embed

def deposit(user_id:int, amount:int):
    if amount < 1:
        return embed_Error("処理に失敗しました", "`amount`は1以上の整数を入力してください")
    response = vcclient.post(path="/users/@me/claims",data={"payer_discord_id":user_id,"unit":config.vc_currency_unit,"amount":amount}).json()
    claim_id = int(response['id'])
    return embed_Yellow("請求の発行完了", f"VirtualCrypto上で請求の承認を行ってください\n ` /claim show id:{claim_id} `\n"
                                         f"承認後、` /confirm claim_id:{claim_id} `を実行してください")

async def confirm_deposit(user_id:int, claim_id:int):
    try:
        with open('confirmed_id.json') as f:
            confirmed_id_list:list[int] = json.load(f)
    except FileNotFoundError:
        confirmed_id_list:list[int] = []
    if claim_id in confirmed_id_list:
        return embed_Error("処理に失敗しました", "すでに入金が完了しています")
    
    try:
        deposit_claim = vcclient.get_claim(claim_id)
    except:
        return embed_Error("処理に失敗しました", "存在しない、もしくは無効な請求idです")
    if deposit_claim.payer.discord.id != user_id:
        return embed_Error("処理に失敗しました", "存在しない、もしくは無効な請求idです")
    if deposit_claim.status != virtualcrypto.ClaimStatus.Approved:
        return embed_Error("処理に失敗しました", "請求は承認されていません")
    
    UBClient = unbelievaboat.Client(config.unbelievaboat_secret)
    await UBClient.update_user_balance(config.guild_id,user_id,bank=deposit_claim.amount,reason=f"VirtualCrypto deposit(deposit_id: {deposit_claim.id})")
    
    confirmed_id_list.append(deposit_claim.id)
    with open('confirmed_id.json', 'w') as f:
        json.dump(confirmed_id_list, f, indent=1)

    embed = Embed()
    embed.colour = Colour.from_rgb(56,234,65)
    embed.title = "入金完了"
    embed.add_field(name="入金数量",value=f"{deposit_claim.amount} {config.vc_currency_unit}",inline=False)
    embed.add_field(name="請求id",value=f"{deposit_claim.id}",inline=False)
    return embed

async def withdraw(user_id:int, amount:int):
    if amount < 1:
        return embed_Error("処理に失敗しました", "`amount`は1以上の整数を入力してください")
    
    UBClient = unbelievaboat.Client(config.unbelievaboat_secret)
    guild:unbelievaboat.Guild = await UBClient.get_guild(config.guild_id)
    ubuser:unbelievaboat.UserBalance = await guild.get_user_balance(user_id)

    if ubuser.bank < amount:
        return embed_Error("処理に失敗しました", "銀行の残高が不足しています")
    
    withdrawable_bal = None
    for bal in vcclient.get_balances():
        if bal.currency.unit == config.vc_currency_unit:
            withdrawable_bal = bal.amount
            break
    
    if not withdrawable_bal or withdrawable_bal < amount:
        return embed_Error("処理に失敗しました",
                          f"現在の出金可能な残高({withdrawable_bal} {config.vc_currency_unit})を超過しています\n出金数量を減らすか、ボットの残高を追加してください")
    
    await ubuser.update(bank=-amount,reason=f"VirtualCrypto withdraw")

    vcclient.create_user_transaction(config.vc_currency_unit, user_id, amount)

    embed = Embed()
    embed.colour = Colour.from_rgb(56,234,65)
    embed.title = "出金完了"
    embed.add_field(name="出金数量",value=f"{amount} {config.vc_currency_unit}",inline=False)
    return embed

def withdraw_all(user_id:int):
    if not user_id in config.admin_user_id:
        return embed_Error("無効な操作","このコマンドを使用する権限がありません")
    
    withdrawed = 0
    withdrawed_amount = 0
    for bal in vcclient.get_balances():
        vcclient.create_user_transaction(bal.currency.unit, user_id, bal.amount)
        withdrawed += 1
        withdrawed_amount += bal.amount
    
    return embed_Success("出金完了",f"{withdrawed}個, {withdrawed_amount}枚を引き出しました",inline=False)
