from discord.ext import commands,tasks
from discord import Webhook, RequestsWebhookAdapter, Embed
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import discord
import asyncio
import os
import keep_alive
import requests
import math
import time
import json
import random
import datetime
import subprocess

client = commands.Bot(command_prefix="bb!")
slash = SlashCommand(client, sync_commands=True)
KEY = os.environ['API_KEY']
client.remove_command('help')

global pickaxes
pickaxes = ["BingCoin Pickaxe", "BingCoin Drill", "Miner x1000", "Miner x1050", "Miner x1060", "Miner x1070", "Miner x1080", "NFT x2000", "NFT x2050", "NFT x2060", "NFT x2070", "NFT x2080", "BTH x3000", "BTH x3050", "BTH x3060", "BTH x3070", "BTH x3080", "BTH x3090"]
global bank_list
bank_list = ["Default Bank", "Amateur Bank", "Professional Bank", "Elite Bank", "NFT Bank", "BTH Bank", "DGE Bank", "DGE Premium"]


def getInfo(call):
    r = requests.get(call)
    return r.json()

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bb!help | by @bing"))

@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.CommandOnCooldown):
    if error.retry_after >= 86400:
      msg = f"**Still on cooldown**, please try again in {error.retry_after/86400:.2f}hr"
    elif error.retry_after >= 60:
      msg = f"**Still on cooldown**, please try again in {error.retry_after/60:.2f}min"
    else:
      msg = f"**Still on cooldown**, please try again in {error.retry_after:.2f}s"
    await ctx.reply(msg)

@client.event
async def on_message(message):
  guild = message.guild
  log_channel = discord.utils.get(guild.channels, name="message-log")
  if log_channel is None:
    await client.process_commands(message)
    return
  if not message.author.bot:
    embed=discord.Embed(title="",color=0xC98FFC, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=message.author.display_name,icon_url=message.author.avatar_url)
    embed.add_field(name=message.content, value=message.channel.mention, inline=False)
    embed.set_footer(text=message.author.id)
    if len(message.attachments) > 0:
      embed.set_image(url = message.attachments[0].url)
    await log_channel.send(embed=embed)
    await client.process_commands(message)
  
@client.command()
async def help(ctx, arg="none"):
  if arg == "none":
    embed = discord.Embed(title="Help Categories", color=0xC98FFC)
    embed.add_field(name="bb!help admin", value="Admin Commands", inline=False)
    embed.add_field(name="bb!help hypixel", value="Hypixel Commands", inline=False)
    embed.add_field(name="bb!help skyblock", value="Hypixel Skyblock Commands", inline=False)
    embed.add_field(name="bb!help fun", value="Random BingBot Commands", inline=False)
    embed.add_field(name="bb!help economy", value="BingCoin Economy Commands", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  elif arg == "admin":
    embed = discord.Embed(title="Admin Commands", color=0xC98FFC)
    embed.add_field(name="bb!purge (AMOUNT)", value="Purge a number of messages in a channel", inline=False)
    embed.add_field(name="bb!curl (WEBHOOK)", value="Find information about a webhook", inline=False)
    embed.add_field(name="bb!delete (WEBHOOK)", value="Delete a webhook", inline=False)
    embed.add_field(name="bb!troll (WEBHOOK) (MESSAGE)", value="Send a troll message to a webhook", inline=False)
    embed.add_field(name="bb!giverole (@USER) (@ROLE)", value="Give a certain user a role and send them a message", inline=False)
    embed.add_field(name="bb!geolocate (IP)", value="Gives general geolocation information about an IP", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  elif arg == "hypixel":
    embed = discord.Embed(title="Hypixel Commands", color=0xC98FFC)
    embed.add_field(name="bb!stats (IGN)", value="Check the general statistics of a player", inline=False)
    embed.add_field(name="bb!duels (IGN)", value="Check the general Dueling statistics of a player", inline=False)
    embed.add_field(name="bb!bedwars (IGN)", value="Check the general Bedwars statistics of a player", inline=False)
    embed.add_field(name="bb!skywars (IGN)", value="Check the general Skywars statistics of a player", inline=False)
    embed.add_field(name="bb!skyblock (IGN)", value="Check the general Skyblock statistics of a player", inline=False)
    embed.add_field(name="bb!skin (IGN)", value="Display's the player's current skin", inline=False)
    embed.add_field(name="bb!ign (UUID)", value="Gets the player's IGN from their UUID", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  elif arg == "fun":
    embed = discord.Embed(title="BingBot Fun Commands", color=0xC98FFC)
    embed.add_field(name="bb!embed (CONTEXT)", value="Creates an embed and outputs the CONTEXT", inline=False)
    embed.add_field(name="bb!number (NUMBER)", value="Displays a random integer from 0-NUMBER", inline=False)
    embed.add_field(name="bb!hello", value="Simply saying hello to the bot", inline=False)
    embed.add_field(name="bb!ping", value="Check the response time of the bot", inline=False)
    embed.add_field(name="bb!penis (NAME)", value="Check a person's penis size", inline=False)
    embed.add_field(name="bb!dox (NAME)", value="Creates a random IP and uses geolocation API to locate it", inline=False)
    embed.add_field(name="bb!logo", value=f"Get {ctx.guild.name}'s Server Icon", inline=False)
    embed.add_field(name="/userinfo mention:/id: (@USER/USER ID)", value="Get information about a user's profile", inline=False)
    embed.add_field(name="bb!members", value=f"Get {ctx.guild.name}'s Member Count", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  elif arg == "skyblock":
    embed = discord.Embed(title="Skyblock Commands", color=0xC98FFC)
    embed.add_field(name="bb!megakloon", value="Check the current skin of Minikloon's alt, Megakloon", inline=False)
    embed.add_field(name="bb!completion (IGN)", value="Check the floor completions of a player in Skyblock", inline=False)
    embed.add_field(name="bb!slayer (IGN)", value="Check the slayer level and xp of a player in Skyblock", inline=False)
    embed.add_field(name="bb!rev (IGN)", value="Check the Revenant Horror kills of a player in Skyblock", inline=False)
    embed.add_field(name="bb!tara (IGN)", value="Check the Tarantula Broodfather kills of a player in Skyblock", inline=False)
    embed.add_field(name="bb!sven (IGN)", value="Check the Sven Packmaster kills of a player in Skyblock", inline=False)
    embed.add_field(name="bb!enderman (IGN)", value="Check the Voidgloom Seraph kills of a player in Skyblock", inline=False)
    embed.add_field(name="bb!essence (IGN)", value="Lists all the essence of the specified player in Skyblock", inline=False)
    embed.add_field(name="bb!weight (IGN)", value="Display's the player's weight according to senither", inline=False)
    embed.add_field(name="bb!skills (IGN)", value="Display's the player's skills and skill average", inline=False)
    embed.add_field(name="bb!bin (ITEM)", value="Display's an item's 'Buy It Now' data", inline=False)
    embed.add_field(name="bb!skycrypt (IGN)", value="Gets a user's Skycrpyt link", inline=False)
    embed.add_field(name="bb!plancke (IGN)", value="Gets a user's Plancke link", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  elif arg == "economy":
    embed = discord.Embed(title="BingCoin Economy Commands", color=0xC98FFC)
    embed.add_field(name="bb!startmining", value="Starts your mining journey", inline=False)
    embed.add_field(name="bb!balance/bal (@USER)", value="Checks balance of another user if @ or yourself without @USER parameter", inline=False)
    embed.add_field(name="bb!networth/worth/nw/nworth (@USER)", value="Checks networth of another user if @ or yourself without @USER parameter", inline=False)
    embed.add_field(name="bb!pickaxe/pick (@USER)", value="Checks pickaxe of another user if @ or yourself without @USER parameter", inline=False)
    embed.add_field(name="bb!mine", value="Mine and receive BingCoin", inline=False)
    embed.add_field(name="bb!shop", value="View all available items for sale", inline=False)
    embed.add_field(name="bb!buy (PICKAXE)", value="Purchases the desired pickaxe", inline=False)
    embed.add_field(name="bb!leaderboard", value="Check BingCoin leaderboard", inline=False)
    embed.add_field(name="bb!bank (@USER)", value="Checks bank of another user if @ or yourself without @USER parameter", inline=False)
    embed.add_field(name="bb!banks", value="Views all available banks", inline=False)
    embed.add_field(name="bb!deposit", value="Deposit BingCoin to your bank", inline=False)
    embed.add_field(name="bb!withdraw", value="Withdraw BingCoin to your bank", inline=False)
    embed.add_field(name="bb!apply (BANK)", value="Puchase a bank to store your BingCoin", inline=False)
    embed.add_field(name="bb!rob (@USER)", value="Rob a user of their BingCoin in their wallet", inline=False)
    embed.add_field(name="bb!ranks (@USER)", value="View all available ranks", inline=False)
    embed.add_field(name="bb!rank (@USER)", value="Checks rank of another user if @ or yourself without @USER parameter", inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
  else:
    embed = discord.Embed(title="Error", description="Invalid Parameter")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@client.command()
async def ping(ctx):
    await ctx.send('Response time: {0}ms'.format(round(client.latency, 1)))
@client.command()
async def logo(ctx):
  embed=discord.Embed(title=ctx.guild.name, color=0xC98FFC)
  embed.set_image(url=ctx.guild.icon_url)
  await ctx.send(embed=embed)

@client.command()
async def megakloon(ctx):
    embed = discord.Embed(title=f"Megakloon's Current Skin", color=0xC98FFC)
    embed.set_image(url=f"https://crafatar.com/renders/body/41d3abc2d749400c9090d5434d03831b")
    await ctx.send(embed=embed)

@client.command()
async def stats(ctx, name):
    try:
      user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
      uuid = user_name["id"]
      link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
      data = getInfo(link)

      embed = discord.Embed(title=f"{name}'s Hypixel Statistics", color=0xC98FFC)
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url=f"https://crafatar.com/renders/head/{uuid}")
      embed.add_field(name="Karma:", value="{:,}".format(data['player']['karma']))
      embed.add_field(name="Network XP:", value="{:,.2f}".format(data['player']['networkExp']))
      rank = data['player']['newPackageRank']
      if "_" in rank:
          rank = rank.replace("_PLUS","+")
      if "MVP" in rank:
          if data['player']['monthlyPackageRank'] != "NONE":
              rank = rank + "+"
      embed.add_field(name="Hypixel Rank:", value=f"{rank}")
      level = ((math.sqrt(data['player']['networkExp'] + 15312.5) - (125/math.sqrt(2))) / 25 * math.sqrt(2)) / 2
      embed.add_field(name="Hypixel Level:", value="{:.2f}".format(level))
    except:
      embed = discord.Embed(title="Error", description="Invalid IGN")
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def duels(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)

        embed = discord.Embed(title=f"{name}'s Duels Statistics", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Games Played:", value="{:,.0f}".format(data['player']['stats']['Duels']['games_played_duels']))
        embed.add_field(name="Coins:", value="{:,.0f}".format(data['player']['stats']['Duels']['coins']))
        embed.add_field(name="Melee Swings:", value="{:,.0f}".format(data['player']['stats']['Duels']['melee_swings']))
        embed.add_field(name="Wins:", value="{:,.0f}".format(data['player']['stats']['Duels']['wins']))
        embed.add_field(name="Losses:", value="{:,.0f}".format(data['player']['stats']['Duels']['losses']))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
    await ctx.send(embed=embed)

@client.command()
async def bedwars(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)

        embed = discord.Embed(title=f"{name}'s Bedwars Statistics", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Games Played:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['games_played_bedwars_1']))
        embed.add_field(name="Experience:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['Experience']))
        embed.add_field(name="Coins:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['coins']))
        embed.add_field(name="Kills:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['kills_bedwars']))
        embed.add_field(name="Deaths:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['deaths_bedwars']))
        embed.add_field(name="Wins:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['wins_bedwars']))
        embed.add_field(name="Losses:", value="{:,.0f}".format(data['player']['stats']['Bedwars']['losses_bedwars']))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def skywars(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        embed = discord.Embed(title=f"{name}'s Skywars Statistics", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Games Played:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['games']))
        embed.add_field(name="Souls:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['souls']))
        embed.add_field(name="Coins:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['coins']))
        embed.add_field(name="Kills:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['kills']))
        embed.add_field(name="Wins:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['wins']))
        embed.add_field(name="Losses:", value="{:,.0f}".format(data['player']['stats']['SkyWars']['losses']))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def completion(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def entrance():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['0']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['0']
            except:
                return 0

        def floor_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['1']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['1']
            except:
                return 0

        def floor_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['2']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['2']
            except:
                return 0

        def floor_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['3']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['3']
            except:
                return 0

        def floor_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['4']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['4']
            except:
                return 0

        def floor_5():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['5']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['5']
            except:
                return 0

        def floor_6():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['6']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['6']
            except:
                return 0

        def floor_7():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['7']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['tier_completions']['7']
            except:
                return 0

        def mm_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['1']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['1']
            except:
                return 0

        def mm_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['2']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['2']
            except:
                return 0

        def mm_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['3']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['3']
            except:
                return 0

        def mm_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['4']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['4']
            except:
                return 0

        def mm_5():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['5']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['5']
            except:
                return 0

        def mm_6():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['6']
                return sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['master_catacombs']['tier_completions']['6']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Floor Completions", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/a/a6/Mort_%28wide%29.png/revision/latest/scale-to-width-down/120?cb=20210828154023")
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Entrance:", value="{:,.0f}".format(entrance()), inline=True)
        embed.add_field(name="Floor 1:", value="{:,.0f}".format(floor_1()),inline=True)
        embed.add_field(name="Floor 2:", value="{:,.0f}".format(floor_2()),inline=True)
        embed.add_field(name="Floor 3:", value="{:,.0f}".format(floor_3()),inline=True)
        embed.add_field(name="Floor 4:", value="{:,.0f}".format(floor_4()),inline=True)
        embed.add_field(name="Floor 5:", value="{:,.0f}".format(floor_5()),inline=True)
        embed.add_field(name="Floor 6:", value="{:,.0f}".format(floor_6()),inline=True)
        embed.add_field(name="Floor 7:", value="{:,.0f}".format(floor_7()),inline=True)
        embed.add_field(name="Mastermode Floor 1:", value="{:,.0f}".format(mm_1()),inline=True)
        embed.add_field(name="Mastermode Floor 2:", value="{:,.0f}".format(mm_2()),inline=True)
        embed.add_field(name="Mastermode Floor 3:", value="{:,.0f}".format(mm_3()),inline=True)
        embed.add_field(name="Mastermode Floor 4:", value="{:,.0f}".format(mm_4()),inline=True)
        embed.add_field(name="Mastermode Floor 5:", value="{:,.0f}".format(mm_5()),inline=True)
        embed.add_field(name="Mastermode Floor 6:", value="{:,.0f}".format(mm_6()),inline=True)
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def slayer(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        senither = f"https://hypixel-api.senither.com/v1/profiles/{uuid}?key={KEY}"
        senither_data = getInfo(senither)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        SPIDER_XP = senither_data['data'][profile_num]['slayers']['bosses']['tarantula']['experience']
        SPIDER_LVL = senither_data['data'][profile_num]['slayers']['bosses']['tarantula']['level']
        REV_XP = senither_data['data'][profile_num]['slayers']['bosses']['revenant']['experience']
        REV_LVL = senither_data['data'][profile_num]['slayers']['bosses']['revenant']['level']
        SVEN_XP = senither_data['data'][profile_num]['slayers']['bosses']['sven']['experience']
        SVEN_LVL = senither_data['data'][profile_num]['slayers']['bosses']['sven']['level']
        ENDER_XP = senither_data['data'][profile_num]['slayers']['bosses']['enderman']['experience']
        ENDER_LVL = senither_data['data'][profile_num]['slayers']['bosses']['enderman']['level']
        COINS_SPENT = senither_data['data'][profile_num]['slayers']['total_coins_spent']

        embed = discord.Embed(title=f"{name}'s Slayer XP and Levels", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/c/c6/Maddox_Batphone.png/revision/latest/scale-to-width-down/300?cb=20210708220524")
        embed.add_field(name="Active Profile:", value=profile_name, inline=False)
        embed.add_field(name="Total Coins Spent:", value=COINS_SPENT, inline=False)
        embed.add_field(name="Revenant Horror: Level {:.0f}", value="Slayer XP: {:,.0f}".format(REV_LVL,REV_XP), inline=False)
        embed.add_field(name="Tarantula Broodfather: Level {:.0f}", value="Slayer XP: {:,.0f}".format(SPIDER_LVL,SPIDER_XP), inline=False)
        embed.add_field(name="Sven Packmaster: Level {:.0f}", value="Slayer XP: {:,.0f}".format(SVEN_LVL,SVEN_XP), inline=False)
        embed.add_field(name="Voidgloom Seraph: Level {:.0f}", value="Slayer XP: {:,.0f}".format(ENDER_LVL,ENDER_XP), inline=False)
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def rev(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def rev_tier_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_0']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_0']
            except:
                return 0

        def rev_tier_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_1']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_1']
            except:
                return 0

        def rev_tier_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_2']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_2']
            except:
                return 0

        def rev_tier_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_3']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_3']
            except:
                return 0

        def rev_tier_5():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_3']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['zombie']['boss_kills_tier_4']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Revenant Horror Kills", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/e/eb/Atoned_Horror.png/revision/latest/scale-to-width-down/312?cb=20210312065431")
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Tier 1 Kills:", value="{:,.0f}".format(rev_tier_1()))
        embed.add_field(name="Tier 2 Kills:", value="{:,.0f}".format(rev_tier_2()))
        embed.add_field(name="Tier 3 Kills:", value="{:,.0f}".format(rev_tier_3()))
        embed.add_field(name="Tier 4 Kills:", value="{:,.0f}".format(rev_tier_4()))
        embed.add_field(name="Tier 4 Kills:", value="{:,.0f}".format(rev_tier_5()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def tara(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def tara_tier_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_0']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_0']
            except:
                return 0

        def tara_tier_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_1']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_1']
            except:
                return 0

        def tara_tier_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_2']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_2']
            except:
                return 0

        def tara_tier_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_3']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['spider']['boss_kills_tier_3']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Tarantula Broodfather Kills", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/8/8b/Tarantula_Broodfather.png/revision/latest/scale-to-width-down/1080?cb=20200425074841")
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Tier 1 Kills:", value="{:,.0f}".format(tara_tier_1()))
        embed.add_field(name="Tier 2 Kills:", value="{:,.0f}".format(tara_tier_2()))
        embed.add_field(name="Tier 3 Kills:", value="{:,.0f}".format(tara_tier_3()))
        embed.add_field(name="Tier 4 Kills:", value="{:,.0f}".format(tara_tier_4()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def sven(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def wolf_tier_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_0']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_0']
            except:
                return 0

        def wolf_tier_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_1']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_1']
            except:
                return 0

        def wolf_tier_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_2']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_2']
            except:
                return 0

        def wolf_tier_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_3']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['wolf']['boss_kills_tier_3']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Sven Packmaster Kills", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/9/98/Angry_Wolf.png/revision/latest/scale-to-width-down/512?cb=20210625230344")
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Tier 1 Kills:", value="{:,.0f}".format(wolf_tier_1()))
        embed.add_field(name="Tier 2 Kills:", value="{:,.0f}".format(wolf_tier_2()))
        embed.add_field(name="Tier 3 Kills:", value="{:,.0f}".format(wolf_tier_3()))
        embed.add_field(name="Tier 4 Kills:", value="{:,.0f}".format(wolf_tier_4()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def enderman(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def ender_tier_1():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_0']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_0']
            except:
                return 0

        def ender_tier_2():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_1']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_1']
            except:
                return 0

        def ender_tier_3():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_2']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_2']
            except:
                return 0

        def ender_tier_4():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_3']
                return sb_data['profiles'][profile_num]['members'][uuid]['slayer_bosses']['enderman']['boss_kills_tier_3']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Voidgloom Seraph Kills", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/2/28/Enderman.png/revision/latest/scale-to-width-down/629?cb=20200209104412")
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Tier 1 Kills:", value="{:,.0f}".format(ender_tier_1()))
        embed.add_field(name="Tier 2 Kills:", value="{:,.0f}".format(ender_tier_2()))
        embed.add_field(name="Tier 3 Kills:", value="{:,.0f}".format(ender_tier_3()))
        embed.add_field(name="Tier 4 Kills:", value="{:,.0f}".format(ender_tier_4()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def skyblock(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        cata_exp = sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['dungeon_types']['catacombs']['experience']

        current_class = sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['selected_dungeon_class']

        class_exp = sb_data['profiles'][profile_num]['members'][uuid]['dungeons']['player_classes'][current_class]['experience']

        def get_cata(exp):
            levels = {'1': 50, '2': 125, '3': 235, '4': 395, '5': 625, '6': 955, '7': 1425, '8': 2095, '9': 3045,
                      '10': 4385, '11': 6275, '12': 8940, '13': 12700, '14': 17960, '15': 25340, '16': 35640,
                      '17': 50040, '18': 70040, '19': 97640, '20': 135640, '21': 188140, '22': 259640, '23': 356640,
                      '24': 488640, '25': 668640, '26': 911640, '27': 1239640, '28': 1684640, '29': 2284640,
                      '30': 3084640, '31': 4149640, '32': 5559640, '33': 7459640, '34': 9959640, '35': 13259640,
                      '36': 17559640, '37': 23159640, '38': 30359640, '39': 39559640, '40': 51559640, '41': 66559640,
                      '42': 85559640, '43': 109559640, '44': 139559640, '45': 177559640, '46': 225559640,
                      '47': 285559640, '48': 360559640, '49': 453559640, '50': 569809640
                      }
            try:
                for level in range(1, len(levels) + 1):
                    if exp <= levels[f"{level}"]:
                        return level - 1
                    else:
                        if exp >= levels["50"]:
                            return 50
                        else:
                            pass
            except:
                message = "That person hasn't played dungeons yet!"
                return message

        def class_xp(exp):
            levels = {'1': 50, '2': 75, '3': 110, '4': 160, '5': 230, '6': 330, '7': 470, '8': 670, '9': 950,
                      '10': 1340, '11': 1890, '12': 2665, '13': 3760, '14': 5260, '15': 7380, '16': 10300,
                      '17': 14400, '18': 20000, '19': 27600, '20': 38000, '21': 52500, '22': 71500, '23': 97000,
                      '24': 132000, '25': 180000, '26': 243000, '27': 328000, '28': 445000, '29': 600000,
                      '30': 800000, '31': 1065000, '32': 1410000, '33': 1900000, '34': 2500000, '35': 3300000,
                      '36': 4300000, '37': 5600000, '38': 7200000, '39': 9200000, '40': 12000000, '41': 15000000,
                      '42': 19000000, '43': 24000000, '44': 30000000, '45': 38000000, '46': 48000000,
                      '47': 60000000, '48': 75000000, '49': 93000000, '50': 116250000
                      }
            try:
                for level in range(1, len(levels) + 1):
                    if exp <= levels[f"{level}"]:
                        return level - 1
                    else:
                        if exp >= levels["50"]:
                            return 50
                        else:
                            pass
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s General Skyblock Statistics", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Purse:", value="{:,.1f}".format(sb_data['profiles'][profile_num]['members'][uuid]['coin_purse']), inline=False)
        embed.add_field(name="Fairy Souls:", value="{:,.0f}".format(sb_data['profiles'][profile_num]['members'][uuid]['fairy_souls_collected']), inline=False)
        embed.add_field(name="Catacombs Level:", value=f"{get_cata(cata_exp)}", inline=False)
        embed.add_field(name="Selected Dungeon Class:", value=f"{current_class.capitalize()}", inline=False)
        embed.add_field(name="Class Level:", value=f"{class_xp(class_exp)}", inline=False)
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def essence(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def undead_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_undead']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_undead']
            except:
                return 0

        def diamond_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_diamond']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_diamond']
            except:
                return 0

        def dragon_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_dragon']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_dragon']
            except:
                return 0

        def gold_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_gold']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_gold']
            except:
                return 0

        def ice_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_ice']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_ice']
            except:
                return 0

        def wither_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_wither']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_wither']
            except:
                return 0

        def spider_essence():
            try:
                sb_data['profiles'][profile_num]['members'][uuid]['essence_spider']
                return sb_data['profiles'][profile_num]['members'][uuid]['essence_spider']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Dungeon Essence", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Undead Essence:", value="{:,.0f}".format(undead_essence()))
        embed.add_field(name="Diamond Essence:", value="{:,.0f}".format(diamond_essence()))
        embed.add_field(name="Dragon Essence:", value="{:,.0f}".format(dragon_essence()))
        embed.add_field(name="Gold Essence:", value="{:,.0f}".format(gold_essence()))
        embed.add_field(name="Ice Essence:", value="{:,.0f}".format(ice_essence()))
        embed.add_field(name="Wither Essence:", value="{:,.0f}".format(wither_essence()))
        embed.add_field(name="Spider Essence:", value="{:,.0f}".format(spider_essence()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def weight(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        senither = f"https://hypixel-api.senither.com/v1/profiles/{uuid}?key={KEY}"
        senither_data = getInfo(senither)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(senither_data['data'])):
            if senither_data['data'][z]['id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def weight():
            try:
                senither_data['data'][profile_num]['weight']
                return senither_data['data'][profile_num]['weight']
            except:
                return 0

        def overflow():
            try:
                senither_data['data'][profile_num]['weight_overflow']
                return senither_data['data'][profile_num]['weight_overflow']
            except:
                return 0

        def total_weight():
            return overflow() + weight()

        embed = discord.Embed(title=f"{name}'s Player Weight", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Active Profile", value=profile_name, inline=False)
        embed.add_field(name="Weight:", value="{:,.2f}".format(weight()), inline=False)
        embed.add_field(name="Overflow Weight:", value="{:,.2f}".format(overflow()), inline=False)
        embed.add_field(name="Total Weight:", value="{:,.2f}".format(total_weight()), inline=False)
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def skills(ctx, name):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        uuid = user_name["id"]
        profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
        sb_data = getInfo(profile_link)
        link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
        data = getInfo(link)
        senither = f"https://hypixel-api.senither.com/v1/profiles/{uuid}?key={KEY}"
        senither_data = getInfo(senither)
        save = 9999999999999999999
        for x in range(0, len(sb_data['profiles'])):
            for y in sb_data['profiles'][x]['members']:
                if uuid == y:
                    difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                    if difference < save:
                        save = sb_data['profiles'][x]['members'][y]['last_save']
                        profile_id = sb_data['profiles'][x]['profile_id']

        for z in range(0,len(senither_data['data'])):
            if senither_data['data'][z]['id'] == profile_id:
                profile_num = z

        profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

        def farming():
            try:
                senither_data['data'][profile_num]['skills']['farming']['level']
                return senither_data['data'][profile_num]['skills']['farming']['level']
            except:
                return 0

        def mining():
            try:
                senither_data['data'][profile_num]['skills']['mining']['level']
                return senither_data['data'][profile_num]['skills']['mining']['level']
            except:
                return 0

        def combat():
            try:
                senither_data['data'][profile_num]['skills']['combat']['level']
                return senither_data['data'][profile_num]['skills']['combat']['level']
            except:
                return 0

        def foraging():
            try:
                senither_data['data'][profile_num]['skills']['foraging']['level']
                return senither_data['data'][profile_num]['skills']['foraging']['level']
            except:
                return 0

        def fishing():
            try:
                senither_data['data'][profile_num]['skills']['fishing']['level']
                return senither_data['data'][profile_num]['skills']['fishing']['level']
            except:
                return 0

        def enchanting():
            try:
                senither_data['data'][profile_num]['skills']['enchanting']['level']
                return senither_data['data'][profile_num]['skills']['enchanting']['level']
            except:
                return 0

        def alchemy():
            try:
                senither_data['data'][profile_num]['skills']['alchemy']['level']
                return senither_data['data'][profile_num]['skills']['alchemy']['level']
            except:
                return 0

        def taming():
            try:
                senither_data['data'][profile_num]['skills']['taming']['level']
                return senither_data['data'][profile_num]['skills']['taming']['level']
            except:
                return 0

        def skill_average():
            try:
                senither_data['data'][profile_num]['skills']['average_skills']
                return senither_data['data'][profile_num]['skills']['average_skills']
            except:
                return 0

        embed = discord.Embed(title=f"{name}'s Skills", color=0xC98FFC)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Active Profile", value=profile_name)
        embed.add_field(name="Skill Average:", value="{:,.1f}".format(skill_average()), inline=False)
        embed.add_field(name="Farming:", value="{:,.0f}".format(farming()))
        embed.add_field(name="Mining:", value="{:,.0f}".format(mining()))
        embed.add_field(name="Combat:", value="{:,.0f}".format(combat()))
        embed.add_field(name="Foraging:", value="{:,.0f}".format(foraging()))
        embed.add_field(name="Fishing:", value="{:,.0f}".format(fishing()))
        embed.add_field(name="Enchanting:", value="{:,.0f}".format(enchanting()))
        embed.add_field(name="Alchemy:", value="{:,.0f}".format(alchemy()))
        embed.add_field(name="Taming:", value="{:,.0f}".format(taming()))
    except:
        embed = discord.Embed(title="Error", description="Invalid IGN")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def skin(ctx, name):
  try:
    user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
    embed = discord.Embed(title=f"{name}'s Current Skin", color=0xC98FFC)
    uuid = user_name['id']
    search = f"https://crafatar.com/renders/body/{uuid}"
    embed.set_image(url=search)
  except:
    embed = discord.Embed(title="Error", description="Invalid IGN")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def ign(ctx, uuid):
  try:
    data = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
    user_name = data[len(data)-1]['name']
    embed = discord.Embed(title = f"{uuid} = {user_name}", color=0xC98FFC)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  except:
    embed = discord.Embed(title="Error", description="Invalid UUID")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def skycrypt(ctx, name):
  try:
    user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
    uuid = user_name["id"]
    profile_link = f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}"
    sb_data = getInfo(profile_link)
    link = f"https://api.hypixel.net/player?key={KEY}&uuid={uuid}"
    data = getInfo(link)
    save = 9999999999999999999
    for x in range(0, len(sb_data['profiles'])):
        for y in sb_data['profiles'][x]['members']:
            if uuid == y:
                difference = time.time() - sb_data['profiles'][x]['members'][y]['last_save']
                if difference < save:
                    save = sb_data['profiles'][x]['members'][y]['last_save']
                    profile_id = sb_data['profiles'][x]['profile_id']
    profile_name = data['player']['stats']['SkyBlock']['profiles'][profile_id]["cute_name"]

    skycrypt = f"https://sky.shiiyu.moe/stats/{name}/{profile_name}#"

    embed = discord.Embed(title=f"{name}'s Statistics on {profile_name}", url=skycrypt, color=0xC98FFC)
    embed.set_image(url=f"https://crafatar.com/renders/body/{uuid}")
  except:
    embed = discord.Embed(title="Error", description="Invalid IGN")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
        
@client.command()
async def number(ctx, number):
  try:
    generated = random.randint(0,int(number))
    await ctx.send(f"{ctx.author.mention} your number is {generated}")
  except:
    await ctx.send(f"{ctx.author.mention} '{number}' is not a valid integer")

@client.command()
async def embed(ctx, *, message):
  try:
    sendme = discord.Embed(title=message)
    await ctx.send(embed=sendme)
  except:
    await ctx.send(f"{ctx.author.mention} that hurt my brain. Try something more simple")

@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number=1):
  try:
    number+=1
    await ctx.channel.purge(limit=number)
  except:
    await ctx.send("Invalid Number or Message Outdated")

@client.command()
async def curl(ctx, webhook):
  try:
    webby_info = requests.get(webhook).json()
    if "id" in webby_info:
      embed = discord.Embed(title=webhook, inline=False)
      embed.add_field(name="Webhook Name:", value=f"{webby_info['name']}", inline=False)
      embed.add_field(name="Webhook ID:", value=f"{webby_info['id']}", inline=False)
      embed.add_field(name="Avatar URL:", value=f"{webby_info['avatar']}", inline=False)
      embed.add_field(name="Webhook Token:", value=f"{webby_info['token']}", inline=False)
      embed.add_field(name="Guild ID:", value=f"{webby_info['guild_id']}", inline=False)
      embed.add_field(name="Channel ID:", value=f"{webby_info['channel_id']}", inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send("The webhook no longer exists")
  except:
    await ctx.send("Invalid Webhook")

@client.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, webhook):
  try:
    webby_info = requests.get(webhook).json()
    name = webby_info['name']
    if "id" in webby_info:
      os.system(f"curl -X DELETE {webhook}")
      await ctx.send(f"{name} has been nuked")
    else:
      await ctx.send("The webhook no longer exists")
  except:
    await ctx.send("Invalid Webhook")

@client.command()
async def penis(ctx, name):
  length = ""
  try:
    number = random.randint(1,12)
    for x in range(0,number):
      length += "="
    embed = discord.Embed(title=f"{name}'s Penis", description=f"8{length}D", color=0xC98FFC)
    await ctx.send(embed = embed)
  except:
    await ctx.send(f"{name}'s penis is too tiny'")

@client.command()
@commands.has_permissions(administrator=True)
async def troll(ctx, webhook, *, message):
  try:
    webby = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())
    url = requests.get(webhook).json()
    embed = discord.Embed(title=message, color=0xC98FFC)
    webby.send(username="Totally Not Lyoni", avatar_url="https://cdn.discordapp.com/attachments/675540348822618117/934311231400079450/Screenshot_20220103-060329_Gallery.png", embed=embed)
    await ctx.send(f"Message has been sent to {url['name']} in {url['guild_id']}")
  except:
    await ctx.send("Webhook or Message Invalid")

@client.command()
async def dox(ctx, name):
  digit1 = random.randint(1,255)
  digit2 = random.randint(1,255)
  digit3 = random.randint(1,99)
  digit4 = random.randint(1,255)
  IP = str(digit1) + "." + str(digit2) + "." + str(digit3) + "." + str(digit4)
  url = requests.get(f"http://www.geoplugin.net/json.gp?ip={IP}").json()
  embed = discord.Embed(title=f"{name}'s Dox Information", description="Gathered by BingBot", color=0xC98FFC)
  embed.add_field(name="IP Address", value=f"{IP}", inline=False)
  embed.add_field(name="Continent", value=url['geoplugin_continentName'], inline=False)
  embed.add_field(name="Country", value=url['geoplugin_countryName'], inline=False)
  embed.add_field(name="Timezone", value=url['geoplugin_timezone'], inline=False)
  embed.add_field(name="Region/State", value=url['geoplugin_regionName'], inline=True)
  embed.add_field(name="City", value=url['geoplugin_city'], inline=True)
  embed.set_footer(text="IP Randomly Generated")
  await ctx.send(embed=embed)

@client.command()
async def plancke(ctx, name="hypixel"):
  try:
    user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
    uuid = user_name["id"]
    url = f"https://plancke.io/hypixel/player/stats/{name}"
    embed = discord.Embed(title=f"{name}'s Planke Statistics", url=url, color=0xC98FFC)
    embed.set_image(url=f"https://crafatar.com/renders/body/{uuid}")
  except:
    embed = discord.Embed(title="Error", description="Invalid IGN")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def bin(ctx, *, item):
  try:
    auction_data = requests.get("http://maro.skyblockextras.com/api/auctions/all").json()
    for i in range(0,len(auction_data['data'])):
      if auction_data['data'][i]['name'] == item or item.lower() == auction_data['data'][i]['name'].lower():
        number = i

    item_id = auction_data['data'][number]['id']
    item_data = requests.get(f"http://maro.skyblockextras.com/api/auctions/quickStats/{item_id}").json()
    embed = discord.Embed(title=auction_data['data'][number]['name'], description=item_id, color=0xC98FFC)
    embed.add_field(name="Lowest BIN", value="{:,.0f} coins".format(auction_data['data'][number]['value']))
    embed.add_field(name="Average Price", value="{:,.2f} coins".format(item_data['data']['average']))
    embed.add_field(name="Highest Price", value="{:,.2f} coins".format(item_data['data']['max']))
  except:
    embed = discord.Embed(title="Error", description="Invalid Item")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
  try:
    await user.add_roles(role)
    await ctx.send(f"{user.name} has been given {role.name}")
    await user.send(f"You were given **{role.name}** in *{user.guild.name}*")
  except:
    embed = discord.Embed(title="Error", description="Invalid Role or ID")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command()
async def geolocate(ctx, IP):
  try:
    url = requests.get(f"http://www.geoplugin.net/json.gp?ip={IP}").json()
    embed = discord.Embed(title=f"{IP} Geolocation Information", description="Geolocation API", color=0xC98FFC)
    embed.add_field(name="Continent", value=f"{url['geoplugin_continentName']}", inline=False)
    embed.add_field(name="Country", value=f"{url['geoplugin_countryName']}", inline=False)
    embed.add_field(name="Timezone", value=f"{url['geoplugin_timezone']}", inline=False)
    embed.add_field(name="Region/State", value=f"{url['geoplugin_regionName']}", inline=True)
    embed.add_field(name="City", value=f"{url['geoplugin_city']}", inline=True)
    embed.set_footer(text=f"https://thatsthem.com/ip/{IP}")
  except:
    embed = discord.Embed(title="Error", description="Invalid IP")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@slash.slash(
  description="View a user's profile information",
  guild_ids=[945030771410878495, 931682862581841940, 925930297789415554, 934362614572650517, 963211165763252354],
  options = [
    create_option(
      name="id",
      description="User ID",
      required=False,
      option_type=3
    ),
    create_option(
      name="mention",
      description="Mention User",
      required=False,
      option_type=6
    )
  ]
)
async def userinfo(ctx, id=None, mention=None):
  try:
    if id is None:
      id = str(mention.id)
    output = subprocess.check_output(f"curl --silent --header 'Authorization: Bot {token}' https://discord.com/api/v9/users/{id}", shell=True).decode("utf-8")
    res = json.loads(str(output))
    embed = discord.Embed(title=res['username'], color=0xC98FFC)
    user = await client.fetch_user(int(id))
    x = str(user.created_at).split("-")
    compl = x[2].split(" ")
    months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
    embed.add_field(name="User Information:", 
                    value=f"User: {res['username']}#{res['discriminator']}\nID: {id}\nAccount Created: {months[x[1]]} {compl[0]}, {x[0]}\nAccent Color: {res['accent_color']}\nBanner Color: {res['banner_color']}\nBanner: https://cdn.discordapp.com/banners/{id}/${res['banner']}?size=256")
    if mention != None:
      revroles = " ".join([role.mention for role in mention.roles if role.name != "@everyone"])
      splitted = revroles.split(" ")
      splitted.reverse()
      roles = " ".join(item for item in splitted)
      embed.add_field(name="Server Roles:", value=f"{roles}", inline=False)
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{id}/{res['avatar']}.webp?size=1024")
    await ctx.send(embed=embed)
  except:
    await ctx.send("An error has occured")

@client.command()
async def servers(ctx):
  try:
    for guild_ in client.guilds:
      await ctx.send(f"{guild_}: {guild_.id}")
  except:
    await ctx.send("Did not work properly")

@client.command()
async def startmining(ctx):
  with open("economy.json", "r") as f:
    data = json.load(f)
    
  user_num = -1
  for x in range(len(data)):
    if data[x]["id"] == ctx.author.id:
      user_num = x
  if user_num == -1:
    with open("economy.json", "r") as f:
      data = json.load(f)
    user_info = {"id": ctx.author.id, "name": str(ctx.author), "coin": 0, "bank": [0, "Default Bank"], "spent": 0, "current_pick": "BingCoin Pickaxe"}
    data.append(user_info)
    with open('economy.json', 'w') as outfile:
      outfile.write(json.dumps(data))
    await ctx.send(f"You are now ready to mine {ctx.author}")
  else:
    await ctx.send(f"{ctx.author} you already have an account!")

@client.command()
async def members(ctx):
  await ctx.send(f"{ctx.guild} has {ctx.guild.member_count} members")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def mine(ctx):
  with open("economy.json", "r") as f:
    data = json.load(f)
  account = False

  user_num = -1
  rank_ = "Default"
  for x in range(len(data)):
    if data[x]["id"] == ctx.author.id:
      user_num = x
      account = True 
  
  if account is True:
    with open("premium.json", "r") as premfile:
        premium = json.load(premfile)
    def return_key(val):
      key_list=list(premium[0].keys())
      val_list=list(premium[0].values())
      for i in range(len(premium[0])):
        if val_list[i]==val:
          return key_list[i]
          
    for p in premium[0]:
      for i in range(len(premium[0][p])):
        if ctx.author.id == premium[0][p][i]:
          rank_ = return_key(premium[0][p])
    if data[user_num]['current_pick'] == "BingCoin Pickaxe":
      min = 1
      coin_num = 1
    elif data[user_num]['current_pick'] == "BingCoin Drill": 
      min = 1
      coin_num = 2
    elif data[user_num]['current_pick'] == "Miner x1000": 
      min = 2
      coin_num = 5
    elif data[user_num]['current_pick'] == "Miner x1050": 
      min = 4
      coin_num = 7
    elif data[user_num]['current_pick'] == "Miner x1060": 
      min = 6
      coin_num = 9
    elif data[user_num]['current_pick'] == "Miner x1070": 
      min = 8
      coin_num = 11
    elif data[user_num]['current_pick'] == "Miner x1080": 
      min = 10
      coin_num = 13
    elif data[user_num]['current_pick'] == "NFT x2000": 
      min = 17
      coin_num = 20
    elif data[user_num]['current_pick'] == "NFT x2050": 
      min = 20
      coin_num = 23
    elif data[user_num]['current_pick'] == "NFT x2060": 
      min = 26
      coin_num = 32
    elif data[user_num]['current_pick'] == "NFT x2070": 
      min = 36
      coin_num = 43
    elif data[user_num]['current_pick'] == "NFT x2080": 
      min = 50
      coin_num = 66
    elif data[user_num]['current_pick'] == "BTH x3000": 
      min = 150
      coin_num = 165
    elif data[user_num]['current_pick'] == "BTH x3050": 
      min = 170
      coin_num = 185
    elif data[user_num]['current_pick'] == "BTH x3060": 
      min = 185
      coin_num = 200
    elif data[user_num]['current_pick'] == "BTH x3070": 
      min = 210
      coin_num = 230
    elif data[user_num]['current_pick'] == "BTH x3080": 
      min = 240
      coin_num = 270
    elif data[user_num]['current_pick'] == "BTH x3090": 
      min = 280
      coin_num = 310
    

    if rank_ == "Default":
      chance = random.randint(0, 50)
    elif rank_ == "Script Kitty":
      chance = random.randint(40,80)
    elif rank_ == "Bitcoin Screenshotter":
      chance = random.randint(40,70)
    elif rank_ == "NFT Miner":
      chance = random.randint(60,80)
    NFT = False
    mined = random.randint(min,coin_num)
    if chance == 69:
      mined = mined * 5
      NFT = True
    new_coins = mined + data[user_num]["coin"]
    same_info = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]['current_pick']}
    data.pop(user_num)
    data.append(same_info)
    with open('economy.json', 'w') as outfile:
      outfile.write(json.dumps(data))
    if NFT is True:
      await ctx.reply(f"{ctx.author} has mined an NFT and received 〶{mined:,} BingCoin")
    else:
      await ctx.reply(f"{ctx.author} has mined 〶{mined:,} BingCoin")
  else:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command(aliases=["bal"])
async def balance(ctx, user:discord.Member=None):
  try:
    with open("economy.json", "r") as f:
       data = json.load(f)
    if user == None:
      for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
      user_balance = ctx.author
    else:
      for x in range(len(data)):
        if data[x]["id"] == user.id:
          user_num = x
      user_balance = user
  
    await ctx.send(f"{user_balance}'s Account:\n\n 💰 Bank: **〶{data[user_num]['bank'][0]:,} BingCoin**\n💵 Wallet: **〶{data[user_num]['coin']:,} BingCoin**")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command(aliases=["nw", "worth", "nworth"])
async def networth(ctx, user:discord.Member=None):
  try:
    with open("economy.json", "r") as f:
       data = json.load(f)
    if user == None:
      for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
      user_balance = ctx.author
    else:
      for x in range(len(data)):
        if data[x]["id"] == user.id:
          user_num = x
      user_balance = user
  
    await ctx.send(f"{user_balance}'s current networth is **〶{(data[user_num]['coin'] + data[user_num]['spent'] + data[user_num]['bank'][0]):,} BingCoin**")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command(aliases=['pick'])
async def pickaxe(ctx, user:discord.Member=None):
  try:
    with open("economy.json", "r") as f:
       data = json.load(f)
    if user == None:
      for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
      user_pick = ctx.author
    else:
      for x in range(len(data)):
        if data[x]["id"] == user.id:
          user_num = x
      user_pick = user
  
    await ctx.send(f"{user_pick}'s current pickaxe is **{data[user_num]['current_pick']}**")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command()
async def shop(ctx):
  embed = discord.Embed(title="BingCoin Shop", description="Coins must be in wallet to make purchases", color=0xC98FFC)
  embed.add_field(name="Pickaxes:", value=f"{pickaxes[0]}: Free\n{pickaxes[1]}: 〶20\n\n{pickaxes[2]}: 〶75\n{pickaxes[3]}: 〶150\n{pickaxes[4]}: 〶300\n{pickaxes[5]}: 〶500\n{pickaxes[6]}: 〶750\n\n{pickaxes[7]}: 〶1,250\n{pickaxes[8]}: 〶1,900\n{pickaxes[9]}: 〶2,900\n{pickaxes[10]}: 〶4,000\n{pickaxes[11]}: 〶7,500\n\n{pickaxes[12]}: 〶20,000\n{pickaxes[13]}: 〶30,000\n{pickaxes[14]}: 〶43,000\n{pickaxes[15]}: 〶57,000\n{pickaxes[16]}: 〶74,000\n{pickaxes[17]}: 〶94,000", inline=True)
  embed.add_field(name="Banks:", value=f"{bank_list[0]}: Free\n{bank_list[1]}: 〶450\n{bank_list[2]}: 〶1,200\n{bank_list[3]}: 〶3,000\n{bank_list[4]}: 〶7,500\n{bank_list[5]}: 〶18,000\n{bank_list[6]}: 〶37,000\n{bank_list[7]}: 〶57,000", inline=True)
  embed.add_field(name="Donations:", value="Paypal: itsb1ng611@gmail.com", inline=False)
  embed.set_footer(text="Developed by bing#0001", icon_url="https://i.imgur.com/9ZTBdOK.png")
  await ctx.send(embed=embed)

@client.command()
async def buy(ctx, *, pick_name):
  with open("economy.json", "r") as f:
    data = json.load(f)

  for x in range(len(data)):
    if data[x]["id"] == ctx.author.id:
      user_num = x
  if pick_name in pickaxes:
    for x in range(len(pickaxes)):
      if pickaxes[x] == pick_name:
        pick_num = x
    for z in range(len(pickaxes)):
      if pickaxes[z] == data[user_num]["current_pick"]:
        current_pick_num = z
        
    if (pick_num == 1) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 20):
      new_coins = data[user_num]['coin'] - 20
      spend = data[user_num]['spent'] + 20
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶20")
    elif (pick_num == 2) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 75):
      new_coins = data[user_num]['coin'] - 75
      spend = data[user_num]['spent'] + 75
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶75")
    elif (pick_num == 3) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 150):
      new_coins = data[user_num]['coin'] - 150
      spend = data[user_num]['spent'] + 150
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶150")
    elif (pick_num == 4) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 300):
      new_coins = data[user_num]['coin'] - 300
      spend = data[user_num]['spent'] + 300
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶300")
    elif (pick_num == 5) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 500):
      new_coins = data[user_num]['coin'] - 500
      spend = data[user_num]['spent'] + 500
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶500")
    elif (pick_num == 6) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 750):
      new_coins = data[user_num]['coin'] - 750
      spend = data[user_num]['spent'] + 750
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶750")
    elif (pick_num == 7) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 1250):
      new_coins = data[user_num]['coin'] - 1250
      spend = data[user_num]['spent'] + 1250
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶1,250")
    elif (pick_num == 8) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 1900):
      new_coins = data[user_num]['coin'] - 1900
      spend = data[user_num]['spent'] + 1900
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶1,900")
    elif (pick_num == 9) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 2900):
      new_coins = data[user_num]['coin'] - 2900
      spend = data[user_num]['spent'] + 2900
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶2,900")
    elif (pick_num == 10) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 4000):
      new_coins = data[user_num]['coin'] - 4000
      spend = data[user_num]['spent'] + 4000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶4,000")
    elif (pick_num == 11) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 7500):
      new_coins = data[user_num]['coin'] - 7500
      spend = data[user_num]['spent'] + 7500
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶7,500")
    elif (pick_num == 12) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 20000):
      new_coins = data[user_num]['coin'] - 20000
      spend = data[user_num]['spent'] + 20000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶20,000")
    elif (pick_num == 13) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 30000):
      new_coins = data[user_num]['coin'] - 30000
      spend = data[user_num]['spent'] + 30000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶30,000")
    elif (pick_num == 14) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 43000):
      new_coins = data[user_num]['coin'] - 43000
      spend = data[user_num]['spent'] + 43000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶43,000")
    elif (pick_num == 15) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 57000):
      new_coins = data[user_num]['coin'] - 57000
      spend = data[user_num]['spent'] + 57000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶57,000")
    elif (pick_num == 16) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 74000):
      new_coins = data[user_num]['coin'] - 74000
      spend = data[user_num]['spent'] + 74000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶74,000")
    elif (pick_num == 17) and (current_pick_num < pick_num) and (data[user_num]['coin'] >= 94000):
      new_coins = data[user_num]['coin'] - 94000
      spend = data[user_num]['spent'] + 94000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": spend, "current_pick": pick_name}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {pick_name} for 〶94,000")
    else:
      await ctx.send(f"Could not purchase {pick_name}")
  else:
    await ctx.send(f"{pick_name} is not a valid pickaxe")

@client.command()
async def leaderboard(ctx):
  with open("economy.json", "r") as f:
    data = json.load(f)
  first = ("",0)
  second = ("",0)
  third = ("",0)
  
  for x in range(len(data)):
    value1 = int(data[x]['coin']) + int(data[x]['spent']) + int(data[x]['bank'][0])
    if int(value1) > first[1]:
      first = (data[x]["name"], int(value1))

  for x in range(len(data)):
    value2 = int(data[x]['coin']) + int(data[x]['spent']) + int(data[x]['bank'][0])
    if (int(value2) > second[1]) and (int(value2) < first[1]):
      second = (data[x]['name'], int(value2))

  for x in range(len(data)):
    value3 = int(data[x]['coin']) + int(data[x]['spent']) + int(data[x]['bank'][0])
    if (int(value3) > third[1]) and (int(value3) < second[1]):
      third = (data[x]['name'], int(value3))

  await ctx.send(f"〶      BingCoin Leaderboard:      〶\n\n1. {first[0]}: 〶{first[1]:,}\n2. {second[0]}: 〶{second[1]:,}\n3. {third[0]}: 〶{third[1]:,}")

@client.command(aliases=["depo"])
@commands.cooldown(1, 60, commands.BucketType.user)
async def deposit(ctx, amount="all"):
  try:
    max = 0
    with open("economy.json", "r") as f:
      data = json.load(f)

    for x in range(len(data)):
      if data[x]["id"] == ctx.author.id:
        user_num = x
    if amount == "all":
      if data[user_num]['bank'][1] == bank_list[0]:
        max = 100
      elif data[user_num]['bank'][1] == bank_list[1]:
        max = 600
      elif data[user_num]['bank'][1] == bank_list[2]:
        max = 1500
      elif data[user_num]['bank'][1] == bank_list[3]:
        max = 3500
      elif data[user_num]['bank'][1] == bank_list[4]:
        max = 10000
      elif data[user_num]['bank'][1] == bank_list[5]:
        max = 27500
      elif data[user_num]['bank'][1] == bank_list[6]:
        max = 50000
      elif data[user_num]['bank'][1] == bank_list[7]:
        max = 80000

      attempt_depo = data[user_num]['bank'][0] + data[user_num]['coin']
      coin_ = data[user_num]['coin']
      if max == data[user_num]['bank'][0]:
        await ctx.reply(f"Your bank *{data[user_num]['bank'][1]}* is currently full")
      elif attempt_depo <= max:
        new_wallet = 0
        new_bank_balance = data[user_num]['bank'][0] + data[user_num]['coin']
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_wallet, "bank": [new_bank_balance, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as outfile:
          outfile.write(json.dumps(data))
        await ctx.reply(f"You have deposited 〶{coin_:,} BingCoin")
      elif attempt_depo > max:
        over_max = attempt_depo - max
        deposited = coin_ - over_max
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": over_max, "bank": [max, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as outfile:
          outfile.write(json.dumps(data))
        await ctx.reply(f"You have deposited 〶{deposited:,} BingCoin and *{data[user_num]['bank'][1]}* is full")
    elif int(amount) <= data[user_num]['coin']:
      if data[user_num]['bank'][1] == bank_list[0]:
        max = 100
      elif data[user_num]['bank'][1] == bank_list[1]:
        max = 600
      elif data[user_num]['bank'][1] == bank_list[2]:
        max = 1500
      elif data[user_num]['bank'][1] == bank_list[3]:
        max = 3500
      elif data[user_num]['bank'][1] == bank_list[4]:
        max = 10000
      elif data[user_num]['bank'][1] == bank_list[5]:
        max = 27500
      elif data[user_num]['bank'][1] == bank_list[6]:
        max = 50000
      elif data[user_num]['bank'][1] == bank_list[7]:
        max = 80000
        
      attempt_depo = data[user_num]['bank'][0] + int(amount)
      if max == data[user_num]['bank'][0]:
        await ctx.reply(f"Your bank *{data[user_num]['bank'][1]}* is currently full")
      elif attempt_depo <= max:
        new_wallet = data[user_num]['coin'] - int(amount)
        new_bank_balance = data[user_num]['bank'][0] + int(amount)
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_wallet, "bank": [new_bank_balance, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as outfile:
          outfile.write(json.dumps(data))
        await ctx.reply(f"You have deposited 〶{int(amount)} BingCoin")
      elif attempt_depo > max:
        over_max = attempt_depo - max
        deposited = int(amount) - over_max
        new_coins = (data[user_num]['coin'] - int(amount)) + over_max
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [max, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as outfile:
          outfile.write(json.dumps(data))
        await ctx.reply(f"You have deposited 〶{deposited} BingCoin and *{data[user_num]['bank'][1]}* is full")
    else:
      if int(amount) > 0:
        await ctx.reply(f"You do not have **〶{amount} BingCoin** in your wallet")
      else:
        await ctx.reply(f"**{amount}** is not a valid integer")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command(aliases=["with"])
async def withdraw(ctx, amount="all"):
  try:
    with open("economy.json", "r") as f:
      data = json.load(f)

    for x in range(len(data)):
      if data[x]["id"] == ctx.author.id:
        user_num = x
    bankee = data[user_num]['bank'][0]
    if amount == "all":
      new_wallet = data[user_num]['coin'] + data[user_num]['bank'][0]
      new_bank_balance = 0
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_wallet, "bank": [new_bank_balance, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.reply(f"You have withdrawn 〶{bankee:,} BingCoin")
    elif int(amount) <= data[user_num]['bank'][0]:
      new_wallet = data[user_num]['coin'] + int(amount)
      new_bank_balance = data[user_num]['bank'][0] - int(amount)
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_wallet, "bank": [new_bank_balance, data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]["current_pick"]}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.reply(f"You have withdrawn 〶{int(amount):,} BingCoin")
    else:
      if int(amount) > 0:
        await ctx.reply(f"You do not have **〶{int(amount):,} BingCoin** in your bank")
      else:
        await ctx.reply(f"**{amount}** is not a valid integer")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command()
async def bank(ctx, user:discord.Member=None):
  try:
    with open("economy.json", "r") as f:
       data = json.load(f)
    if user == None:
      for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
    else:
      for x in range(len(data)):
        if data[x]["id"] == user.id:
          user_num = x
  
    await ctx.send(f"{data[user_num]['name']}'s current bank is **{data[user_num]['bank'][1]}**")
  except:
    await ctx.send("You do not have a mining setup yet please try 'bb!startmining'")

@client.command()
async def apply(ctx, *, bank_application):
  with open("economy.json", "r") as f:
    data = json.load(f)

  for x in range(len(data)):
    if data[x]["id"] == ctx.author.id:
      user_num = x
  if bank_application in bank_list:
    for x in range(len(bank_list)):
      if bank_list[x] == bank_application:
        bank_num = x
    for z in range(len(bank_list)):
      if bank_list[z] == data[user_num]["bank"][1]:
        current_bank_num = z
        
    if (bank_num == 1) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 450):
      new_coins = data[user_num]['coin'] - 450
      spend = data[user_num]['spent'] + 450
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶450")
    elif (bank_num == 2) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 1200):
      new_coins = data[user_num]['coin'] - 1200
      spend = data[user_num]['spent'] + 1200
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶1,200")
    elif (bank_num == 3) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 3000):
      new_coins = data[user_num]['coin'] - 3000
      spend = data[user_num]['spent'] + 3000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶3,000")
    elif (bank_num == 4) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 7500):
      new_coins = data[user_num]['coin'] - 7500
      spend = data[user_num]['spent'] + 7500
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶7,500")
    elif (bank_num == 5) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 18000):
      new_coins = data[user_num]['coin'] - 18000
      spend = data[user_num]['spent'] + 18000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶18,000")
    elif (bank_num == 6) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 37000):
      new_coins = data[user_num]['coin'] - 37000
      spend = data[user_num]['spent'] + 37000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶37,000")
    elif (bank_num == 7) and (current_bank_num < bank_num) and (data[user_num]['coin'] >= 57000):
      new_coins = data[user_num]['coin'] - 57000
      spend = data[user_num]['spent'] + 57000
      outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], bank_application], "spent": spend, "current_pick": data[user_num]['current_pick']}
      data.pop(user_num)
      data.append(outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      await ctx.send(f"You have purchased {bank_application} for 〶57,000")
    else:
      await ctx.send(f"Could not purchase {bank_application}")
    
  else:
    await ctx.send(f"{bank_application} is not a valid bank")

@client.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def rob(ctx, user:discord.Member):
  try:
    rank_ = "Default"
    with open("economy.json", "r") as f:
      data = json.load(f)

    for v in range(len(data)):
      if data[v]["id"] == user.id:
        victim_num = v

    if data[victim_num]['coin'] >= 10:
      with open("premium.json", "r") as premfile:
        premium = json.load(premfile)
      def return_key(val):
        key_list=list(premium[0].keys())
        val_list=list(premium[0].values())
        for i in range(len(premium[0])):
            if val_list[i]==val:
                return key_list[i]
        return("Key Not Found")
      for p in premium[0]:
        for i in range(len(premium[0][p])):
          if ctx.author.id == premium[0][p][i]:
            rank_ = return_key(premium[0][p])
      if rank_ == "Default":
        robbed = data[victim_num]['coin'] * 0.20
      elif rank_ == "Script Kitty":
        robbed = data[victim_num]['coin'] * 0.30
      elif rank_ == "Bitcoin Screenshotter":
        robbed = data[victim_num]['coin'] * 0.40
      elif rank_ == "NFT Miner":
        robbed = data[victim_num]['coin'] * 0.50
        
      victim_coins = data[victim_num]['coin'] - int(robbed)
      victim_outdata = {"id": data[victim_num]['id'], "name": data[victim_num]['name'], "coin": victim_coins, "bank": [data[victim_num]['bank'][0], data[victim_num]['bank'][1]], "spent": data[victim_num]['spent'], "current_pick": data[victim_num]['current_pick']}
      data.pop(victim_num)
      data.append(victim_outdata)
      with open('economy.json', 'w') as outfile:
        outfile.write(json.dumps(data))
      outfile.close()

      for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          robber_num = x
        
      robber_coins = data[robber_num]['coin'] + int(robbed)
      robber_outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": robber_coins, "bank": [data[robber_num]['bank'][0], data[robber_num]['bank'][1]], "spent": data[robber_num]['spent'], "current_pick": data[robber_num]['current_pick']}
      data.pop(robber_num)
      data.append(robber_outdata)
      with open('economy.json', 'w') as robberout:
        robberout.write(json.dumps(data))
      robberout.close()

      await ctx.reply(f"You have robbed {user} for 〶{int(robbed)} BingCoin")
    else:  
      await ctx.reply(f"You could not rob {user}")
  except:
    await ctx.send("You cannot rob try 'bb!startmining'")

@client.command()
async def banks(ctx):
  embed=discord.Embed(title="Available Banks", color=0xC98FFC)
  embed.add_field(name="DGE Premium", value="Cost: 〶57,000\nCapacity: 〶80,000", inline=False)
  embed.add_field(name="DGE Bank", value="Cost: 〶37,000\nCapacity: 〶50,000", inline=False)
  embed.add_field(name="BTH Bank", value="Cost: 〶18,000\nCapacity: 〶27,500", inline=False)
  embed.add_field(name="NFT Bank", value="Cost: 〶7,500\nCapacity: 〶10,000", inline=False)
  embed.add_field(name="Elite Bank", value="Cost: 〶3,000\nCapacity: 〶3,500", inline=False)
  embed.add_field(name="Professional Bank", value="Cost: 〶1,200\nCapacity: 〶1,500", inline=False)
  embed.add_field(name="Amateur Bank", value="Cost: 〶450\nCapacity: 〶600", inline=False)
  embed.add_field(name="Default Bank", value="Cost: 〶Free\nCapacity: 〶100", inline=False)
  embed.set_footer(text="Developed by bing#0001", icon_url="https://i.imgur.com/9ZTBdOK.png")
  await ctx.send(embed=embed)

@client.command()
async def ranks(ctx):
  embed = discord.Embed(title="BingCoin Ranks", color=0xC98FFC)
  embed.add_field(name="NFT Miner: Donation Exclusive", value="- Rob 50% of victim wallet\n- 5% chance of mining an NFT\n- 60% Bank Interest", inline=False)
  embed.add_field(name="Bitcoin Screenshotter: Donation Exclusive", value="- Rob 40% of victim wallet\n- 3.34% chance of mining an NFT\n- 50% Bank Interest", inline=False)
  embed.add_field(name="Script Kitty: 〶5,000", value="- Rob 30% of victim wallet\n- 2.5% chance of mining an NFT\n- 35% Bank Interest", inline=False)
  embed.add_field(name="Default", value="- Rob 20% of victim wallet\n- 2% chance of mining an NFT\n- 20% Bank Interest", inline=False)
  await ctx.send(embed=embed)

@client.command()
async def rank(ctx, user:discord.Member=None):
  try:
    rank_ = "Default"
    with open("premium.json", "r") as premfile:
      premium = json.load(premfile)
    def return_key(val):
      key_list=list(premium[0].keys())
      val_list=list(premium[0].values())
      for i in range(len(premium[0])):
        if val_list[i]==val:
          return key_list[i]
      return("Key Not Found")
    if user is None:
      for p in premium[0]:
        for i in range(len(premium[0][p])):
          if ctx.author.id == premium[0][p][i]:
            rank_ = return_key(premium[0][p])
      await ctx.send(f"{ctx.author}'s rank is: **{rank_}**")
    else:
      for p in premium[0]:
        for i in range(len(premium[0][p])):
          if user.id == premium[0][p][i]:
            rank_ = return_key(premium[0][p])
      await ctx.send(f"{user}'s rank is: **{rank_}**")
  except:
    await ctx.reply("`Invalid user!`")

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def interest(ctx):
  try:
    with open("economy.json", "r") as f:
      data = json.load(f)
    for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
    rank_ = "Default"
    with open("premium.json", "r") as premfile:
      premium = json.load(premfile)
    def return_key(val):
      key_list=list(premium[0].keys())
      val_list=list(premium[0].values())
      for i in range(len(premium[0])):
        if val_list[i]==val:
          return key_list[i]
      return("Key Not Found")
    for p in premium[0]:
      for i in range(len(premium[0][p])):
        if ctx.author.id == premium[0][p][i]:
          rank_ = return_key(premium[0][p])

    if rank_ == "Default":
      percent = .20
    elif rank_ == "Script Kitty":
      percent = .35
    elif rank_ == "Bitcoin Screenshotter":
      percent = .50
    elif rank_ == "NFT Miner":
      percent = .60

    income = data[user_num]['bank'][0] * percent
    new_balance = income + data[user_num]['coin']

    outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": int(new_balance), "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]['current_pick']}
    data.pop(user_num)
    data.append(outdata)
    with open('economy.json', 'w') as outfile:
      outfile.write(json.dumps(data))
    await ctx.send(f"{ctx.author} has received **〶{int(income):,} BingCoin** as interest")
  except:
    await ctx.send("You cannot collect interest yet please try 'bb!startmining'")

@slash.slash(
  description="Coinflip the AI",
  guild_ids=[945030771410878495, 931682862581841940, 925930297789415554, 934362614572650517, 963211165763252354],
  options = [
    create_option(
      name="amount",
      description="BingCoin to coinflip",
      required=True,
      option_type=4
    ),
    create_option(
      name="choice",
      description="heads or tails",
      required=True,
      option_type=3
    )
  ]
)
async def coinflip(ctx, amount, choice):
  try:
    with open("economy.json", "r") as f:
      data = json.load(f)
    for x in range(len(data)):
        if data[x]["id"] == ctx.author.id:
          user_num = x
    if data[user_num]['coin'] >= amount:
      chance = random.randint(1,100)
      if chance >= 50:
        flip = "heads"
      elif chance <= 49:
        flip = "tails"
  
      if flip == "heads" and choice.lower() == "heads":
        new_coins = amount + data[user_num]['coin']
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]['current_pick']}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as out:
          out.write(json.dumps(data))
        await ctx.send(f"It was {flip}! You earned **〶{int(amount):,} BingCoin**")
      elif flip == "tails" and choice.lower() == "tails":
        new_coins = amount + data[user_num]['coin']
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]['current_pick']}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as out:
          out.write(json.dumps(data))
        await ctx.send(f"It was {flip}! You earned **〶{int(amount):,} BingCoin**")
      else:
        new_coins = data[user_num]['coin'] - amount
        outdata = {"id": ctx.author.id, "name": str(ctx.author), "coin": new_coins, "bank": [data[user_num]['bank'][0], data[user_num]['bank'][1]], "spent": data[user_num]['spent'], "current_pick": data[user_num]['current_pick']}
        data.pop(user_num)
        data.append(outdata)
        with open('economy.json', 'w') as out:
          out.write(json.dumps(data))
        await ctx.send(f"It was {flip} :( You lost **〶{int(amount):,} BingCoin**")
    else:  
      await ctx.reply(f"You do not have enough BingCoin to coinflip. Check wallet balance")
  except:
    await ctx.send("You cannot coinflip try 'bb!startmining'")      
    
keep_alive.keep_alive()
client.run(token)