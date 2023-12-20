import discord
from discord.ext import commands
from discord import app_commands
from datetime import date
import json

def load_name_map():
    with open('name_map.json', 'r', encoding='utf-8') as f:
        name_map = json.load(f)
    return name_map

def save_name_map(name_map):
    with open('name_map.json', 'w', encoding='utf-8') as f:
        json.dump(name_map, f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

n = 1
name_map = {}

@bot.event
async def on_ready():
    activity = discord.Game(name="Netflix", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print('[!] 실행 성공')
    await bot.tree.sync()
    global name_map, n
    name_map = load_name_map()
    n = len(name_map.keys()) + 1

#Ping
@bot.tree.command(name="ping", description="ping! pong!")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("pong!")

#익명메세지
@bot.tree.command(name="익명메세지", description="익명메세지를 보낼 수 있습니다.")
@app_commands.describe(msg='message')
async def say(interaction: discord.Interaction, msg: str):
    global name_map, n
    if len(msg) < 5:
        await interaction.response.send_message('메세지가 너무 짧아요. 5글자를 넘겨주세요.', ephemeral=True)
    else:
        await interaction.response.send_message('Success!', ephemeral=True)
        if str(interaction.user.id) not in name_map.keys():
            name_map[str(interaction.user.id)] = n
            n = n + 1
        save_name_map(name_map)
        embed = discord.Embed()
        embed.add_field(name=f"익명 {name_map[str(interaction.user.id)]}", value=msg, inline=False)
        await interaction.channel.send(embed=embed)

#유저 아바타 다운로드
@bot.tree.context_menu(name='Get avatar')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    php = member.avatar
    embed = discord.Embed(title="download", url=php)
    embed.set_author(name=member.name, icon_url=php)
    embed.set_image(url=php)
    embed.set_footer(text=f"requester: {interaction.user.name}")
    await interaction.response.send_message('Success!', ephemeral=True)
    await interaction.channel.send(embed=embed)

@bot.tree.command(name='궁합')
@app_commands.describe(arg1='arg1', arg2='arg2')
async def comp(interaction: discord.Integration, arg1: str, arg2: str):
    def calculate_compatibility(str1, str2):
        sum_str1 = sum(ord(char) for char in str1)
        sum_str2 = sum(ord(char) for char in str2)
        compatibility_value = sum_str1 + sum_str2
        normalized_compatibility = min(compatibility_value / (len(str1) + len(str2)) / 2, 100)
        return int(normalized_compatibility)
    
    await interaction.response.send_message(calculate_compatibility(arg1, arg2), ephemeral=True)

with open('token.txt', 'r', encoding='utf8') as f:
    token = f.readline()
bot.run(token)