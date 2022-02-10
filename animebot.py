import discord 
from discord.ext import commands
import mal
from discord_slash import ButtonStyle,SlashCommand,SlashContext
from discord_slash.utils.manage_components import *
from discord_slash.utils.manage_commands import create_choice,create_option


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*', description="description", intents=intents)
slash = SlashCommand(bot,sync_commands=True)
bot.remove_command('help')

guild_ids = [667404420304338945,931591823485468713]

list_gif_hug = ["https://c.tenor.com/wUQH5CF2DJ4AAAAC/horimiya-hug-anime.gif"]

halp = """
\nbigz pour une photo du BigZ
\nanimesearch pour obtenir des id d'anime grâce a son nom 
\nanimeid pour obtenir une description d'anime grâce à son ID
\nctsur pour avoir notre sard pref
\nstatut pour changer le statut du bot"""

@bot.event
async def on_ready():
    print(bot.user.name+" est prêt a casser des culs !!!")
    print('------')

@slash.slash(description="Sardoche will come")
async def ctsur(message):
    await message.send("https://tenor.com/view/sardoche-sardrage-rage-mad-furious-gif-14796614")

@slash.slash(name="bigz",description="Invoque le BigZ",options=[
    create_option(
        name="fan",
        required=False,
        description="fanduz",
        option_type=6)
        ],guild_ids=guild_ids)
async def bigz(ctx:SlashContext,fan:discord.user):
    if fan != None:
        embed=discord.Embed(title = f"{ctx.author} à désigné {fan} comme un admirateur du Z",url="https://programme.zemmour2022.fr",description=f"{fan} est un admirateur du Z")
    else:
        embed=discord.Embed(title = "Le Big Z a un admirateur !",url="https://programme.zemmour2022.fr",description=str(ctx.author.name)+" est un admirateur du Z")
    embed.set_image(url="https://urlz.fr/hjHB")
    await ctx.send(embed=embed)

@slash.slash(name="statut",description="Change le statut du bot :)",options=[
    create_option(
        name="statut",
        required=True,
        description="Statut",
        option_type=3)
        ],guild_ids=guild_ids)
async def statut(ctx:SlashContext,statut:str):
    statut = discord.Game(statut)
    await bot.change_presence(status=discord.Status.idle, activity=statut)
    await ctx.send("Le statut du bot a été changé")

@slash.slash(name="hug",description="Fait un calin à une personne",options=[
    create_option(
        name="mension",
        required=True,      
        description="Mension",
        option_type=6)
        ],guild_ids=guild_ids)
async def statut(ctx:SlashContext,mension:discord.user):
    embed = discord.Embed(title= f'{ctx.author.name} fait un calin à {mension}')
    embed.set_image(url=list_gif_hug[0])
    await ctx.send(embed=embed)

@slash.slash(
    name="animesearch",
    description="Trouver la description d'un anime à partir de son nom",
    options=[
        create_option(
            name="nom_anime",
            required = True,
            description ="Find a anime",
            option_type=3
        )
    ])
async def animesearch(ctx: SlashContext, nom_anime:str):
    buttons = []
    result = mal.get_anime(nom_anime)
    embed=discord.Embed(title = "Liste des anime :", description=str(ctx.author.name)+" voici les anime qui peuvent correspondre à tes attentes :")
    for i in range(len(result)):
        embed.add_field(name=result[i][1],value="ID de l'anime : "+str(result[i][0]))
        buttons.append(create_button(style=ButtonStyle.blue,label=str(i+1),custom_id ="Anime"+str(i+1)))
    action_row = create_actionrow(*buttons)
    await ctx.send(embed=embed,components=[action_row])
    def check(m):
        return m.author.id == ctx.author.id
    button_ctx = await wait_for_component(bot,components=action_row,check=check)
    if button_ctx.custom_id == "Anime1" or "Anime2" or "Anime3" or "Anime4" or "Anime5":
        var = button_ctx.custom_id
        var = var.replace("Anime","")
        var = int(var)-1
        retur = mal.get_resume(result[var][0])
        embed = discord.Embed(title=retur[0],description=retur[3],url="https://myanimelist.net/anime/"+str(result[0][0]))
        embed.set_thumbnail(url=retur[7])
        embed.add_field(name="Date de 1re diffusion : ",value=retur[1], inline=False)
        embed.add_field(name="Date de fin : ",value=retur[2], inline=False)
        embed.add_field(name="Note : ",value=retur[4], inline=False)
        embed.add_field(name="Statut : ",value=retur[5])
        embed.add_field(name="Nombre d'épisodes : ",value=retur[6], inline=False)
        await button_ctx.edit_origin(embed=embed,components=[])


bot.run("VOTRE TOKEN DE BOT")
