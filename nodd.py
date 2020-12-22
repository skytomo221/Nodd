import discord
import re
from discord.ext import commands

TOKEN = 'TOKEN'

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('ログインしました')


@client.command(help='Reply nyan')
async def neko(ctx, *args):
    if len(args) == 0:
        await ctx.send('にゃーん')
    else:
        await ctx.send(''.join(args) + 'にゃん')


@client.command(pass_context=True, help='Change your nickname')
async def nick(ctx, raw_nick):
    nick = raw_nick + re.search(r'（Ｎｏ．[０-９]+）', ctx.author.nick).group()
    await ctx.author.edit(nick=nick)
    await ctx.send(f'あなたのニックネームを {ctx.author.mention} に変更しました')

client.run(TOKEN)
