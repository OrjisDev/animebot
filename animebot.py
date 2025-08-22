import discord
from discord.ext import commands
from discord import app_commands
import mal
from typing import Optional

intents = discord.Intents.default()
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='*', description="description", intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild_id in guild_ids:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

bot = MyBot()
bot.remove_command('help')

guild_ids = [667404420304338945, 931591823485468713]

list_gif_hug = ["https://c.tenor.com/wUQH5CF2DJ4AAAAC/horimiya-hug-anime.gif"]

halp = """
\nbigz pour une photo du BigZ
\nanimesearch pour obtenir des id d'anime grâce a son nom
\nanimeid pour obtenir une description d'anime grâce à son ID
\nctsur pour avoir notre sard pref
\nstatut pour changer le statut du bot"""

@bot.event
async def on_ready():
    print(bot.user.name + " est prêt a casser des culs !!!")
    print('------')
    await bot.setup_hook()

@bot.tree.command(description="Sardoche will come")
async def ctsur(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/sardoche-sardrage-rage-mad-furious-gif-14796614")

@app_commands.describe(fan="fanduz")
@bot.tree.command(name="bigz", description="Invoque le BigZ")
async def bigz(interaction: discord.Interaction, fan: Optional[discord.User] = None):
    if fan is not None:
        embed = discord.Embed(title=f"{interaction.user.name} à désigné {fan.name} comme un admirateur du Z", url="https://programme.zemmour2022.fr", description=f"{fan.name} est un admirateur du Z")
    else:
        embed = discord.Embed(title="Le Big Z a un admirateur !", url="https://programme.zemmour2022.fr", description=str(interaction.user.name) + " est un admirateur du Z")
    embed.set_image(url="https://urlz.fr/hjHB")
    await interaction.response.send_message(embed=embed)

@app_commands.describe(statut="Le statut à afficher")
@bot.tree.command(name="statut", description="Change le statut du bot :)")
async def statut(interaction: discord.Interaction, statut: str):
    game = discord.Game(statut)
    await bot.change_presence(status=discord.Status.idle, activity=game)
    await interaction.response.send_message("Le statut du bot a été changé")

@app_commands.describe(membre="La personne à qui faire un calin")
@bot.tree.command(name="hug", description="Fait un calin à une personne")
async def hug(interaction: discord.Interaction, membre: discord.User):
    embed = discord.Embed(title=f'{interaction.user.name} fait un calin à {membre.name}')
    embed.set_image(url=list_gif_hug[0])
    await interaction.response.send_message(embed=embed)

class AnimeSelect(discord.ui.Select):
    def __init__(self, animes: list):
        self.animes = animes
        options = [
            discord.SelectOption(label=title, value=str(anime_id))
            for anime_id, title in animes
        ]
        super().__init__(placeholder="Choisis un anime...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        anime_id = self.values[0]
        retur = mal.get_resume(anime_id)
        embed = discord.Embed(title=retur[0], description=retur[3], url=f"https://myanimelist.net/anime/{anime_id}")
        embed.set_thumbnail(url=retur[7])
        embed.add_field(name="Date de 1re diffusion : ", value=retur[1], inline=False)
        embed.add_field(name="Date de fin : ", value=retur[2], inline=False)
        embed.add_field(name="Note : ", value=retur[4], inline=False)
        embed.add_field(name="Statut : ", value=retur[5])
        embed.add_field(name="Nombre d'épisodes : ", value=retur[6], inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

class AnimeView(discord.ui.View):
    def __init__(self, animes: list, author_id: int):
        super().__init__(timeout=60)
        self.add_item(AnimeSelect(animes))
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author_id

@app_commands.describe(nom_anime="Le nom de l'anime à rechercher")
@bot.tree.command(name="animesearch", description="Trouver la description d'un anime à partir de son nom")
async def animesearch(interaction: discord.Interaction, nom_anime: str):
    result = mal.get_anime(nom_anime)
    if not result:
        await interaction.response.send_message("Aucun anime trouvé pour cette recherche.", ephemeral=True)
        return

    embed = discord.Embed(title="Liste des animes :", description=f"{interaction.user.name}, voici les animes qui peuvent correspondre à tes attentes :")
    for anime_id, title in result:
        embed.add_field(name=title, value=f"ID de l'anime : {anime_id}", inline=False)

    view = AnimeView(result, interaction.user.id)
    await interaction.response.send_message(embed=embed, view=view)

bot.run("VOTRE TOKEN DE BOT")
