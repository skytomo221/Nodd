import discord
import re
from discord.ext import commands

TOKEN = None
GUILD_ID = None
client = commands.Bot(command_prefix='.')
numbers = 0

with open('token.txt') as f:
    TOKEN = f.read().strip()
with open('guild_id.txt') as f:
    GUILD_ID = f.read().strip()


def get_fullwidth_next_number() -> str:
    global numbers
    return str(numbers + 1).translate(str.maketrans(
        {chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


@client.event
async def on_ready():
    global numbers
    print('ログインしました')
    print(f"GUILD_ID={GUILD_ID}")
    guild = client.get_guild(GUILD_ID)
    numbers = 0 if guild == None else guild.member_count
    print(f'guild={guild}')
    print(f'numbers={numbers}')


@client.command(help='Reply nyan')
async def neko(ctx, *args):
    if len(args) == 0:
        await ctx.send('にゃーん')
    else:
        await ctx.send(''.join(args) + 'にゃん')


@client.command(pass_context=True, help='Change your nickname')
async def nick(ctx, raw_nick):
    if re.search(r'（Ｎｏ．[０-９]+）', raw_nick):
        await ctx.send(f'そのニックネームには変更できません。')
        return
    nick = raw_nick + re.search(r'（Ｎｏ．[０-９]+）', ctx.author.nick).group()
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
