import os
import praw
import random
import discord
from typing import Text
from discord import message
from discord import channel
from discord import member
from discord import guild
from discord.activity import CustomActivity
from discord.enums import ChannelType
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.abc import Messageable

#for reddit memes command
reddit = praw.Reddit(client_id = "icPTZIm7OljvDFAIOfeX2Q",
                     client_secret = "d03JweFqi6FqJ2ekj9pu9IrIZ5ff7A",
                     username = "Xplode_29",
                     password = "CHAcha.29",
                     user_agent = "XplodeBot",
                     check_for_async=False)
                     

bot = Bot(command_prefix="*", description= "bot du serveur de Xplode_29")
member = discord.Member
guild = discord.Guild
textchannel = discord.TextChannel
voicechannel = discord.VoiceChannel
message = discord.Message

#when he's ready
@bot.event
async def on_ready():
    print("XplodeBot is ready")

#help command
@bot.command()
async def helpme(ctx):
    description ="tapez *present pour que je me presente,\n*meme pour avoir un meme aléatoire,\n*salon_prive pour créer un salon prive que seul vous et les bots peuvent y acceder.\nD'autres commandes arriveront encore prochainement, n'hésitez pas à dm le chef supreme pour proposer des commandes à ajouter !"
    embed = discord.Embed(description = description,
    color = 0xFF5733)
    await ctx.send(embed=embed)

@bot.command()
async def present(ctx):
    embed = discord.Embed(description = "Je suis Le bot de ce serveur,\n créé par son chef Xplode_29", color = 0xFF5733)
    await ctx.send(embed = embed)
    
@bot.command(name = 'del')
@commands.has_permissions(manage_messages = True)
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
    for each_message in messages:
        await each_message.delete()


@bot.command(name='ban')
@commands.has_permissions(ban_members = True, kick_members = True)
async def eject_permanently(ctx, arg1):
    await ctx.channel.send("Banned {}".format(arg1))

@bot.command()
async def salon_prive(ctx):
    description = "Le salon sera Vocal ou Textuel ?"
    embed = discord.Embed(title = "Création du channel privé",
    description = description,
    color = 0xFF5733)
    message = await ctx.send(embed = embed)
    await message.add_reaction("🔊")
    await message.add_reaction("⌨️")

    def checkReaction(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "🔊" or str(reaction.emoji) == "⌨️")


    reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkReaction)


    if reaction.emoji == "🔊":
        #pas fini reste à déplacer la personne
        description = str(description) + "\n" + "création du salon vocal en cours..."
        embed = discord.Embed(title = "Création du channel privé",
        description = description,
        color = 0xFF5733)
        await message.edit(embed = embed)
        channelname = 'private_voice_' + str(user)
        role = discord.utils.get(ctx.guild.roles, id=808717762272165928)

        overwrites = {
            role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True)
        }
        guild = ctx.guild
        category = discord.utils.get(ctx.guild.categories, name='private channels')
        await guild.create_voice_channel(name = channelname, overwrites=overwrites, category = category)
        description = str(description) + "\n" + "salon créé dans la section private channels"
        embed = discord.Embed(title = "Création du channel privé",
        description = description,
        color = 0xFF5733)
        await message.edit(embed = embed)
        
    else:
        #fini nickel
        description = str(description) + "\n" + "création du salon textuel en cours..."
        embed = discord.Embed(title = "Création du channel privé",
        description = description,
        color = 0xFF5733)
        await message.edit(embed = embed)
        channelname ='private_text_' + str(user)
        role = discord.utils.get(ctx.guild.roles, id=808717762272165928)

        overwrites = {
            role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True)
        }
        guild = ctx.guild
        category = discord.utils.get(ctx.guild.categories, name='private channels')
        await guild.create_text_channel(name=channelname, overwrites=overwrites, category = category)
        description = str(description) + "\n" + "salon créé dans la section private channels"
        embed = discord.Embed(title = "Création du channel privé",
        description = description,
        color = 0xFF5733)
        await message.edit(embed = embed)
        channel = discord.utils.get(guild.text_channels, name=channelname)
        await channel.send('is it working ?')

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Test Embed",
    description ="Voici un test d'un embed",
    color = 0xFF5733)
    embed.set_author(name=ctx.author.display_name,
    icon_url=ctx.author.avatar_url)

    lien_de_limage = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzs-ec3VCaErGS_i3Fg-ALWrPCapoeAss7ng&usqp=CAU'
    embed.set_thumbnail(url=lien_de_limage)

    embed.add_field(name="Field 1 Title", 
    value="This is the value for field 1. This is NOT an inline field.", 
    inline=False)
    embed.add_field(name="Field 2 Title", 
    value="It is inline with Field 3", inline=True)
    embed.add_field(name="Field 3 Title", 
    value="It is inline with Field 2", inline=True)

    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))

    await ctx.send(embed=embed)

@bot.command()
async def be_member(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, id=864239570756436009)
    await member.add_roles(role)

@bot.command()
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []

    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url =random_sub.url

    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(808717975167303751)
    await channel.send("Yo {member.mention}, Bienvenue dans La Communauté Explosive!")

bot.run("ODYzNjkxNTQ1MzM2NjEwODM2.YOqlbw.EUFVePBTr3zQMlrRmEccLAh1TO8")