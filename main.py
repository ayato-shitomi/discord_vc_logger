# 必須ライブラリをインポート
from dataclasses import replace
from os import sync
import discord
from datetime import datetime, timedelta


# tokenファイルを読みこみ、内容を返す
# 第一引数にトークンのファイルパスを取る
def getToken(filePath):
	f = open(filePath, 'r', encoding="UTF-8")
	data = f.read()
	f.close()
	return data


# トークンと環境変数等を取得する
TOKEN = getToken("token")
SERVER_ID = <サーバーID>
TXT_ID = <テキストID>
DBGMSG = "BOTはオンラインです。"
print("Success > Got token and SERVER and TEXT ID.")

client = discord.Client()

# クライアントクラスを作成する
@client.event
async def on_ready():
	print("Success > Login.")

# ボイスチャットに変化があった際のイベント
@client.event
async def on_voice_state_update(member, before, after):
	print("Info > Event was called.")
	if member.guild.id == SERVER_ID:
		if before.channel != after.channel:
			now = datetime.utcnow() + timedelta(hours=9)
			alert_channel = client.get_channel(TXT_ID)
			if before.channel is None:
				msg = f"== {now:%m/%d %H:%M} ==\n{member.name} さん <#{after.channel.id}> へようこそ！"
				print("Info > " + msg.replace("\n", " "))
				await alert_channel.send(msg)
			elif after.channel is None:
				msg = f"== {now:%m/%d %H:%M} ==\n{member.name} さん <#{before.channel.id}> へまた来てね！"
				print("Info > " + msg.replace("\n", " "))
				await alert_channel.send(msg)

# デバッグ用
@client.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は何もしない
	if message.author.bot:
		return
	# 「/botdbg」コマンド
	if message.content == "/botdbg":
		print("Info > " + DBGMSG)
		await message.channel.send(DBGMSG)

# クライアントクラスを実行する。
client.run(TOKEN)