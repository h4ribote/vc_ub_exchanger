import discord
from discord import app_commands
import commands as cmds
import config

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'" {client.user} "としてログイン中')
    await client.change_presence(activity=discord.Game(name="vc_ub_exchanger made by h4ribote"),status=discord.Status.online)
    await tree.sync()

@client.event
async def on_message(message:discord.Message):
    if message.content.startswith(f"<@{client.user.id}>") and message.author.id in config.admin_user_id:
        if message.content.split(' ')[1] == "kill":
            await client.close()
            await client._connection.close()
            exit()

@tree.command(name="help",description="主要なコマンドの使い方を表示します")
async def help_command(interaction:discord.Interaction):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(embed=cmds.bot_help())

@tree.command(name="withdrawable",description="現在の出金可能残高を表示します")
async def withdrawable_command(interaction:discord.Interaction):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(embed=cmds.withdrawable())

@tree.command(name="deposit",description="UnbelievaBoatに入金します")
@app_commands.describe(amount="入金数量")
async def deposit_command(interaction:discord.Interaction, amount:int):
    await interaction.response.defer(thinking=True,ephemeral=True)
    await interaction.followup.send(embed=cmds.deposit(interaction.user.id,amount),ephemeral=True)

@tree.command(name="confirm",description="入金処理を確認します")
@app_commands.describe(claim_id="VirtualCrypto上での請求id")
async def confirm_deposit_command(interaction:discord.Interaction, claim_id:int):
    await interaction.response.defer(thinking=True,ephemeral=True)
    await interaction.followup.send(embed=await cmds.confirm_deposit(interaction.user.id,claim_id),ephemeral=True)

@tree.command(name="withdraw",description="UnbelievaBoatから出金します")
@app_commands.describe(amount="出金数量")
async def withdraw_command(interaction:discord.Interaction, amount:int):
    await interaction.response.defer(thinking=True,ephemeral=True)
    await interaction.followup.send(embed= await cmds.withdraw(interaction.user.id,amount),ephemeral=True)

@tree.command(name="withdraw_all",description="ボットが所有している全通貨を引き出します(adminに指定されているユーザーのみ)")
async def withdraw_all_command(interaction:discord.Interaction):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(embed=cmds.withdraw_all(interaction.user.id))

client.run(config.bot_token)
