import os
import re
import sys

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from asyncio.exceptions import CancelledError
import traceback

TOKEN = os.environ['DISCORD_NODD_BOT_TOKEN']
GUILD_ID = os.environ['DISCORD_NODD_GUILD_ID']
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
numbers = 0


def get_fullwidth_next_number() -> str:
    global numbers
    return str(numbers + 1).translate(str.maketrans(
        {chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


slash_client = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    global numbers
    print('ログインしました')
    print(f"GUILD_ID={GUILD_ID}")
    guild = client.get_guild(GUILD_ID)
    numbers = 0 if guild == None else guild.member_count
    print(f'guild={guild}')
    print(f'numbers={numbers}')


@slash_client.slash(name="neko",
                    description='Noddくんが生きているか判定します。',
                    options=[
                        create_option(
                            name="text",
                            description="Noddくんに言わせるセリフ",
                            option_type=3,
                            required=False
                        )
                    ])
async def neko(ctx, text=''):
    if len(text) == 0:
        await ctx.send('にゃーん')
    else:
        await ctx.send(''.join(text).replace('な', 'にゃ') + 'にゃ', allowed_mentions=None)


@slash_client.slash(name="python",
                    description='任意のPythonコードを実行します。',
                    options=[
                        create_option(
                            name="command",
                            description="実行する命令",
                            option_type=3,
                            required=True
                        )
                    ])
async def python(ctx, command: str):
    if (len(command) - len(command.replace('_', '')) > 10):
        await ctx.send(f"そのコードはセキュリティ上の問題で実行しにゃいにゃ！")
    else:
        await ctx.send(f"```python\n>>> {command}\n{eval(command, {'__builtins__': None})}```")


@slash_client.slash(name="nick",
                    description='ニックネームを変更します。',
                    options=[
                        create_option(
                            name="raw_nick",
                            description="新しいニックネーム",
                            option_type=3,
                            required=True
                        )
                    ])
async def nick(ctx, raw_nick):
    if re.search(r'（Ｎｏ．[０-９]+）', raw_nick):
        await ctx.send(f'そのニックネームには変更できません。')
        return
    nick = raw_nick + re.search(r'（Ｎｏ．[０-９]+）$', ctx.author.nick).group()
    await ctx.author.edit(nick=nick)
    await ctx.send(f'あなたのニックネームを {ctx.author.mention} に変更しました')


@client.command(help='Set member index', name='setnum')
async def set_members(ctx, index):
    global numbers
    numbers = ctx.guild.member_count if index == 'auto' else int(index)
    await ctx.send(f'ナンバリングの末端を{numbers}に設定しました。\n' +
                   f'サーバに参加した方にはニックネームの後ろに（Ｎｏ．{get_fullwidth_next_number()}）が付与されます。')


@client.command(help='Get member index', name='getnum')
async def get_members(ctx):
    await ctx.send(f'サーバに参加した方にはニックネームの後ろに（Ｎｏ．{get_fullwidth_next_number()}）が付与されます。')


@client.event
async def on_member_join(member):
    global numbers
    if not member.bot:
        member.edit(nick=f'{member.nick}（Ｎｏ．{get_fullwidth_next_number()}）')
        numbers += 1

client.run(TOKEN)
