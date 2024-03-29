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
    guild = client.get_guild(int(GUILD_ID))
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
                    ],
                    guild_ids=[])
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
                    ],
                    guild_ids=[])
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
                    ],
                    guild_ids=[])
async def nick(ctx, raw_nick):
    if re.search(r'（Ｎｏ．[０-９]+）', raw_nick):
        await ctx.send(f'そのニックネームには変更できません。')
        return
    nick = raw_nick + re.search(r'（Ｎｏ．[０-９]+）$', ctx.author.nick).group()
    await ctx.author.edit(nick=nick)
    await ctx.send(f'あなたのニックネームを {ctx.author.mention} に変更しました')


@client.event
async def on_slash_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    print(''.join(traceback.TracebackException.from_exception(orig_error).format()))
    await ctx.send(f"エラーだにゃ\n```\n{orig_error}\n```")


@slash_client.slash(name="setnumbers",
                    description='ナンバリングの末端を変更します。',
                    options=[
                        create_option(
                            name="number",
                            description="新しいナンバリング",
                            option_type=4,
                            required=True
                        )
                    ],
                    guild_ids=[])
async def set_numbers(ctx, number):
    global numbers
    numbers = number
    await ctx.send(f'ナンバリングの末端を{numbers}に設定しました。\n' +
                   f'サーバに参加した方にはニックネームの後ろに（Ｎｏ．{get_fullwidth_next_number()}）が付与されます。')


@slash_client.slash(name="getnumbers",
                    description='ナンバリングの末端を取得します。',
                    guild_ids=[])
async def get_numbers(ctx):
    await ctx.send(f'サーバに参加した方にはニックネームの後ろに（Ｎｏ．{get_fullwidth_next_number()}）が付与されます。')


@client.event
async def on_member_join(member):
    global numbers
    if not member.bot:
        await member.edit(nick=f'{member.name}（Ｎｏ．{get_fullwidth_next_number()}）')
        numbers += 1


@client.event
async def on_message(message):
    # raise the channel
    if message.author.bot:
        return
    if message.channel.category_id != 790197627311357953:
        # 790197627311357953 は「製作中の言語」カテゴリIDです。
        return
    guild = client.get_guild(int(GUILD_ID))
    top_channel = guild.get_channel(879654804039819304)
    # 879654804039819304 は「受け取りテスト」のチャンネルIDです。
    # 「受け取りテスト」を基準に位置を決めます。
    # text_channel.position がネット上（特にQiita）にある日本語の資料と微妙に違う挙動をするので、気をつけてください。
    # 詳しくは以下の issue を参照のこと。
    # https://github.com/Rapptz/discord.py/issues/2392
    new_position = top_channel.position + 1
    if message.channel.position > new_position:
        await message.channel.edit(position=new_position)

client.run(TOKEN)
